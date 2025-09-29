from langchain_core.chat_history import InMemoryChatMessageHistory

# === STORE GLOBAL (multi-user) ===
_store = {}

def get_session_history(session_id: str):
    """Retourne ou crée l'historique de session pour un utilisateur donné"""
    if session_id not in _store:
        _store[session_id] = InMemoryChatMessageHistory()
    return _store[session_id]

def get_user_history(session_id: str):
    """Récupère l'historique complet d'un utilisateur"""
    history = get_session_history(session_id).messages
    return [
        {"role": msg.type, "content": msg.content}
        for msg in history
    ]
