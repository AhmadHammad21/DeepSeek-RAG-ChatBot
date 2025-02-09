import numpy as np
import faiss
from transformers import AutoTokenizer, AutoModel
import torch

class PDFEmbeddingIndexer:
    def __init__(self, embedding_model_name):
        self.tokenizer = AutoTokenizer.from_pretrained(embedding_model_name)
        self.model = AutoModel.from_pretrained(embedding_model_name)
        self.index = None
        self.documents = []

    def embed_text(self, text):
        inputs = self.tokenizer(text, return_tensors="pt", truncation=True, padding=True)
        with torch.no_grad():
            outputs = self.model(**inputs)
        return outputs.last_hidden_state.mean(dim=1).numpy()

    def build_index(self, documents):
        self.documents = documents
        embeddings = [self.embed_text(doc) for doc in documents]
        dimension = embeddings[0].shape[1]

        self.index = faiss.IndexFlatL2(dimension)
        for emb in embeddings:
            self.index.add(emb)

