import numpy as np

from scipy.spatial import distance_matrix

def distance_sample(embedding, n=100):
    """Pairwise Distance quantiles
    embedding - np.array
    n


    Returns:
    tuple of:
      embedding
      np.array (embedding[0] x n) where X[i,j] is the jth quantile for point i
      n
    """
    D_quantile = distance_matrix(
        embedding,
        embedding[np.random.choice(embedding.shape[0], n), :]
    )
    D_quantile.sort()
    return embedding, D_quantile, n

def qdist(dsample, alter):
    """Quantilized distances between dsample and alter

    Parameters:
    dsample - from distance_sample
    alter - np.array, same number of columns as dsample embedding


    Returns:
    np.array(embedding[0] x alter[0]) of distance quantiles 0-100
    """
    embedding, D_quantile, n = dsample

    D_alter = distance_matrix(embedding, alter)


    D_alter_quantile =  np.array([ np.searchsorted(D_quantile[i,:], D_alter[i,:]) for i in range(embedding.shape[0])  ])
    D_alter_quantile = 100 *( 1 - D_alter_quantile / n)
    return D_alter_quantile
