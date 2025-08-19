from typing import Dict, Union

from langchain.prompts import PromptTemplate
from langchain.output_parsers import PydanticOutputParser
from langchain_core.output_parsers import StrOutputParser
from langchain.callbacks import get_openai_callback

from .llm import llm
from .prompts import (
    check_prompt, test_prompt, explain_cannot_prompt, explain_tests_prompt
)
from .parser import (
    check_parser, CheckOutput
)
from .logger import save_llm_interaction
from .memory import (
    get_memory, write_verdict_to_memory,
    log_user_code, log_tests, log_explanation
)


def make_chain(prompt_template: PromptTemplate, parser, input_vars: list):
    if isinstance(parser, PydanticOutputParser):
        prompt = PromptTemplate(
            template=prompt_template.template + "\n\n{format_instructions}",
            input_variables=input_vars,
            partial_variables={"format_instructions": parser.get_format_instructions()},
        )
    else:
        prompt = PromptTemplate(
            template=prompt_template.template,
            input_variables=input_vars,
        )
    chain = prompt | llm | parser
    chain._saved_prompt = prompt
    return chain


# === Chaînes spécialisées ===
check_chain = make_chain(check_prompt, check_parser, ["function_code"])
tests_chain = make_chain(test_prompt, StrOutputParser(), ["function_code"])
explain_cannot_chain = make_chain(
    explain_cannot_prompt, StrOutputParser(), ["function_code", "reason"]
)
explain_tests_chain = make_chain(
    explain_tests_prompt, StrOutputParser(), ["function_code", "tests_code"]
)


class AnalyzeCodeChain:
    """
    Orchestrateur:
    1) Analyse toujours le code avec check_chain.
    2) Si status=='ok': génère des tests (code brut) puis une explication (texte brut).
    3) Sinon: explique pourquoi on ne peut pas générer.
    Mémoire enrichie avec code, tests, explications et tokens.
    """

    def _safe_invoke(self, chain, inputs: Dict, step_name: str):
        prompt = getattr(chain, "_saved_prompt", None)
        try:
            prompt_text = prompt.format(**inputs) if prompt else "[Prompt manquant]"
        except Exception:
            prompt_text = "[Prompt inconnu — erreur dans inputs]"

        try:
            with get_openai_callback() as cb:
                result = chain.invoke(inputs)

            out_txt = (
                result.model_dump_json() if hasattr(result, "model_dump_json")
                else (result.model_dump() if hasattr(result, "model_dump") else str(result))
            )

            save_llm_interaction(prompt_text, out_txt, step=step_name)

            # 👉 Sauvegarde des stats tokens
            self.last_token_stats = f"[TOKENS] prompt={cb.prompt_tokens}, completion={cb.completion_tokens}, total={cb.total_tokens}, cost=${cb.total_cost:.5f}"
            save_llm_interaction(prompt_text, self.last_token_stats, step=f"{step_name} - TOKENS")

            return result
        except Exception as e:
            save_llm_interaction(prompt_text, str(e), step=f"{step_name} ❌ ERROR")
            raise

    def invoke(self, inputs: Union[str, Dict]) -> Dict:
        if isinstance(inputs, str):
            code = inputs
            explain_tests_flag = True
        elif isinstance(inputs, dict):
            code = inputs.get("function_code")
            if not isinstance(code, str) or not code.strip():
                raise ValueError("`function_code` doit être une chaîne non vide.")
            explain_tests_flag = bool(inputs.get("explain_tests", True))
        else:
            raise TypeError("`inputs` doit être une str (code) ou un dict.")

        mem = get_memory()

        # Toujours relancer l'analyse
        analysis: CheckOutput = self._safe_invoke(
            check_chain, {"function_code": code}, "ANALYZE"
        )
        write_verdict_to_memory(mem, analysis.status, analysis.reason)
        verdict = analysis

        if verdict.status == "ok":
            log_user_code(mem, code)

            tests_code = self._safe_invoke(tests_chain, {"function_code": code}, "GENERATE_TESTS")
            log_tests(mem, str(tests_code))

            result = {
                "status": "ok",
                "tests_code": str(tests_code),
            }

            if explain_tests_flag:
                explain_out = self._safe_invoke(
                    explain_tests_chain,
                    {"function_code": code, "tests_code": str(tests_code)},
                    "EXPLAIN_TESTS",
                )
                explanation_text = str(explain_out)
                result["tests_explanation"] = explanation_text
                log_explanation(mem, explanation_text)

            # 👉 Ajouter les stats de tokens
            result["token_stats"] = getattr(self, "last_token_stats", None)

            return result

        reason = verdict.reason or "Le modèle n'a pas fourni de raison."
        cannot_out = self._safe_invoke(
            explain_cannot_chain, {"function_code": code, "reason": reason}, "EXPLAIN_CANNOT"
        )
        explanation_text = str(cannot_out)
        log_explanation(mem, explanation_text)
        return {
            "status": "error",
            "reason": reason,
            "explanation": explanation_text,
            "token_stats": getattr(self, "last_token_stats", None)
        }
