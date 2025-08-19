from fastapi import FastAPI, HTTPException, Form
from pydantic import BaseModel
import os

from app.basic_langchain.chains import build_chain

app = FastAPI()

# Stockage temporaire de la clé GROQ
api_key_storage = {"groq_api_key": None}

# ----------- Schemas -----------

class FunctionInput(BaseModel):
    function_code: str

# ----------- Endpoints -----------

@app.get("/health")
def health_check():
    """Vérifie que l'API fonctionne."""
    return {"status": "✅ API opérationnelle"}

@app.post("/set-api-key")
def set_api_key(api_key: str = Form(...)):
    api_key_storage["groq_api_key"] = api_key
    return {"message": "✅ Clé GROQ enregistrée en mémoire"}

@app.post("/generate/test")
def generate_test(body: FunctionInput):
    """Génère des tests unitaires à partir d'une fonction Python."""
    return run_chain_for_task("test", body.function_code)

@app.post("/generate/explain")
def generate_explanation(body: FunctionInput):
    """Explique le fonctionnement d'une fonction Python."""
    return run_chain_for_task("explain", body.function_code)

@app.post("/generate/refactor")
def generate_refactor(body: FunctionInput):
    """Propose une version refactorisée de la fonction Python."""
    return run_chain_for_task("refactor", body.function_code)

# ----------- Fonction utilitaire -----------

def run_chain_for_task(task: str, function_code: str):
    api_key = api_key_storage.get("groq_api_key")
    if not api_key:
        raise HTTPException(status_code=400, detail="Clé API non définie. Utilise d'abord /set_api_key.")
    
    os.environ["GROQ_API_KEY"] = api_key

    try:
        chain, llm = build_chain(task=task)
        input_data = {"function_code": function_code}
        output = chain.invoke(input_data)
        return {"result": output["text"]}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
