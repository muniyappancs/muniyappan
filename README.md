# LegalEase - AI-Powered Legal Document Generator

FastAPI backend + Streamlit frontend + Google Gemini. Generates legal documents
(contracts, NDAs, leases...) with editable preview and export to .txt / .docx / .pdf.

## Setup
```bash
python -m venv venv
venv\Scripts\activate          # Windows   (Mac/Linux: source venv/bin/activate)
pip install -r requirements.txt
```
Edit `.env` and paste your key (get one at https://aistudio.google.com/app/apikey):
```
GEMINI_API_KEY=xxxx
GEMINI_MODEL=gemini-2.5-flash
```

## Run (two terminals)
```bash
uvicorn legalEaseAPI.main:app --reload      # backend  -> http://localhost:8000
streamlit run frontend/app.py               # frontend -> http://localhost:8501
```
(Mac/Linux/Git-Bash: `./run.sh` starts both.)

## Structure
```
ai_core/gemini_generator.py   Gemini prompt + call
ai_core/generator.py          sanitize_text, format_docx, format_pdf, format_html_preview
legalEaseAPI/main.py, routes.py   FastAPI app, POST /generate
frontend/app.py               Streamlit UI
config.py                     env + paths
Image/                        logos
```
