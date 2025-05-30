from langchain_openai import OpenAIEmbeddings
from dotenv import load_dotenv
import os

# Load variables from .env file
load_dotenv()

# Fetch the key from environment variables
api_key = os.getenv("OPENAI_API_KEY")

# Initialize the embedder
embedder = OpenAIEmbeddings(openai_api_key=api_key)
