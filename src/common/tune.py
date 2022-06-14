"""Tuning PacMAP

This module contains the helper methods necessary to tune a PacMAP model. If
run directly, using

    python -m eonacs.common.tune

It will load data and run 100 iterations of hyperopt, and print the best fit found.

The loss function is a nonparametric 'stress' - the ability of the reduced
space to represent distances between points. This is captured by the spearman
correlation of the pairwise distances between the complete points and reduced
dimensionality points.


"""
import time

import pandas as pd
import numpy as np

from scipy.stats import spearmanr
from scipy.spatial.distance import pdist

import pacmap

def loss(Y, Yhat):
    """Spearman stress
    """
    r = spearmanr(pdist(Y), pdist(Yhat)).correlation
    return 1-r


def cv_par(features, nfolds, loss, pacmap_params):
    """Cross validation
    """
    folds = np.random.randint(0, nfolds, features.shape[0])
    ARGS = zip(range(nfolds), (features,)*nfolds, (folds,)*nfolds, (loss,)*nfolds, (pacmap_params,)*nfolds)

    return map(score_fold_par, ARGS)


def score_fold_par(ARGS):
    """Score a single fold
    """
    i, features, folds, loss, pacmap_params = ARGS
    train, test = features[folds != i, :], features[folds == i, :]
    m = pacmap.PaCMAP(**pacmap_params, save_tree=True)
    pred = m.fit(train).transform(test)
    return loss(test, pred)



############################

import hyperopt
from hyperopt import hp, space_eval, fmin, Trials, pyll

space = (
    hp.quniform("n_buckets", 4, 4096, 4),
    [
        hp.qloguniform("n_components", np.log(2), np.log(1000), 1),
        hp.quniform("n_near", 3, 60, 1),
        hp.quniform("n_mid",  3, 60, 1),
        hp.quniform("n_far",  3, 60, 1),
        hp.lognormal("lr", 0, .5)
    ]
)

##############################

from eonacs.common.bloom import bloom_categories
from eonacs.common.nlp import hashtrick

def a_trial(s):
    """Run a single trial for tuning

    Parameters:
    s: hyperparamters

    Returns:
    Trial results

    """

    NFOLDS=5

    buckets = int(s[0])
    pacmap_params = s[1]

    pacmap_params = dict(
        n_components = int(pacmap_params[0]),
        n_neighbors  = int(pacmap_params[1]),
        MN_ratio = pacmap_params[2] / pacmap_params[1],
        FP_ratio = pacmap_params[3] / pacmap_params[1],
        lr = pacmap_params[4]

    ) #s[1]

    big = \
        np.concatenate( [ hyper_e,
                          bloom_categories(tasks["text"]),
                          hashtrick(tasks["text"], buckets) ],
                       axis=1)
    big = np.asarray(big)

    try :
        tic = time.time()
        scores = cv_par(big, NFOLDS, loss, pacmap_params)
        toc = time.time()
        scores = sorted(scores)
        return {'loss': scores[2],
                'true_loss':scores[2],
                'true_loss_variance':scores[4] - scores[0],
                'time': toc - tic,
                'status': hyperopt.STATUS_OK }
    except :
        return {'status': hyperopt.STATUS_FAIL}


if __name__ == "__main__":


    EMBED = "data/tasks_dbert_hyper_e_refactor.pkl.gz"
    print("Loading data...")
    tasks, hyper_e = pd.read_pickle(EMBED)

    t = pd.read_pickle("data/hyperopt_refactor.pkl") # Trials()
    TRIAL_PICKLE = "data/hyperopt_refactor_100.pkl.gz"
    best = fmin(a_trial, space, hyperopt.tpe.suggest, 100, trials=t)
    pd.to_pickle(t, TRIAL_PICKLE)
    print(best)






