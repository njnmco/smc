import pandas as pd
import numpy as np

import re
import nltk.stem

# https://www.apu.edu/live_data/files/333/blooms_taxonomy_action_verbs.pdf
bloom = dict(
    remembering=["Choose","Define","Find","How","Label","List","Match","Name","Omit","Recall","Relate","Select","Show","Spell","Tell","What","When","Where","Which","Who","Why"],
    understanding=["Classify","Compare","Contrast","Demonstrate","Explain","Extend","Illustrate","Infer","Interpret","Outline","Relate","Rephrase","Show","Summarize","Translate"],
    applying=["Apply","Build","Choose","Construct","Develop","Experiment","Identify","Interview","Make","Model","Organize","Plan","Select","Solve","Utilize"],
    analyzing=["Analyze","Assume","Categorize","Classify","Compare","Conclusion","Contrast","Discover","Dissect","Distinguish","Divide","Examine","Function","Inference","Inspect","List","Motive","Relationships","Simplify","Survey","Take","Test","Theme"],
    evaluating=["Agree","Appraise","Assess","Award","Choose","Compare","Conclude","Criteria","Criticize","Decide","Deduct","Defend","Determine","Disprove","Estimate","Evaluate","Explain","Importance","Influence","Interpret","Judge","Justify","Mark","Measure","Opinion","Perceive","Prioritize","Prove","Rate","Recommend","Rule","Select","Support","Value"],
    creating=["Adapt","Build","Change","Choose","Combine","Compile","Compose","Construct","Create","Delete","Design","Develop","Discuss","Elaborate","Estimate","Formulate","Happen","Imagine","Improve","Invent","Make","Maximize","Minimize","Modify","Original","Originate","Plan","Predict","Propose","Solution","Solve","Suppose","Test","Theory"]
)

def bloom_categories(tasks):
    """Bloom's Taxonomy embedding

    Embed tasks using Bloom's taxonomy

    Parameters:
    tasks (pd.Series): Text

    Returns:
    np.array, rows normalized to sum to unity


    """

    stemmer = nltk.stem.SnowballStemmer("english").stem

    bloom_mat = np.zeros((len(tasks), len(bloom)))
    for i, K in enumerate(bloom):
        v = map(stemmer, bloom[K])
        r = r"\b(?:%s)" % "|".join(v)
        bloom_mat[:,i] = tasks.str.contains(r, flags=re.IGNORECASE)

    #https://stackoverflow.com/a/16202486/986793
    bloom_mat = bloom_mat / np.maximum(1, bloom_mat.sum(axis=1)[:,None])
    return pd.DataFrame(bloom_mat,columns=bloom.keys())
