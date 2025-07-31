from typing import List, Optional
from pydantic import BaseModel
from langchain.output_parsers import PydanticOutputParser

class CheckOutput(BaseModel):
    status: str  # "ok" ou "error"
    reason: Optional[str] = None

class RefactorOutput(BaseModel):
    refactored_code: str
    reason: str

class ExplainOutput(BaseModel):
    explanation: str

class TestOutput(BaseModel):
    tests: List[str]

# Parsers
check_parser = PydanticOutputParser(pydantic_object=CheckOutput)
refactor_parser = PydanticOutputParser(pydantic_object=RefactorOutput)
explain_parser = PydanticOutputParser(pydantic_object=ExplainOutput)
test_parser = PydanticOutputParser(pydantic_object=TestOutput)
