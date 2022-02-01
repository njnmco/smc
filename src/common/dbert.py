import transformers
import torch
import numpy as np

_device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")


def dbert():
    tokenizer = transformers.DistilBertTokenizer.from_pretrained('distilbert-base-uncased')
    model = transformers.DistilBertModel.from_pretrained('distilbert-base-uncased')
    return tokenizer, model

# NB - must pad with zeros, using other values could lead to downstream array indexing errors
def pad_series(series):
    series.apply(lambda x, max_width: x.extend([0]*(max_width - len(x))),
                 max_width = series.apply(len).max()    )

def tokens_to_np(toks):
    return np.array(dwa_tok.to_list())

def get_embeddings(model, X):
    input_ids = torch.tensor(X)
    attention_mask = torch.tensor(np.where(X != 0, 1, 0))

    print(f"Using {_device}")

    input_ids = input_ids.to(device)
    attention_mask = attention_mask.to(device)
    model = model.to(device)

    with torch.no_grad():
            last_hidden_states = model(input_ids, attention_mask=attention_mask)

    features = last_hidden_states[0][:,0,:].cpu().numpy()

    return features


