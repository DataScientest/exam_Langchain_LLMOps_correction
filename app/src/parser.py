import re

def extract_code_block(text: str) -> str:
    """
    Extrait un bloc de code Python depuis un texte retourné par un LLM.

    3 cas traités :
    1. Bloc Markdown explicite ```python ... ```
    2. Bloc Markdown générique ``` ... ```
    3. Texte brut contenant du code (détection par indentation ou 'def test_')
    """

    # Cas 1 : bloc ```python ... ```
    match = re.search(r"```python(.*?)```", text, re.DOTALL)
    if match:
        return match.group(1).strip()

    # Cas 2 : bloc ``` ... ```
    match = re.search(r"```(.*?)```", text, re.DOTALL)
    if match:
        return match.group(1).strip()

    # Cas 3 : texte brut → on essaie d’extraire le bloc de test
    # Cherche une fonction commençant par "def test_"
    match = re.search(r"(def test_[\s\S]+)", text)
    if match:
        code = match.group(1)
        # On nettoie tout ce qui suit un double saut de ligne après le test
        code = re.split(r"\n\s*\n", code)[0]
        return code.strip()

    # Cas ultime : retour brut
    return text.strip()
