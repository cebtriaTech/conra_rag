from fastapi import FastAPI, UploadFile, File
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from dotenv import load_dotenv
import os
import shutil

from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import FAISS
from langchain.chains import RetrievalQA
from langchain.text_splitter import CharacterTextSplitter
from langchain.document_loaders import (
    TextLoader,
    PyPDFLoader,
    UnstructuredWordDocumentLoader,
)

from langchain_openai import ChatOpenAI
from langchain_community.chat_models import ChatOpenRouter

load_dotenv()

app = FastAPI()

embedding = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
vectorstore = None

# Choose between OpenAI and OpenRouter
use_openrouter = os.getenv("USE_OPENROUTER", "false").lower() == "true"

if use_openrouter:
    llm = ChatOpenRouter(
        model_name="mistralai/mistral-7b-instruct",
        openai_api_key=os.getenv("OPENROUTER_API_KEY")
    )
else:
    llm = ChatOpenAI(
        model_name="gpt-3.5-turbo",
        temperature=0,
        openai_api_key=os.getenv("OPENAI_API_KEY")
    )

def get_loader(file_path):
    ext = os.path.splitext(file_path)[1].lower()
    if ext == ".txt":
        return TextLoader(file_path)
    elif ext == ".pdf":
        return PyPDFLoader(file_path)
    elif ext == ".docx":
        return UnstructuredWordDocumentLoader(file_path)
    else:
        raise ValueError(f"Unsupported file type: {ext}")

@app.post("/upload/")
async def upload_files(files: list[UploadFile] = File(...)):
    global vectorstore
    os.makedirs("temp_docs", exist_ok=True)
    all_docs = []

    for file in files:
        file_location = f"temp_docs/{file.filename}"
        with open(file_location, "wb") as f:
            shutil.copyfileobj(file.file, f)

        loader = get_loader(file_location)
        documents = loader.load()
        text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
        docs = text_splitter.split_documents(documents)
        all_docs.extend(docs)

    vectorstore = FAISS.from_documents(all_docs, embedding)
    return {"status": "success", "message": f"Processed {len(files)} file(s)."}

class Query(BaseModel):
    question: str

@app.post("/ask/")
async def ask_question(query: Query):
    global vectorstore
    if not vectorstore:
        return JSONResponse(status_code=400, content={"error": "Please upload document(s) first."})
    try:
        qa = RetrievalQA.from_chain_type(
            llm=llm,
            chain_type="stuff",
            retriever=vectorstore.as_retriever()
        )
        answer = qa.run(query.question)
        return {"question": query.question, "answer": answer}
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})
