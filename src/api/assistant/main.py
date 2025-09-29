from fastapi import FastAPI, HTTPException, Header, Depends
from pydantic import BaseModel
from core.chains import analysis_chain, test_chain, explain_test_chain, chat_chain
from core.parsers import analysis_parser, test_parser, explain_test_parser
from api.authentification.auth import decode_token, User
from memory.memory import get_session_history, get_user_history

from langchain_core.runnables.history import RunnableWithMessageHistory

app = FastAPI(title="Assistant Test Unitaire", version="3.1")

# === MODELES ===
class CodeInput(BaseModel):
    code: str

class TestInput(BaseModel):
    unit_test: str

class ChatInput(BaseModel):
    input: str


# === AUTH ===
def get_current_user(authorization: str = Header(...)) -> User:
    if not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="En-tête Authorization invalide")
    try:
        token = authorization.split(" ")[1]
        username = decode_token(token)
        return User(username=username)
    except Exception:
        raise HTTPException(status_code=401, detail="Token invalide ou expiré")


# === ENDPOINTS ===

@app.post("/analyze")
def analyze_code(payload: CodeInput, user: User = Depends(get_current_user)):
    try:
        chain_with_memory = RunnableWithMessageHistory(
            analysis_chain,
            get_session_history,
            input_messages_key="input",
            history_messages_key="messages",
        )
        config = {"configurable": {"session_id": user.username}}
        result = chain_with_memory.invoke(
            {"input": payload.code, "format_instructions": analysis_parser.get_format_instructions()},
            config=config
        )

        session = get_session_history(user.username)
        session.add_ai_message(str(result.dict()))

        return result.dict()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur analyse: {e}")


@app.post("/generate_test")
def generate_test(payload: CodeInput, user: User = Depends(get_current_user)):
    try:
        chain_with_memory = RunnableWithMessageHistory(
            test_chain,
            get_session_history,
            input_messages_key="input",
            history_messages_key="messages",
        )
        config = {"configurable": {"session_id": user.username}}
        test = chain_with_memory.invoke(
            {"input": payload.code, "format_instructions": test_parser.get_format_instructions()},
            config=config
        )

        session = get_session_history(user.username)
        session.add_ai_message(str(test.dict()))

        return test.dict()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur génération test: {e}")



@app.post("/explain_test")
def explain_test(payload: TestInput, user: User = Depends(get_current_user)):
    try:
        chain_with_memory = RunnableWithMessageHistory(
            explain_test_chain,
            get_session_history,
            input_messages_key="input",
            history_messages_key="messages",
        )
        config = {"configurable": {"session_id": user.username}}
        explanation = chain_with_memory.invoke(
            {"input": payload.unit_test, "format_instructions": explain_test_parser.get_format_instructions()},
            config=config
        )

        session = get_session_history(user.username)
        session.add_ai_message(str(explanation.dict()))

        return explanation.dict()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur explication: {e}")


@app.post("/full_pipeline")
def full_pipeline(payload: CodeInput, user: User = Depends(get_current_user)):
    try:
        config = {"configurable": {"session_id": user.username}}

        analysis_chain_with_memory = RunnableWithMessageHistory(
            analysis_chain,
            get_session_history,
            input_messages_key="input",
            history_messages_key="messages",
        )
        analysis = analysis_chain_with_memory.invoke(
            {"input": payload.code, "format_instructions": analysis_parser.get_format_instructions()},
            config=config
        )

        if not analysis.is_optimal:
            session = get_session_history(user.username)
            session.add_ai_message(str(analysis.dict()))
            return {
                "analysis": analysis.dict(),
                "error": "Code non optimal",
                "issues": analysis.issues,
                "suggestions": analysis.suggestions,
            }

        test_chain_with_memory = RunnableWithMessageHistory(
            test_chain,
            get_session_history,
            input_messages_key="input",
            history_messages_key="messages",
        )
        test = test_chain_with_memory.invoke(
            {"input": payload.code, "format_instructions": test_parser.get_format_instructions()},
            config=config
        )

        explain_chain_with_memory = RunnableWithMessageHistory(
            explain_test_chain,
            get_session_history,
            input_messages_key="input",
            history_messages_key="messages",
        )
        explanation = explain_chain_with_memory.invoke(
            {"input": test.unit_test, "format_instructions": explain_test_parser.get_format_instructions()},
            config=config
        )

        session = get_session_history(user.username)
        session.add_ai_message(str(analysis.dict()))
        session.add_ai_message(str(test.dict()))
        session.add_ai_message(str(explanation.dict()))

        return {
            "analysis": analysis.dict(),
            "test": test.dict(),
            "explanation": explanation.dict(),
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur pipeline: {e}")

@app.post("/chat")
def chat(payload: ChatInput, user: User = Depends(get_current_user)):
    try:
        chain_with_memory = RunnableWithMessageHistory(
            chat_chain,
            get_session_history,
            input_messages_key="input",
            history_messages_key="messages",
        )
        config = {"configurable": {"session_id": user.username}}
        result = chain_with_memory.invoke({"input": payload.input}, config=config)
        return {"response": result.content}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur conversation: {e}")

@app.get("/history")
def get_history(user: User = Depends(get_current_user)):
    """Retourne l'historique complet de la session de l'utilisateur"""
    try:
        return {"history": get_user_history(user.username)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur récupération historique: {e}")

