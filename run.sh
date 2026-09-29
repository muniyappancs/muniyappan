#!/bin/bash
# Starts FastAPI backend (port 8000) and Streamlit frontend (port 8501)
uvicorn legalEaseAPI.main:app --reload --port 8000 &
BACK=$!
trap "kill $BACK" EXIT
streamlit run frontend/app.py
