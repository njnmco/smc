import transformers

def dbert():
    tokenizer = transformers.DistilBertTokenizer.from_pretrained('distilbert-base-uncased')
    model = transformers.DistilBertModel.from_pretrained('distilbert-base-uncased')
    return tokenizer, model

