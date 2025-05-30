from qdrant_client import QdrantClient
from qdrant_client.http.models import VectorParams, Distance

client = QdrantClient(
    url="https://<your-qdrant-url>",
    api_key="your_api_key_here"
)

client.recreate_collection(
    collection_name="centria-docs",
    vectors_config=VectorParams(size=768, distance=Distance.COSINE),
)
