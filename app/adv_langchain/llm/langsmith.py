import os
from dotenv import load_dotenv
from langsmith import Client

load_dotenv()

os.environ["LANGCHAIN_TRACING_V2"] = "true"
os.environ["LANGCHAIN_PROJECT"] = os.getenv("LANGCHAIN_PROJECT", "unit-test-assistant")

api_key = os.getenv("LANGCHAIN_API_KEY")
if not api_key:
    raise ValueError("❌ LANGCHAIN_API_KEY manquant dans .env")
os.environ["LANGCHAIN_API_KEY"] = api_key

client = Client()

print(f"✅ LangSmith configuré pour le projet : {os.environ['LANGCHAIN_PROJECT']}")

def get_langsmith_client() -> Client:
    return client
