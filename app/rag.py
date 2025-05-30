import os
from dotenv import load_dotenv
from langchain.chains import RetrievalQA
from langchain_community.chat_models import ChatOpenAI
from app.vector_store import vector_store

# Load environment variables
load_dotenv()

# Ensure environment variable is set
LLM_MODEL = os.getenv("LLM_MODEL", "mistralai/Mixtral-8x7B-Instruct")
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

# Check if required values are set
if not OPENROUTER_API_KEY:
    raise ValueError("Missing OPENROUTER_API_KEY in environment variables.")

# Set up LLM using OpenRouter + Mixtral
llm = ChatOpenAI(
    temperature=0,
    openai_api_base="https://openrouter.ai/api/v1",
    openai_api_key=OPENROUTER_API_KEY,
    model=LLM_MODEL,
)

# Set up RetrievalQA chain
qa = RetrievalQA.from_chain_type(
    llm=llm,
    retriever=vector_store.as_retriever(),
    return_source_documents=False
)

# Ask question interface
def ask_question(question: str) -> str:
    return qa.run(question)
