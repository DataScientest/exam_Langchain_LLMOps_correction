from typing import Optional
from pydantic import BaseModel, Field
from langchain.output_parsers import PydanticOutputParser

# --- Modèles Pydantic ---
class CheckOutput(BaseModel):
    status: str = Field(description="Statut d'analyse : 'ok' ou 'error'")
    reason: Optional[str] = Field(description="Explication courte si status='error'")

# --- Parsers ---
check_parser = PydanticOutputParser(pydantic_object=CheckOutput)

