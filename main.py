from app.src.chains import build_chain
from app.src.logger import save_memory_to_file
from app.src.prompt import PromptFactory

# Exemple de fonction Python à traiter
function_code = '''
def multiply(a, b):
    return a * b
'''

task = "explain"  

chain, llm = build_chain(task)

input_data = {"function_code": function_code}

output = chain.invoke(input_data)

messages = PromptFactory.get_prompt(task).format_messages(**input_data)
formatted_prompt = "\n\n".join([f"{m.type}: {m.content}" for m in messages])

save_memory_to_file(
    memory=chain.memory,
    prompt_text=formatted_prompt,
    output_text=output["text"],
    llm=llm
)
