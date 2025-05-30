# main.py
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse
from app.rag import process_pdf, ask_question
from tempfile import NamedTemporaryFile
import shutil

app = FastAPI()

@app.post("/upload")
async def upload_pdf(file: UploadFile = File(...)):
    # Accept only PDFs
    if file.content_type != "application/pdf":
        raise HTTPException(status_code=400, detail="Only PDF files are supported.")

    # Save uploaded PDF to temp file
    try:
        with NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
            shutil.copyfileobj(file.file, tmp)
            temp_path = tmp.name
    finally:
        file.file.close()

    try:
        result = process_pdf(temp_path)
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})

    return {"status": result}

class QuestionIn(BaseModel):
    question: str

@app.post("/ask")
def ask(question: QuestionIn):
    answer = ask_question(question.question)
    return {"answer": answer}
