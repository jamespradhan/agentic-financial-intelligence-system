import os
from dotenv import load_dotenv
from google import genai
from schema import FinancialResponse

load_dotenv()

class FinancialAgent:
    def __init__(self):
        # Ensure you have GEMINI_API_KEY in your .env file
        self.client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
        # Using a model capable of complex reasoning
        self.model_id = "gemini-2.5-flash" 

    def analyze(self, pdf_path: str, user_query: str):
        # 1. Upload the file to Gemini's context window
        # In a real production app (like Bajaj wants), you might cache this file ID
        uploaded_file = self.client.files.upload(file=pdf_path)
        
        # 2. Agentic Prompt: Forces the model to "think" before answering
        prompt = f"""
        You are an expert Financial Analyst AI. Your task is to answer the user's question based strictly on the provided annual report.

        USER QUESTION: "{user_query}"

        INSTRUCTIONS:
        1. SEARCH: Scan the document for relevant tables, text, or figures.
        2. REASON: Break down your logic step-by-step. If you need to calculate growth (Year 2 - Year 1), show the math.
        3. VERIFY: Assign a confidence score. If the data is missing, state that clearly in the answer.
        4. CITE: list EVERY page number you used to construct the answer (e.g., [2, 5, 12]).

        Return the result strictly as JSON matching the FinancialResponse schema.
        """

        # 3. Call the model with Type Constraint (Structured Output)
        response = self.client.models.generate_content(
            model=self.model_id,
            contents=[uploaded_file, prompt],
            config={
                'response_mime_type': 'application/json',
                'response_schema': FinancialResponse,
            }
        )
        
        # 4. Validate and return the Pydantic object
        return FinancialResponse.model_validate_json(response.text)