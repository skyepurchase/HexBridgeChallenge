import numpy as np

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.preprocessing import Normalizer
from sklearn.cluster import KMeans


def init():
    '''
        Load data from database and do initial clustering.
    '''


def process_user(user_id, weighted_texts, add_to_model=True):
    '''
        Update the model with new user.

        user_id: unique identifier of the user, will be passed to db function
        weighted_texts: iterable of tuples (weight, text)
                        where text has to be taken into account by multiplier weight
        add_to_model: if False, model will not be updated, only cluster will be looked up

        returns: ([user_ids of similar people], [user_ids of very different people])
    '''

    return [], []

