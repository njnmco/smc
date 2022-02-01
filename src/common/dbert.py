import transformers
import torch
import numpy as np

_device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")

def set_device(device):
    global _device
    _device = device


def dbert():
    tokenizer = transformers.DistilBertTokenizer.from_pretrained('distilbert-base-uncased')
    model = transformers.DistilBertModel.from_pretrained('distilbert-base-uncased')
    return tokenizer, model

# NB - must pad with zeros, using other values could lead to downstream array indexing errors
# NB - truncate to K tokens to keep memory usage down.
def pad_series(series, K=50):
    K = min(K, series.apply(len).max())
    for x in series:
        x.extend([0]*(K - len(x)))
        x[:] = x[:K]

def tokens_to_np(toks):
    return np.array(toks.to_list())

# Note available in itertools until 3.10
def pairwise(iterable):
    from itertools import tee
    # pairwise('ABCDEFG') --> AB BC CD DE EF FG
    a, b = tee(iterable)
    next(b, None)
    return zip(a, b)

def get_embeddings(phrases, tokenizer=None, model=None):
    if tokenizer is None and model is None:
	tokenizer, model = dbert()
    toks = phrases.apply(tokenizer.encode)

    pad_series(toks, 66)
    X = tokens_to_np(toks)
    features = apply_model(model, X)
    return features

def apply_model(model, X):

    ret = list()

    print(f"Using {_device}")
    model = model.to(_device)

    def embed_slice(X):
        input_ids = torch.tensor(X)
        attention_mask = torch.tensor(np.where(X != 0, 1, 0))


        input_ids = input_ids.to(_device)
        attention_mask = attention_mask.to(_device)

        with torch.no_grad():
            last_hidden_states = model(input_ids, attention_mask=attention_mask)

        features = last_hidden_states[0][:,0,:].cpu().numpy()
        return features

    N = X.shape[0]
    for i,j in pairwise(range(0, N, 1024)):
        print(f"{i}...")
        ret.append(embed_slice(X[i:j,:]))

    if j < N:
        print(f"{j}...")
        ret.append(embed_slice(X[j:N,:]))


    return np.concatenate(ret)


