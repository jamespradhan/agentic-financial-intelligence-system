import os
import time
from dotenv import load_dotenv
from google import genai
from schema import FinancialResponse

load_dotenv()

class FinancialAgent:
    def __init__(self):
        # Ensure GEMINI_API_KEY is in your .env file
        self.client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
        
        # Using Flash for low latency, or use "gemini-1.5-pro" for complex reasoning
        self.model_id = "gemini-2.5-flash" 

    def upload_file(self, file_path: str):
        """
        Uploads the file ONCE and waits for processing to complete.
        Returns the remote file object to be cached by the app.
        """
        print(f"Uploading {file_path}...")
        file_obj = self.client.files.upload(file=file_path)

        # Enterprise Logic: Poll for 'ACTIVE' state to prevent crashing on large files
        while file_obj.state.name == "PROCESSING":
            print("Processing PDF...")
            time.sleep(1)
            file_obj = self.client.files.get(name=file_obj.name)
            
        if file_obj.state.name != "ACTIVE":
            raise Exception(f"File upload failed with state: {file_obj.state.name}")
            
        print(f"File {file_obj.name} is ready for analysis.")
        return file_obj

    def analyze(self, remote_file_obj, user_query: str):
        """
        Uses the CACHED file object to answer questions instantly.
        """
        # Agentic Prompt: Forces the model to synthesize data from multiple pages
        prompt = f"""
        You are an expert Financial Analyst AI.
        
        USER QUESTION: "{user_query}"
        
        INSTRUCTIONS:
        1. SEARCH: Scan the ENTIRE document. Information might be split across multiple sections.
        2. SYNTHESIZE: If the answer requires combining text from different pages, merge them into a single summary.
        3. REASON: Break down your logic step-by-step in 'reasoning_path'.
        4. CITE: In 'source_pages', list EVERY page number used (e.g., [2, 5, 12]).
        
        Return the result strictly as JSON matching the FinancialResponse schema.
        """

        response = self.client.models.generate_content(
            model=self.model_id,
            contents=[remote_file_obj, prompt],
            config={
                'response_mime_type': 'application/json',
                'response_schema': FinancialResponse,
            }
        )
        
        return FinancialResponse.model_validate_json(response.text)