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

self.vectorizer = TfidfVectorizer(
    # 검색 시 불필요한 단어를 걸러내는 최소/최대 문서 빈도
    min_df=2,   # 2개 이하의 문서에서만 등장하는 단어는 무시
    max_df=0.8, # 전체 문서의 80% 이상에서 등장하는 단어는 무시
    # ngram_range=(1,2), etc.
).fit(texts)
        self.tfidf_matrix = self.vectorizer.transform(texts)
        self.metadata = docs

    def search(self, query, top_k=2, min_score=0.3):
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
