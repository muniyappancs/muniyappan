import os
from dotenv import load_dotenv

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
load_dotenv(os.path.join(BASE_DIR, ".env"))

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")
BACKEND_URL = os.getenv("BACKEND_URL", "http://localhost:8000")

LOGO_PATH = os.path.join(BASE_DIR, "Image", "Logo.png")            # light background (docx/pdf)
WEB_LOGO_PATH = os.path.join(BASE_DIR, "Image", "inverseLogo.png")  # dark background (web UI)
FOOTER_TEXT = "LegalEase Inc. | contact@legalease.com | All Rights Reserved."
