from sklearn.feature_extraction import FeatureHasher

import nltk.stem
import nltk.corpus

import re

def hashtrick(txt, n_buckets=1024):
    stemmer = nltk.stem.SnowballStemmer("english").stem
    stopwords = set(nltk.corpus.stopwords.words("english"))

    txt = map(str.lower, txt)
    txt = map(re.compile(r"\w+").findall, txt)
    txt = map(lambda x: set(x) - stopwords, txt)
    txt = map(lambda x: map(stemmer, x), txt)

    return FeatureHasher(n_buckets, input_type='string').transform(txt).todense()


