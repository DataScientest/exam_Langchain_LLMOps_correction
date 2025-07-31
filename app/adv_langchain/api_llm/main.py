from fastapi import FastAPI, HTTPException, Request
from pydantic import BaseModel
import jwt
from app.adv_langchain.chains import AnalyzeCodeChain

SECRET_KEY = "secret123"
ALGORITHM = "HS256"

app = FastAPI()

class CodeInput(BaseModel):
    token: str
    code: str

@app.post("/analyze_code")
def analyze_code(input: CodeInput):
    try:
        jwt.decode(input.token, SECRET_KEY, algorithms=[ALGORITHM])
    except jwt.InvalidTokenError:
        raise HTTPException(401, "Invalid token")

    result = AnalyzeCodeChain().invoke(input.code)
    return result
