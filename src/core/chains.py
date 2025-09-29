from .llm import llm
from prompts.prompts import analysis_prompt, test_prompt, explain_test_prompt, chat_prompt
from core.parsers import analysis_parser, test_parser, explain_test_parser

# 1. Analyse de code
analysis_chain = analysis_prompt | llm | analysis_parser

# 2. Génération de tests unitaires
test_chain = test_prompt | llm | test_parser

# 3. Explication du test unitaire (JSON strict)
explain_test_chain = explain_test_prompt | llm | explain_test_parser

chat_chain = chat_prompt | llm
