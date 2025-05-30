from langchain.schema import Document
from app.vector_store import vector_store

def add_document(text: str, metadata: dict = None):
    doc = Document(page_content=text, metadata=metadata or {})
    vector_store.add_documents([doc])
