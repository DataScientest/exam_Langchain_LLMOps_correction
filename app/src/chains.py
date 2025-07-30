import os
from dotenv import load_dotenv
from langchain_litellm import ChatLiteLLM
from langchain.chains import LLMChain
from app.src.prompt import PromptFactory
from app.src.parser import ParserFactory
from app.src.parser import PythonCodeOutputParser, ExplainOutputParser
from app.src.memory import BufferMemory

def build_chain(task: str = "test"):

    load_dotenv()
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        raise ValueError("❌ GROQ_API_KEY manquant dans .env")

    llm = ChatLiteLLM(
        model="groq/llama-3.3-70b-versatile",
        api_key=api_key,
    )

    output_parser = PythonCodeOutputParser()

    prompt = PromptFactory.get_prompt(task)
    output_parser = ParserFactory.get_parser(task)

    # Chaîne de base sans mémoire (pipe)
    chain = LLMChain(
        llm=llm,
        prompt=prompt,
        memory=BufferMemory(memory_key="chat_history", return_messages=True),
        output_parser=output_parser
    )

    return chain, llm
