from fastapi import FastAPI, HTTPException, Header
from pydantic import BaseModel
from datetime import datetime, timedelta
import jwt
from jwt import PyJWTError

# === CONFIG JWT ===
SECRET_KEY = "supersecretkey"  
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

# Base utilisateurs en mémoire
fake_users_db = {}

app = FastAPI(title="API Auth", version="3.1")


# === MODELES ===
class UserSignup(BaseModel):
    username: str
    password: str

class User(BaseModel):
    username: str

class Token(BaseModel):
    access_token: str
    token_type: str


# === UTILS ===
def create_access_token(username: str):
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    payload = {"sub": username, "exp": expire}
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

def decode_token(token: str) -> str:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload.get("sub")
    except PyJWTError:
        raise HTTPException(status_code=401, detail="Token invalide ou expiré")


# === ENDPOINTS ===
@app.post("/signup", response_model=User)
def signup(user: UserSignup):
    if user.username in fake_users_db:
        raise HTTPException(status_code=400, detail="Nom d'utilisateur déjà pris")
    fake_users_db[user.username] = {"username": user.username, "password": user.password}
    return User(username=user.username)


@app.post("/login", response_model=Token)
def login(user: UserSignup):
    stored_user = fake_users_db.get(user.username)
    if not stored_user or stored_user["password"] != user.password:
        raise HTTPException(status_code=401, detail="Nom d'utilisateur ou mot de passe incorrect")
    token = create_access_token(user.username)
    return {"access_token": token, "token_type": "bearer"}


@app.get("/me", response_model=User)
def me(authorization: str = Header(...)):
    if not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="En-tête Authorization invalide")
    token = authorization.split(" ")[1]
    username = decode_token(token)
    return User(username=username)
