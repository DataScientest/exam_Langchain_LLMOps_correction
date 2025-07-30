import re
from langchain_core.output_parsers import BaseOutputParser

class PythonCodeOutputParser(BaseOutputParser):
    """Extrait le bloc de code Python d’une réponse LLM."""
    
    def parse(self, text: str) -> str:
        # Bloc explicite ```python ... ```
        match = re.search(r"```python(.*?)```", text, re.DOTALL | re.IGNORECASE)
        if match:
            return match.group(1).strip()

        # Bloc générique ```
        match = re.search(r"```(.*?)```", text, re.DOTALL)
        if match:
            return match.group(1).strip()

        # Fallback : tout le texte
        return text.strip()
    
class ExplainOutputParser(BaseOutputParser):
    """Nettoie simplement le texte pour les tâches d'explication."""
    
    def parse(self, text: str) -> str:
        return text.strip()

class ParserFactory:
    """Fabrique d'output parsers selon la tâche demandée."""

    @staticmethod
    def get_parser(task: str):
        if task == "test":
            return PythonCodeOutputParser()
        elif task == "explain":
            return ExplainOutputParser()
        elif task == "refactor":
            return PythonCodeOutputParser()
        else:
            raise ValueError(f"Tâche inconnue : {task}")