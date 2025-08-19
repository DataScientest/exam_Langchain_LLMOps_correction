# app/adv_langchain/api_llm/main.py
from fastapi import FastAPI, HTTPException, Query
from fastapi.responses import JSONResponse
from pydantic import BaseModel
import jwt

from llm.chains import AnalyzeCodeChain
from llm.memory import get_memory, read_last_verdict_from_memory

SECRET_KEY = "secret123"
ALGORITHM = "HS256"

app = FastAPI()
chain = AnalyzeCodeChain()

class CodeInput(BaseModel):
    token: str
    code: str
    force_recheck: bool = False
    explain_tests: bool = True

def _auth_or_401(token: str):
    try:
        jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/analyze_code")
def analyze_code(body: CodeInput):
    _auth_or_401(body.token)
    try:
        result = chain.invoke({
            "function_code": body.code,
            "force_recheck": body.force_recheck,
            "explain_tests": body.explain_tests,
        })
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"detail": f"Chain error: {type(e).__name__}: {str(e)[:400]}"},
        )
    return JSONResponse(status_code=200, content=result)

@app.get("/memory")
def get_memory_state(token: str = Query(..., description="JWT token")):
    _auth_or_401(token)
    mem = get_memory()
    # Historique conversationnel
    messages = getattr(mem.chat_memory, "messages", [])
    msgs = []
    for m in messages:
        role = getattr(m, "type", None) or getattr(m, "role", None) or m.__class__.__name__.lower()
        content = getattr(m, "content", "")
        msgs.append({"role": role, "content": content})
    # Dernier verdict
    v = read_last_verdict_from_memory(mem)
    verdict = v.model_dump() if v else None
    return JSONResponse(status_code=200, content={
        "size": len(msgs),
        "verdict": verdict,
        "messages": msgs
    })

@app.delete("/memory")
def clear_memory(token: str = Query(..., description="JWT token")):
    _auth_or_401(token)
    mem = get_memory()
    mem.clear()
    return JSONResponse(status_code=200, content={"status": "cleared"})
