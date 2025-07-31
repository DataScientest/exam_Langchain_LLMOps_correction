# app/chains.py
import os
from dotenv import load_dotenv
from langchain_litellm import ChatLiteLLM
from langchain_core.exceptions import OutputParserException

from prompts import check_prompt, refactor_prompt, explain_prompt, test_prompt
from parser import (
    check_parser, refactor_parser, explain_parser, test_parser,
    CheckOutput, RefactorOutput, ExplainOutput, TestOutput
)
from logger import save_llm_interaction

def get_llm():
    load_dotenv()
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        raise ValueError("❌ GROQ_API_KEY manquant dans .env")
    return ChatLiteLLM(model="groq/llama-3.3-70b-versatile", api_key=api_key)

llm = get_llm()

class AnalyzeCodeChain:
    def __init__(self):
        self.llm = llm

    def invoke_chain(self, prompt, parser, inputs, step):
        prompt_text = prompt.format(**inputs)
        try:
            output = self.llm.invoke(prompt_text)
            result = parser.parse(output.content)  # ✅ essentiel
            save_llm_interaction(prompt_text, output.content, step)
            return result
        except OutputParserException as e:
            save_llm_interaction(prompt_text, e.llm_output or "[vide]", step + " ❌ PARSE FAIL")
            raise

    def invoke(self, function_code: str) -> dict:
        # Étape 1 — Analyse initiale
        analysis: CheckOutput = self.invoke_chain(check_prompt, check_parser, {"function_code": function_code}, "ANALYZE")

        if analysis.status == "ok":
            tests: TestOutput = self.invoke_chain(test_prompt, test_parser, {"function_code": function_code}, "TEST")
            return {
                "status": "ok",
                "function_code": function_code,
                "tests": tests.tests
            }

        # Étape 2 — Refactor
        refactor: RefactorOutput = self.invoke_chain(
            refactor_prompt, refactor_parser,
            {"function_code": function_code, "reason": analysis.reason}, "REFACTOR"
        )

        # Étape 3 — Explication
        explanation: ExplainOutput = self.invoke_chain(
            explain_prompt, explain_parser,
            {"function_code": refactor.refactored_code}, "EXPLAIN"
        )

        # Étape 4 — Re-analyse
        recheck: CheckOutput = self.invoke_chain(
            check_prompt, check_parser,
            {"function_code": refactor.refactored_code}, "RE-ANALYZE"
        )

        if recheck.status == "ok":
            tests: TestOutput = self.invoke_chain(
                test_prompt, test_parser,
                {"function_code": refactor.refactored_code}, "TEST_AFTER_REFACTOR"
            )
            return {
                "status": "refactored",
                "original_code": function_code,
                "refactored_code": refactor.refactored_code,
                "reason": refactor.reason,
                "explanation": explanation.explanation,
                "tests": tests.tests
            }

        return {
            "status": "refactored",
            "original_code": function_code,
            "refactored_code": refactor.refactored_code,
            "reason": refactor.reason,
            "explanation": explanation.explanation,
            "recheck": recheck.status,
            "recheck_reason": recheck.reason  # 
        }

