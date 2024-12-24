import os
import pickle
from sklearn.feature_extraction.text import TfidfVectorizer # type: ignore
import numpy as np

class SearchEngine:
    def __init__(self, vectorizer=None, tfidf_matrix=None, metadata=None):
        self.vectorizer = vectorizer
        self.tfidf_matrix = tfidf_matrix
        self.metadata = metadata

    def fit(self, docs):
        # docs: [{"filename": ..., "chunk_index": ..., "text": ...}, ...]
        texts = [d["text"] for d in docs]
       from sklearn.feature_extraction.text import TfidfVectorizer

self.vectorizer = TfidfVectorizer() .fit(texts)
        self.tfidf_matrix = self.vectorizer.transform(texts)
        self.metadata = docs

    def search(self, query, top_k=2.5, min_score=0.3):
        query_vec = self.vectorizer.transform([query])
        scores = (self.tfidf_matrix * query_vec.T).toarray().ravel()
        top_indices = np.argsort(scores)[::-1][:top_k]
        results = [self.metadata[i] for i in top_indices]
        return results

    def save(self, path):
        with open(path, 'wb') as f:
            pickle.dump((self.vectorizer, self.tfidf_matrix, self.metadata), f)

    def load(self, path):
        with open(path, 'rb') as f:
            self.vectorizer, self.tfidf_matrix, self.metadata = pickle.load(f)
