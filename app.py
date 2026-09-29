import os
import sys

import requests
import streamlit as st

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from ai_core.generator import format_docx, format_html_preview, format_pdf, sanitize_text  # noqa: E402
from config import BACKEND_URL, WEB_LOGO_PATH  # noqa: E402

st.set_page_config(page_title="LegalEase", layout="centered")

_, col2, _ = st.columns([1, 2, 1])
with col2:
    st.image(WEB_LOGO_PATH, use_container_width=True)

st.markdown("<h2 style='text-align: center;'>AI Legal Document Generator</h2>", unsafe_allow_html=True)

document_type = st.text_input("Document Type (Ex: Agreement, Contract, NDA)")
parties = st.text_area("Parties Involved")
terms = st.text_area("Terms & Conditions (Use semicolons for bullet points)")
dates = st.text_input("Effective Date")

if st.button("Generate Document"):
    if not all([document_type.strip(), parties.strip(), terms.strip(), dates.strip()]):
        st.warning("Please fill in all the fields.")
    else:
        with st.spinner("Drafting your document..."):
            try:
                response = requests.post(
                    f"{BACKEND_URL}/generate",
                    json={"document_type": document_type, "parties": parties,
                          "terms": terms, "dates": dates},
                    timeout=120,
                )
                if response.ok:
                    st.session_state.generated_text = sanitize_text(response.json()["document"])
                    st.session_state.doc_type = document_type
                    st.session_state.terms = terms
                    st.session_state.show_edit = False
                    st.session_state.pop("editor", None)
                    st.success("Document Generated Successfully!")
                else:
                    st.error(f"Backend error: {response.json().get('detail', response.text)}")
            except requests.exceptions.ConnectionError:
                st.error("Cannot reach the backend. Start it with: uvicorn legalEaseAPI.main:app --reload")
            except Exception as e:
                st.error(f"Something went wrong: {e}")

if st.session_state.get("generated_text"):
    styled_html = format_html_preview(st.session_state.generated_text)
    st.markdown(
        "<div style='background:#0f1626;color:#e6e6e6;padding:20px;border-radius:10px;"
        f"max-height:400px;overflow-y:auto;'>{styled_html}</div>",
        unsafe_allow_html=True,
    )

    if st.button("✏️ Click to Edit Document"):
        st.session_state.show_edit = not st.session_state.get("show_edit", False)

    if st.session_state.get("show_edit"):
        edited = st.text_area("Edit Document Below:", st.session_state.generated_text,
                              height=300, key="editor")
        st.session_state.generated_text = edited

    text = st.session_state.generated_text
    dtype = st.session_state.get("doc_type", "Legal Document")
    fname = dtype.replace(" ", "_").lower()

    st.download_button("📄 Download as .TXT", data=text, file_name=f"{fname}.txt", mime="text/plain")
    st.download_button(
        "📝 Download as .DOCX",
        data=format_docx(text, dtype, st.session_state.get("terms", "")),
        file_name=f"{fname}.docx",
        mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
    )
    st.download_button("📕 Download as .PDF", data=format_pdf(text, dtype),
                       file_name=f"{fname}.pdf", mime="application/pdf")
else:
    st.info("Click 'Generate Document' to start")
