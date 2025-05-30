import os
from dotenv import load_dotenv

load_dotenv()

def verify_env():
    keys = ["OPENAI_API_KEY", "OPENROUTER_API_KEY", "LLM_MODEL"]
    for key in keys:
        value = os.getenv(key)
        if value:
            print(f"{key} is set.")
        else:
            print(f"{key} is NOT set!")

if __name__ == "__main__":
    print("Verifying environment variables...")
    verify_env()
    print("Environment verification done.")
