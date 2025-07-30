from datetime import datetime
from pathlib import Path

def save_memory_to_file(memory, prompt_text: str, output_text: str, llm=None):
    # === Création du dossier logs ===
    logs_dir = Path("logs")
    logs_dir.mkdir(exist_ok=True)
    log_file = logs_dir / "memory.log"

    # === Timestamp actuel ===
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # === Récupération de l'historique de la mémoire ===
    if memory is not None:
        variables = memory.load_memory_variables({})
        messages = variables.get("chat_history", [])
        chat_history = "\n".join([f"{m.type.upper()} — {m.content}" for m in messages])
    else:
        chat_history = "[Aucune mémoire]"

    # === Format du log ===
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
{prompt_text}

=========
OUTPUT:
=========
{output_text}

----------------
""".strip()

    # === Écriture dans le fichier ===
    with open(log_file, "a", encoding="utf-8") as f:
        f.write(log_content + "\n\n")

    print(f"✅ Mémoire + prompt + tokens enregistrés dans {log_file}")
