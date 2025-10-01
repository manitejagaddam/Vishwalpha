from qdrant_client import QdrantClient
from qdrant_client.http import models

# Connect to Qdrant
client = QdrantClient(url="http://localhost:6333")

COLLECTION_NAME = "chatbot_docs"

def insert_document(doc_id: int, text: str, vector: list):
    client.upsert(
        collection_name=COLLECTION_NAME,
        points=[models.PointStruct(id=doc_id, vector=vector, payload={"text": text})]
    )

def search_similar(vector: list, top_k: int = 5):
    results = client.search(
        collection_name=COLLECTION_NAME,
        query_vector=vector,
        limit=top_k
    )
    return [r.payload["text"] for r in results]
