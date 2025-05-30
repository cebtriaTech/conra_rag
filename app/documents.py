import os
from langchain.docstore.document import Document
from app.vector_store import vector_store, embedder, VECTOR_STORE_DIR
from langchain_community.vectorstores import FAISS

def add_document(text: str):
    global vector_store

    doc = Document(page_content=text)
    if vector_store is None:
        # First document — create the index
        vector_store = FAISS.from_documents([doc], embedder)
    else:
        # Append to existing index
        vector_store.add_documents([doc])

    os.makedirs(VECTOR_STORE_DIR, exist_ok=True)
    vector_store.save_local(VECTOR_STORE_DIR)
