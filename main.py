from fastapi import FastAPI
from pydantic import BaseModel
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Import after loading env to ensure API key is available
from app.documents import add_document
from app.ask import services.rag_question

# Initialize FastAPI app
app = FastAPI()

# Pydantic models for input
class DocIn(BaseModel):
    text: str

class QuestionIn(BaseModel):
    question: str

# Upload endpoint
@app.post("/upload")
def upload_doc(doc: DocIn):
    add_document(doc.text)
    return {"status": "Document uploaded"}

# Ask question endpoint
@app.post("/ask")
def ask(question: QuestionIn):
    answer = ask_question(question.question)
    return {"answer": answer}
