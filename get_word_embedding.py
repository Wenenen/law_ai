import torch
from pytorch_pretrained_bert import BertModel


def get_word_embedding(input):
    model = BertModel.from_pretrained('ms')
    embedding = model.embeddings.word_embeddings
    print(embedding)
    print(embedding(input))


def get_word_embedding_google_model(input):
    model = BertModel.from_pretrained('bert-base-uncased')
    embedding = model.embeddings.word_embeddings
    print(embedding)
    print(embedding(input))


if __name__ == '__main__':
    input = torch.LongTensor([[1, 2, 4, 5], [0, 3, 2, 9]])
    get_word_embedding(input)

    get_word_embedding_google_model(input)