# smc / Cloud Skills Aligment


This contains a python package and associated Google Colab notebooks for the project.


## Training

See `notebooks/train` - there are 3 phases:

1. Fine Tune distilbert to ONET tasks
2. Construct PacMAP embedding of distilbert to reduce dimensionality
3. Fine Tune distilbert to Embeddings to simplify code path / prediction

## Scoring

See `notebooks/score` - two use cases

1. Compute pairwise distances between a set of course objectives and occupational tasks
2. Index all tasks, and use nearest neighbors to search for relevant occupations.

