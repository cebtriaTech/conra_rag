from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from dotenv import load_dotenv
import os

load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
embedder = OpenAIEmbeddings(openai_api_key=api_key)

VECTOR_STORE_DIR = "vector_store"

# Only load if there’s a saved index directory
if os.path.isdir(VECTOR_STORE_DIR):
    vector_store = FAISS.load_local(
        VECTOR_STORE_DIR,
        embedder,
        allow_dangerous_deserialization=True
    )
else:
    vector_store = None
