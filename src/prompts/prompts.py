from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

analysis_prompt = ChatPromptTemplate.from_messages([
    ("system", "Tu es un expert en Python et en bonnes pratiques de programmation."),
    ("human", 
     "Analyse le code suivant et dis-moi s'il est optimal.\n\n"
     "Code :\n{input}\n\n"
     "Réponds uniquement avec un JSON valide sous la forme :\n"
     "{{\"is_optimal\": true/false, \"issues\": [liste des problèmes ou []], \"suggestions\": [liste des solutions ou []]}}\n\n"
     "{format_instructions}")
])

test_prompt = ChatPromptTemplate.from_messages([
    ("system", "Tu es un générateur de tests unitaires en Python."),
    ("human", 
     "Écris un test unitaire en pytest pour le code suivant.\n\n"
     "Code :\n{input}\n\n"
     "Réponds uniquement avec un JSON valide sous la forme :\n"
     "{{\"unit_test\": \"contenu du test en code Python\"}}\n\n"
     "{format_instructions}")
])

# === Explication du test unitaire ===
explain_test_prompt = ChatPromptTemplate.from_messages([
    ("system", "Tu es un professeur d’informatique. Ton rôle est d’expliquer les tests unitaires en Python."),
    ("human",
     "Explique clairement le test unitaire suivant :\n\n"
     "```python\n{input}\n```\n\n"
     "Réponds uniquement avec un JSON valide sous la forme :\n"
     "{{\"explanation\": \"explication détaillée du test en français\"}}\n\n"
     "{format_instructions}")
])

chat_prompt = ChatPromptTemplate.from_messages([
    ("system", "Tu es un assistant utile qui discute librement avec l’utilisateur."),
    MessagesPlaceholder(variable_name="messages"),
    ("human", "{input}")
])