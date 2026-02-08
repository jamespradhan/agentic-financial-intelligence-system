from pydantic import BaseModel, Field
from typing import List

class ReasoningStep(BaseModel):
    step_number: int = Field(..., description="The sequence number of this reasoning step.")
    logic: str = Field(..., description="The logical deduction made in this step (e.g., 'Found total revenue in Table 3').")

class FinancialResponse(BaseModel):
    answer: str = Field(..., description="The direct answer to the user's financial question.")
    reasoning_path: List[ReasoningStep] = Field(..., description="The step-by-step logic used to derive the answer.")
    confidence_score: float = Field(..., description="A score from 0.0 to 1.0 indicating confidence in the result.")
    source_pages: List[int] = Field(..., description="A list of ALL page numbers where relevant information was found.")