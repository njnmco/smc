import umap
from pacmap import pacmap
from sklearn.preprocessing import StandardScaler


def reduction(features):

    scale = StandardScaler()

    features = scale.fit_transform(features)

    reducer = umap.UMAP()
    embedding = reducer.fit_transform(features)

    return scale, reducer, embedding



class PaCMAP2(pacmap.PaCMAP):

  def fit(self, X, *args, **kwargs):
    super().fit(X, Xp=X[:2, :], *args, **kwargs)
    self.X = X
    self.embedding_ = self.embedding_[0]
    self.proj = np.linalg.lstsq(self.X, self.embedding_)[0]


  def transform(self, Xp, iters=None, lr=None):

    new_embed = np.concatenate((
        self.embedding_,
        np.matmul(Xp, self.proj)
    ))

    new_embed, _, _, _, _ = pacmap.pacmap(
        self.X,
        self.n_dims,
        self.n_neighbors,
        self.n_MN,
        self.n_FP,
        self.pair_neighbors,
        self.pair_MN,
        self.pair_FP,
        self.distance,
        lr or self.lr,
        iters or self.num_iters,
        new_embed, ### !!!
        self.apply_pca,
        self.verbose,
        self.intermediate,
        self.random_state, Xp
    )

    proj = np.linalg.lstsq(new_embed[0], self.embedding_)[0]

    #print(proj)

    new_embed = [np.matmul(x, proj) for x in new_embed]

    return new_embed

