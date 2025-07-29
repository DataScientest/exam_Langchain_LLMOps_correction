import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.chains import LLMChain
from app.src.prompts import chat_prompt
from app.src.memory import get_memory

def build_test_chain():
    load_dotenv()
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        raise ValueError("❌ GOOGLE_API_KEY manquant dans .env")

    # Instanciation du modèle Gemini
    llm = ChatGoogleGenerativeAI(
        model="models/gemini-1.5-flash-latest",
        google_api_key=api_key,
        temperature=0.5,
        top_p=0.9
    )

    # Activation de la mémoire (conversationnelle, glissante)
    memory = get_memory(k=5)  # glisse sur les 5 derniers échanges

    # Chaîne complète avec mémoire
    chain = LLMChain(
        llm=llm,
        prompt=chat_prompt,
        memory=memory
    )

    return chain
