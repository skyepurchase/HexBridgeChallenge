import numpy as np

from matplotlib import pyplot as plt
from matplotlib.collections import LineCollection

from sklearn import manifold
from sklearn.metrics import euclidean_distances
from sklearn.decomposition import PCA


def plot_network(points):
    EPSILON = np.finfo(np.float32).eps
    d=euclidean_distances(points)
    mds=manifold.MDS(dissimilarity='precomputed')
    pos=mds.fit(d).embedding_
    # Rescale the data
    pos *= np.sqrt((d ** 2).sum()) / np.sqrt((pos ** 2).sum())

    # Rotate the data
    clf = PCA(n_components=2)
    X_true = clf.fit_transform(X_true)

    pos = clf.fit_transform(pos)

    fig = plt.figure(1)
    ax = plt.axes([0., 0., 1., 1.])

    s = 100
    plt.scatter(d[:, 0], d[:, 1], color='navy', s=s, lw=0, label='Position')
    plt.legend(scatterpoints=1, loc='best', shadow=False)

    d = d.max() / (d + EPSILON) * 100
    np.fill_diagonal(d, 0)
    # Plot the edges
    start_idx, end_idx = np.where(pos)
    # a sequence of (*line0*, *line1*, *line2*), where::
    #            linen = (x0, y0), (x1, y1), ... (xm, ym)
    segments = [[d[i, :], d[j, :]]
                for i in range(len(pos)) for j in range(len(pos))]
    values = np.abs(d)
    lc = LineCollection(segments,
                        zorder=0, cmap=plt.cm.Blues,
                        norm=plt.Normalize(0, values.max()))
    lc.set_array(d.flatten())
    lc.set_linewidths(np.full(len(segments), 0.5))
    ax.add_collection(lc)

    plt.savefig('network.png')
    plt.show()