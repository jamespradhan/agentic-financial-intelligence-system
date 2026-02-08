from pydantic import BaseModel, Field
from typing import List

class ReasoningStep(BaseModel):
    step_number: int = Field(..., description="The sequence number.")
    logic: str = Field(..., description="The logic used (e.g., 'Combined mission statement from Page 2 with product list on Page 10').")

class FinancialResponse(BaseModel):
    answer: str = Field(..., description="The comprehensive answer.")
    reasoning_path: List[ReasoningStep] = Field(..., description="Step-by-step logic.")
    confidence_score: float = Field(..., description="Confidence score (0.0-1.0).")
    source_pages: List[int] = Field(..., description="A list of ALL page numbers where relevant information was found.")