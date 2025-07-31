from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import jwt, time

SECRET_KEY = "secret123"
ALGORITHM = "HS256"

app = FastAPI()

fake_users = {
    "admin": "admin123",
    "user": "user123"
}

class LoginInput(BaseModel):
    username: str
    password: str

@app.post("/login")
def login(data: LoginInput):
    if data.username in fake_users and fake_users[data.username] == data.password:
        payload = {"sub": data.username, "exp": time.time() + 3600}
        token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
        return {"access_token": token}
    raise HTTPException(401, "Invalid credentials")

@app.get("/verify")
def verify_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return {"user": payload["sub"]}
    except jwt.ExpiredSignatureError:
        raise HTTPException(401, "Token expired")
    except jwt.InvalidTokenError:
        raise HTTPException(401, "Invalid token")
