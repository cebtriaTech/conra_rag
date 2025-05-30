import os
from dotenv import load_dotenv
from langchain_community.vectorstores import Qdrant
from langchain_community.embeddings import OpenAIEmbeddings
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams

# Load environment variables
load_dotenv()

QDRANT_URL = os.getenv("QDRANT_URL", "http://localhost:6333")
QDRANT_COLLECTION = os.getenv("QDRANT_COLLECTION", "centria_docs")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

if not OPENAI_API_KEY:
    raise ValueError("Missing OPENAI_API_KEY in environment variables.")

# Embeddings using OpenAI's text-embedding-3-small
embedder = OpenAIEmbeddings(
    model="text-embedding-3-small",
    openai_api_key=OPENAI_API_KEY
)

# Connect to local or cloud Qdrant
client = QdrantClient(
    url=QDRANT_URL,
)

# Ensure collection exists (optional if already created)
client.recreate_collection(
    collection_name=QDRANT_COLLECTION,
    vectors_config=VectorParams(size=1536, distance=Distance.COSINE),
)

# Bind collection with LangChain wrapper
vector_store = Qdrant(
    client=client,
    collection_name=QDRANT_COLLECTION,
    embeddings=embedder
)
