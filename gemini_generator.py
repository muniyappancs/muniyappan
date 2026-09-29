import os
import sys

import google.generativeai as genai

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import GEMINI_API_KEY, GEMINI_MODEL  # noqa: E402


class GeminiDocumentGenerator:
    """Builds a structured prompt and asks Gemini to draft the legal document."""

    def __init__(self, model_name: str = GEMINI_MODEL):
        if not GEMINI_API_KEY:
            raise RuntimeError("GEMINI_API_KEY is missing. Add it to the .env file.")
        genai.configure(api_key=GEMINI_API_KEY)
        self.model = genai.GenerativeModel(model_name)

    def generate_document(self, document_type, parties, terms, dates):
        prompt = (
            f"Generate a comprehensive legal document titled '{document_type}'.\n"
            f"Involved parties: {parties}\n"
            f"Effective Date: {dates}\n"
            f"Terms and conditions (semicolon separated): {terms}\n"
            "Ensure formal legal structure with multiple numbered sections and legal clauses. "
            "Write section headings on their own line, like '1. Services:'. "
            "Use plain text only (no markdown symbols like ** or #). "
            "End with a signature block for every party."
        )
        response = self.model.generate_content(prompt)
        return response.text
