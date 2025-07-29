from app.src.chains import build_test_chain
from app.src.logger import save_memory_to_file
from app.src.prompts import chat_prompt

function_code = '''
def multiply(a, b):
    """
    Multiplie deux entiers.
    >>> multiply(2, 4)
    8
    """
    return a * b
'''

input_data = {"function_code": function_code}

# Récupère la chaîne (avec mémoire intégrée)
chain = build_test_chain()

output = chain.invoke(input_data)

# Formatage du prompt injecté pour le log
messages = chat_prompt.format_messages(**input_data)
formatted_prompt = "\n\n".join([f"{m.type}: {m.content}" for m in messages])

# Logging propre avec mémoire + comptage de tokens
save_memory_to_file(
    memory=chain.memory,
    prompt_text=formatted_prompt,
    output_text=output["text"]
)

