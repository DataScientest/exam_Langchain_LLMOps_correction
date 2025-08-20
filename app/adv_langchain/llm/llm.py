from langchain_litellm import ChatLiteLLM
from .langsmith import get_langsmith_client
import os

def get_llm():
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        raise ValueError("❌ GROQ_API_KEY manquant dans .env")
    model = os.getenv("LITELLM_MODEL", "groq/llama-3.3-70b-versatile")

    client = get_langsmith_client()
    print("LangSmith client actif:", client)

    return ChatLiteLLM(model=model, api_key=api_key)

llm = get_llm()
