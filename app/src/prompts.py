from langchain.prompts import ChatPromptTemplate

chat_prompt = ChatPromptTemplate.from_messages([
    ("system", 
     "Tu es un assistant Python expert en tests unitaires.\n"
     "Tu écris des tests au format pytest à partir du code source fourni."),
    
    ("user",
     "Voici une fonction Python :\n"
     "```python\n{function_code}\n```\n"
     "Génère un test unitaire pytest correspondant.\n"
     "Fournis le code du test dans un bloc ```python```, avec commentaire et explication.")
])
