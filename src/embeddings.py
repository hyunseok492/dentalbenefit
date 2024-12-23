import openai
import numpy as np
import pickle
from config import OPENAI_API_KEY, EMBEDDING_MODEL
openai.api_key = OPENAI_API_KEY

def get_embedding(text, model=EMBEDDING_MODEL):
    response = openai.Embedding.create(
        input=[text],
        model=model
    )
    embedding = response['data'][0]['embedding']
    return np.array(embedding, dtype=np.float32)

def create_vectorstore(docs):
    # docs: [{"filename":..., "text":...}, ...]
    embeddings = []
    metadata = []
    for doc in docs:
        embedding = get_embedding(doc["text"])
        embeddings.append(embedding)
        metadata.append(doc["filename"])
    embeddings = np.vstack(embeddings)
    return embeddings, metadata

def save_vectorstore(embeddings, metadata, vectorstore_path, meta_path):
    with open(vectorstore_path, 'wb') as f:
        pickle.dump(embeddings, f)
    with open(meta_path, 'wb') as f:
        pickle.dump(metadata, f)

def load_vectorstore(vectorstore_path, meta_path):
    with open(vectorstore_path, 'rb') as f:
        embeddings = pickle.load(f)
    with open(meta_path, 'rb') as f:
        metadata = pickle.load(f)
    return embeddings, metadata
