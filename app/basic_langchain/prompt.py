from langchain.prompts import ChatPromptTemplate

class PromptFactory:
    """Fabrique de prompts pour diverses tâches liées au code Python."""

    @staticmethod
    def test_unitaire_prompt():
        return ChatPromptTemplate.from_messages([
            ("system", "Tu es un assistant Python expert en tests unitaires."),
            ("user",
             "Voici une fonction Python :\n"
             "```python\n{function_code}\n```\n"
             "Génère un test unitaire pytest correspondant.\n"
             "Fournis le code du test dans un bloc ```python```.")
        ])

    @staticmethod
    def explain_prompt():
        return ChatPromptTemplate.from_messages([
            ("system", "Tu es un assistant Python pédagogue qui explique du code à des débutants."),
            ("user",
             "Voici une fonction Python :\n"
            "```python\n{function_code}\n```\n"
            "Explique étape par étape ce que fait cette fonction de façon simple et claire.")
        ])

    @staticmethod
    def refactor_prompt():
        return ChatPromptTemplate.from_messages([
            ("system", "Tu es un assistant Python expert en refactorisation."),
            ("user",
             "Voici une fonction à améliorer :\n"
             "```python\n{function_code}\n```\n"
             "Refactore-la pour la rendre plus lisible, tout en conservant la logique.")
        ])

    @staticmethod
    def get_prompt(task: str):
        """
        Retourne le PromptTemplate approprié pour une tâche donnée.
        """
        prompt_map = {
            "test": PromptFactory.test_unitaire_prompt(),
            "explain": PromptFactory.explain_prompt(),
            "refactor": PromptFactory.refactor_prompt(),
        }

        if task not in prompt_map:
            raise ValueError(f"Tâche inconnue : {task}")

        return prompt_map[task]