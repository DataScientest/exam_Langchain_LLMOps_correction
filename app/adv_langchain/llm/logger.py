from datetime import datetime
from pathlib import Path

def save_llm_interaction(prompt_text: str, output_text: str, step: str = "UNKNOWN"):
    log_file = Path("logs/llm_outputs.log")
    log_file.parent.mkdir(exist_ok=True)

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    log_entry = f"""
--------------------------
⏱️  {timestamp}
🔁  Étape : {step}

== PROMPT ==
{prompt_text.strip()}

== OUTPUT ==
{output_text.strip()}
--------------------------
""".strip()

    with open(log_file, "a", encoding="utf-8") as f:
        f.write(log_entry + "\n\n")

    print(f"✅ Log enregistré dans {log_file}")
