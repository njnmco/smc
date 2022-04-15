import pacmap
from sklearn.preprocessing import StandardScaler
import numpy as np


def reduction(features):

    scale = StandardScaler()

    features = scale.fit_transform(features)

    reducer = umap.UMAP()
    embedding = reducer.fit_transform(features)

    return scale, reducer, embedding


