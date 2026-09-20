from langchain_community.vectorstores import FAISS
from core.embeddings import EmbeddingModel

class FAISSStore:
    def __init__(self):
        self.embedder = EmbeddingModel()
        self.db = None

    def create_index(self, docs):
        self.db = FAISS.from_documents(docs, self.embedder.model)

    def save(self, path="faiss_index"):
        if self.db:
            self.db.save_local(path)

    def load(self, path="faiss_index"):
        self.db = FAISS.load_local(path, self.embedder.model)

    def query(self, query):
        if self.db is None:
            return []
        return self.db.similarity_search(query, k=3)