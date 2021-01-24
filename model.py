import numpy as np
import scipy

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.preprocessing import Normalizer
from sklearn.cluster import KMeans

# Import Astra API
from astra import save_user, load_all_users

# Import vocabulary
from vocabulary import vocabulary

# Constants
NUM_CLUSTERS = 25


class Model:

    def __init__(self):
        '''
            Load data from database and do initial clustering.
        '''

        # Current list of user_ids
        self.uids = []

        # Initialise vector stack
        self.X = scipy.sparse.csr.csr_matrix((0, len(vocabulary)))

        # Create uid list and vector stack
        db_entries = load_all_users()
        for uid, fvector in db_entries:
            self.uids.append(uid)
            self.X = scipy.sparse.vstack([self.X, fvector])

        # Do initial clustering
        self.kmeans = KMeans(n_clusters=min(NUM_CLUSTERS, self.X.shape[0]))
        self.kmeans.fit(self.X)


    def process_user(self, user_id, weighted_texts, add_to_model=True):
        '''
            Update the model with new user.

            user_id: unique identifier of the user, will be passed to db function
            weighted_texts: iterable of tuples (weight, text)
                            where text has to be taken into account by multiplier weight
            add_to_model: if False, model will not be updated, only cluster will be looked up

            returns: ([user_ids of similar people], [user_ids of very different people])
        '''

        # Vectorize the text
        counts = scipy.sparse.csr.csr_matrix((1, len(vocabulary)))
        vectorizer = CountVectorizer(vocabulary=vocabulary)

        for multiplier, text in weighted_texts:
            counts += vectorizer.fit_transform([text]) * multiplier

        # Normalize the vector
        normalizer = Normalizer(copy=False)
        counts = normalizer.transform(counts)

        if add_to_model == True:

            # Persist user
            save_user(user_id, counts)

            # Push to existing data
            self.uids.append(user_id)
            self.X = scipy.sparse.vstack([self.X, counts])

            # Do more iterations of the clustering
            # Might want to set a smaller max_iter here
            self.kmeans = KMeans(n_clusters=min(NUM_CLUSTERS, self.kmeans.n_clusters),
                                 init=self.kmeans.cluster_centers_)
            self.kmeans.fit(self.X)

            # Look up the cluster of the new user
            user_cluster = self.kmeans.labels_[-1]

        else:
            user_cluster = self.kmeans.predict(counts)

        # Find users in the same cluster
        same_cluster_users = [self.uids[i] for i in range(len(self.uids)) if self.kmeans.labels_[i] == user_cluster]

        # Find furthest cluster
        maxdist = 0
        furthest_cluster = -1
        for label, centre in enumerate(self.kmeans.cluster_centers_):
            diffvec = centre - counts
            dist = np.inner(diffvec, diffvec)
            if dist > maxdist:
                maxdist = dist
                furthest_cluster = label

        # Find users in the cluster furthest away
        furthest_cluster_users = [self.uids[i] for i in range(len(self.uids)) if self.kmeans.labels_[i] == furthest_cluster]

        return same_cluster_users, furthest_cluster_users


if __name__ == "__main__":
    print(Model().process_user({'twitter': "asd", 'reddit': "ajsdk"}, [(1, "He just visited Trump but didn't like right wing stuff")], add_to_model=True))


