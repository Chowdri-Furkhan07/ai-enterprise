from langchain.embeddings import HuggingFaceEmbeddings

class EmbeddingModel:
    def __init__(self):
        self.model = HuggingFaceEmbeddings(
            model_name="sentence-transformers/all-MiniLM-L6-v2"
        )

    def embed_documents(self, docs):
        texts = [doc.page_content for doc in docs]
        return self.model.embed_documents(texts)

    def embed_query(self, query):
        return self.model.embed_query(query)
