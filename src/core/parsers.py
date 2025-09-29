from pydantic import BaseModel, Field
from langchain_core.output_parsers import PydanticOutputParser

class AnalysisResult(BaseModel):
    is_optimal: bool = Field(..., description="True si le code est optimal")
    issues: list[str] = Field(..., description="Liste des problèmes détectés")
    suggestions: list[str] = Field(..., description="Liste des solutions proposées")

analysis_parser = PydanticOutputParser(pydantic_object=AnalysisResult)

class TestResult(BaseModel):
    unit_test: str = Field(..., description="Contenu du test unitaire en Python (pytest)")

test_parser = PydanticOutputParser(pydantic_object=TestResult)

class ExplainTestResult(BaseModel):
    explanation: str = Field(..., description="Explication pédagogique du test en français")

explain_test_parser = PydanticOutputParser(pydantic_object=ExplainTestResult)

