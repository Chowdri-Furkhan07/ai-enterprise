from core.llm import LLM
from core.pinecone_db import PineconeStore
from core.faiss_db import FAISSStore
from core.embeddings import EmbeddingModel

class RetrievalAgent:
    def __init__(self):
        self.llm = LLM()
        self.pinecone = PineconeStore()
        self.faiss = FAISSStore()

    def run(self, q):
        # First try Pinecone
        docs = self.pinecone.query(q, top_k=3)
        
        # If Pinecone returns no results, try FAISS
        if not docs:
            docs = self.faiss.query(q)
        
        # Combine results for context
        context = "\n\n".join([d["text"] for d in docs]) if docs else "No relevant documents found."
        
        prompt = f"""
        Use the following documents to answer the question.
        
        Documents:
        {context}
        
        Question: {q}
        
        Provide a accurate and helpful answer based on the documents.
        """
        
        return self.llm.generate(prompt)
    
    def index_documents(self, docs):
        """Index documents to both Pinecone and FAISS for retrieval"""
        # Upsert to Pinecone
        self.pinecone.upsert_documents(docs)
        
        # Create and save FAISS index
        self.faiss.create_index(docs)
        self.faiss.save("faiss_index")
        
        return {"status": "documents indexed"}

