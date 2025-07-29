from langchain.memory import ConversationBufferWindowMemory

def get_memory(k, memory_key: str = "chat_history"):
    """
    Retourne une mémoire conversationnelle à fenêtre glissante.

    Seuls les k derniers échanges sont conservés, ce qui permet de contrôler
    la taille du contexte envoyé au modèle LLM.

    Paramètres :
    - k : nombre d’échanges à garder en mémoire
    - memory_key : clé utilisée dans les chaînes LangChain (par défaut "chat_history")
    """
    return ConversationBufferWindowMemory(
        memory_key=memory_key,
        return_messages=True,
        k=k
    )


