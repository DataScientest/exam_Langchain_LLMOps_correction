import os
from datetime import datetime
from pathlib import Path

import tiktoken

# === Utilitaire pour compter les tokens (estimation)
def count_tokens(text: str, model: str = "gpt-3.5-turbo") -> int:
    try:
        enc = tiktoken.encoding_for_model(model)
        return len(enc.encode(text))
    except Exception:
        return -1

# === Fonction principale de logging
def save_memory_to_file(memory, prompt_text: str, output_text: str, model_for_token_estimate="gpt-3.5-turbo"):
    # Dossier log
    logs_dir = Path("logs")
    logs_dir.mkdir(exist_ok=True)

    # Fichier log
    log_file = logs_dir / "memory.log"

    # Timestamp
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Historique de la mémoire (si activée)
    chat_history = ""
    if memory is not None:
        try:
            variables = memory.load_memory_variables({})
            chat_history = "\n".join([f"{msg.type.upper()} — {msg.content}" for msg in variables.get("chat_history", [])])
        except Exception:
            chat_history = "[Erreur lors du chargement de la mémoire]"
    else:
        chat_history = "[Aucune mémoire]"

    # Comptage des tokens
    prompt_tokens = count_tokens(prompt_text, model=model_for_token_estimate)
    output_tokens = count_tokens(output_text, model=model_for_token_estimate)

    # Log formaté
    log_content = f"""
--------------------------

TIMESTAMP : {timestamp}

================
MEMOIRE DU LLM : 
================
{chat_history}

=============
PROMPT : 
=============
[TOKEN COUNT = {prompt_tokens if prompt_tokens != -1 else "N/A"}]
{prompt_text}

=========
OUTPUT:
=========
[TOKEN COUNT = {output_tokens if output_tokens != -1 else "N/A"}]
{output_text}
----------------
""".strip()

    # Écriture dans le fichier
    with open(log_file, "a", encoding="utf-8") as f:
        f.write(log_content + "\n\n")
    
    print(f"✅ Mémoire + prompt + tokens enregistrés dans {log_file}")
