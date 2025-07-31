# app/prompts.py
from langchain.prompts import PromptTemplate
from parser import check_parser, refactor_parser, explain_parser, test_parser

check_prompt = PromptTemplate(
    template="""
Voici une fonction Python :

{function_code}

Tu dois analyser si elle est fonctionnelle.

Réponds uniquement en JSON : {{ "status": "ok" }} ou {{ "status": "error", "reason": "..." }}

{format_instructions}
""".strip(),
    input_variables=["function_code"],
    partial_variables={"format_instructions": check_parser.get_format_instructions()}
)

refactor_prompt = PromptTemplate(
    template="""
Corrige cette fonction Python pour qu'elle soit fonctionnelle.

Raison : {reason}

{function_code}

Réponds uniquement avec un JSON contenant "refactored_code" et "reason".

{format_instructions}
""".strip(),
    input_variables=["function_code", "reason"],
    partial_variables={"format_instructions": refactor_parser.get_format_instructions()}
)

explain_prompt = PromptTemplate(
    template="""
Explique ce que fait cette fonction Python :

{function_code}

Réponds uniquement avec un JSON contenant "explanation".

{format_instructions}
""".strip(),
    input_variables=["function_code"],
    partial_variables={"format_instructions": explain_parser.get_format_instructions()}
)

test_prompt = PromptTemplate(
    template="""
Écris des tests unittest pour cette fonction :

{function_code}

Réponds uniquement avec un JSON : {{ "tests": ["..."] }}

{format_instructions}
""".strip(),
    input_variables=["function_code"],
    partial_variables={"format_instructions": test_parser.get_format_instructions()}
)
