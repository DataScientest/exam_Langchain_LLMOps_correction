from langchain_litellm import ChatLiteLLM
import os
from dotenv import load_dotenv

def get_llm():
    load_dotenv()
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        raise ValueError("❌ GROQ_API_KEY manquant dans .env")
    model = os.getenv("LITELLM_MODEL", "groq/llama-3.3-70b-versatile")
    return ChatLiteLLM(model=model, api_key=api_key)

llm = get_llm()