from typing import Optional, Tuple
from langchain.memory import ConversationBufferMemory
from pydantic import BaseModel

# --------- Modèles Pydantic (alignés avec parser.py) ----------
class CheckOutput(BaseModel):
    status: str  # "ok" | "error"
    reason: Optional[str] = None

# --------- Mémoire globale unique ----------
_GLOBAL_MEMORY: ConversationBufferMemory = ConversationBufferMemory(
    memory_key="chat_history", return_messages=True
)

# Petit espace clé-valeur pour stocker le dernier verdict
_LAST_VERDICT: Optional[CheckOutput] = None

def get_memory() -> ConversationBufferMemory:
    return _GLOBAL_MEMORY

def write_verdict_to_memory(mem: ConversationBufferMemory, status: str, reason: Optional[str]):
    global _LAST_VERDICT
    _LAST_VERDICT = CheckOutput(status=status, reason=reason)
    # On peut aussi pousser un message "système" dans l'historique (optionnel)
    mem.chat_memory.add_ai_message(f"[verdict] status={status} reason={reason or ''}")

def read_last_verdict_from_memory(mem: ConversationBufferMemory) -> Optional[CheckOutput]:
    return _LAST_VERDICT

def log_user_code(mem, code: str):
    mem.chat_memory.add_user_message(f"[CODE]\n{code}")

def log_tests(mem, tests: str):
    mem.chat_memory.add_ai_message(f"[TESTS]\n{tests}")

def log_explanation(mem, explanation: str):
    mem.chat_memory.add_ai_message(f"[EXPLANATION]\n{explanation}")


def clear():
    """Efface la mémoire + le dernier verdict."""
    global _LAST_VERDICT
    _LAST_VERDICT = None
    _GLOBAL_MEMORY.clear()
