from pinecone import Pinecone, ServerlessSpec
from core.embeddings import EmbeddingModel
from app.config import PINECONE_API_KEY

class PineconeStore:
    def __init__(self, index_name="enterprise-ai", dimension=384):
        """
        dimension:
        - 384 → for all-MiniLM-L6-v2
        - 1536 → for OpenAI embeddings
        """
        self.index_name = index_name
        self.dimension = dimension

        # Initialize Pinecone
        self.pc = Pinecone(api_key=PINECONE_API_KEY)

        # Create index if not exists
        existing_indexes = [i["name"] for i in self.pc.list_indexes()]
        if self.index_name not in existing_indexes:
            self.pc.create_index(
                name=self.index_name,
                dimension=self.dimension,
                metric="cosine",
                spec=ServerlessSpec(
                    cloud="aws",
                    region="us-east-1"
                )
            )

        # Connect to index
        self.index = self.pc.Index(self.index_name)

        # Embedding model
        self.embedder = EmbeddingModel()

    # -------------------------------
    # UPSERT DOCUMENTS
    # -------------------------------
    def upsert_documents(self, docs):
        """
        docs: List of LangChain Document objects
        """
        texts = [doc.page_content for doc in docs]
        metadatas = [doc.metadata for doc in docs]

        embeddings = self.embedder.embed_documents(docs)

        vectors = []
        for i, (emb, meta, text) in enumerate(zip(embeddings, metadatas, texts)):
            vectors.append({
                "id": f"doc_{i}",
                "values": emb,
                "metadata": {
                    "text": text,
                    **meta
                }
            })

        self.index.upsert(vectors=vectors)
        return {"status": "success", "count": len(vectors)}

    # -------------------------------
    # QUERY
    # -------------------------------
    def query(self, query_text, top_k=3):
        """
        Returns top_k similar documents
        """
        query_vector = self.embedder.embed_query(query_text)

        results = self.index.query(
            vector=query_vector,
            top_k=top_k,
            include_metadata=True
        )

        matches = []
        for match in results["matches"]:
            matches.append({
                "score": match["score"],
                "text": match["metadata"].get("text", ""),
                "metadata": match["metadata"]
            })

        return matches

    # -------------------------------
    # DELETE ALL DATA
    # -------------------------------
    def clear_index(self):
        """
        Deletes all vectors from index
        """
        self.index.delete(delete_all=True)
        return {"status": "cleared"}

    # -------------------------------
    # DELETE SPECIFIC IDS
    # -------------------------------
    def delete_ids(self, ids):
        """
        ids: list of vector IDs
        """
        self.index.delete(ids=ids)
        return {"deleted_ids": ids}

    # -------------------------------
    # INDEX STATS
    # -------------------------------
    def stats(self):
        return self.index.describe_index_stats()