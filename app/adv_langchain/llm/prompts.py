from langchain.prompts import PromptTemplate

# 1) Check (interne) — JSON court pour piloter la mémoire
check_prompt_text = """
Voici une fonction Python :

{function_code}

Analyse si elle est fonctionnelle (syntaxe valide + logique minimale cohérente).
Réponds UNIQUEMENT en JSON avec les clés EXACTES :
- status: "ok" ou "error"
- reason: (optionnelle) chaîne courte si status="error"
""".strip()

# 2) Génération de tests (pytest) — SORTIE = CODE PYTHON UNIQUEMENT
test_prompt_text = """
Écris un fichier de tests unitaires **pytest** pour la fonction ci-dessous.

Contraintes :
- Utilise exclusivement pytest (pas unittest).
- Fournis les imports nécessaires (par ex. `import pytest`).
- N’inclus PAS la fonction testée, uniquement les tests.
- Couvre cas nominaux, cas limites, et erreurs attendues si pertinent.

Réponds UNIQUEMENT par le code Python du fichier de tests (sans backticks, sans markdown, sans texte avant/après).

Fonction à tester :
{function_code}
""".strip()

# 3) Explication (quand on NE PEUT PAS générer) — SORTIE = TEXTE BRUT
explain_cannot_prompt_text = """
On ne peut pas générer de tests unitaires pour la fonction ci-dessous.

Raison détectée :
{reason}

Fonction :
{function_code}

Rédige une explication concise (3 à 6 phrases) expliquant pourquoi les tests ne peuvent pas être générés pour le moment et ce qu'il faut corriger d'abord.
Réponds UNIQUEMENT par du texte brut (pas de markdown, pas de JSON).
""".strip()

# 4) Explication des tests générés — SORTIE = TEXTE BRUT
explain_tests_prompt_text = """
Tu dois expliquer précisément ce que vérifient les tests unitaires (pytest) fournis ci-dessous.

Objectif de l'explication :
- Décrire les cas couverts (cas nominaux, cas limites, erreurs/Exceptions attendues).
- Expliquer l'intérêt de chaque groupe de tests (ex. propriétés vérifiées, invariants).
- Mentionner la présence éventuelle de paramétrisation (@pytest.mark.parametrize), de fixtures, de mocks.
- Signaler les hypothèses implicites (ex. types/contrats supposés) et les zones non couvertes, s'il y en a.

Contraintes de sortie :
- Réponds UNIQUEMENT avec du TEXTE BRUT (pas de markdown, pas de JSON).
- 5 à 10 phrases maximum, claires et concises.
- Ne recopie pas le code ci-dessous.

Fonction sous test :
{function_code}

Tests pytest fournis :
{tests_code}
""".strip()

# ---- PromptTemplates ----
check_prompt = PromptTemplate(
    template=check_prompt_text,
    input_variables=["function_code"]
)

test_prompt = PromptTemplate(
    template=test_prompt_text,
    input_variables=["function_code"]
)

explain_tests_prompt = PromptTemplate(
    template=explain_tests_prompt_text,
    input_variables=["function_code", "tests_code"]
)

explain_cannot_prompt = PromptTemplate(
    template=explain_cannot_prompt_text,
    input_variables=["function_code", "reason"]
)
