from fastapi import FastAPI
from pydantic import BaseModel
from app.documents import add_document
from app.ask import services.rag_question
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

class DocIn(BaseModel):
    text: str

class QuestionIn(BaseModel):
    question: str

@app.post("/upload")
def upload_doc(doc: DocIn):
    add_document(doc.text)
    return {"status": "Document uploaded"}

@app.post("/ask")
def ask(question: QuestionIn):
    answer = ask_question(question.question)
    return {"answer": answer}
