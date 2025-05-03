import streamlit as st
import pandas as pd
import spacy
from io import StringIO
from docx import Document
import re

# Load both language models
MODELS = {
    "English": spacy.load("en_core_web_sm"),
    "Portuguese": spacy.load("pt_core_news_sm")
}

VAGUE_TERMS = {
    "English": ["something went wrong", "issue occurred", "problem happened"],
    "Portuguese": ["algo correu mal", "ocorreu um problema", "houve uma falha"]
}

REQUIRED_ENTITIES = {
    "English": ["DATE", "TIME", "ORG", "GPE"],
    "Portuguese": ["DATA", "TEMPO", "ORG", "LOC"]  # Adapted for Portuguese
}

def extract_text_from_docx(file):
    doc = Document(file)
    return "\n".join([para.text for para in doc.paragraphs])

def check_required_entities(doc, lang):
    found = {ent.label_ for ent in doc.ents}
    return [ent for ent in REQUIRED_ENTITIES[lang] if ent not in found]

def check_vague_phrases(text, lang):
    return any(term in text.lower() for term in VAGUE_TERMS[lang])

def check_past_tense(doc, lang):
    if lang == "English":
        past_verbs = [token for token in doc if token.tag_ in ("VBD", "VBN")]
        return len(past_verbs) > 2
    elif lang == "Portuguese":
        endings = ("ou", "ava", "aram", "ia", "iam")
        past_verbs = [token for token in doc if token.tag_ == "VERB" and token.text.lower().endswith(endings)]
        return len(past_verbs) > 1
    return False

def evaluate_report(text, lang):
    doc = MODELS[lang](text)
    return {
        "Missing Entities": ", ".join(check_required_entities(doc, lang)) or "All present",
        "Vague Language Detected": "Yes" if check_vague_phrases(text, lang) else "No",
        "Written in Past Tense": "Yes" if check_past_tense(doc, lang) else "No"
    }

def highlight_violations(text, results, lang):
    vague_terms = VAGUE_TERMS[lang]
    for term in vague_terms:
        if term in text.lower():
            pattern = re.compile(re.escape(term), re.IGNORECASE)
            text = pattern.sub(f"<span style='background-color:#FFA500'>{term}</span>", text)

    if results.get("Written in Past Tense") == "No":
        text = f"<span style='background-color:#ADD8E6'>{text}</span>"

    comments = ""
    if results.get("Missing Entities") != "All present":
        comments = f"<p><strong style='color:red'>Missing Entities:</strong> {results['Missing Entities']}</p>"

    return comments + "<p>" + text.replace("\n", "<br>") + "</p>"

# --- Streamlit UI ---
st.set_page_config(page_title="Incident Compliance Checker", layout="wide")
st.title("Incident Report Compliance Checker")

language = st.radio("Select report language:", ["English", "Portuguese"], horizontal=True)
option = st.radio("Choose input method:", ["Paste Text", "Upload File"])

texts = []

if option == "Paste Text":
    text_input = st.text_area("Paste the incident report:", height=250)
    if text_input.strip():
        texts.append(("Manual Entry", text_input))
elif option == "Upload File":
    uploaded_files = st.file_uploader("Upload .txt or .docx files", type=["txt", "docx"], accept_multiple_files=True)
    for file in uploaded_files:
        if file.name.endswith(".txt"):
            content = StringIO(file.getvalue().decode("utf-8")).read()
        elif file.name.endswith(".docx"):
            content = extract_text_from_docx(file)
        else:
            continue
        texts.append((file.name, content))

if st.button("Check Compliance") and texts:
    results = []
    for name, text in texts:
        res = evaluate_report(text, language)
        res["Report"] = name
        results.append(res)

    df = pd.DataFrame(results).set_index("Report")
    st.subheader("Evaluation Results Table")
    st.dataframe(df)

    excel_buffer = io.BytesIO()
    df.to_excel(excel_buffer, index=True, engine="openpyxl")
    excel_buffer.seek(0)  # Rewind the buffer

    # Download button
    st.download_button(
        label="Download Results as Excel",
        data=excel_buffer,
        file_name="compliance_results.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )

    st.subheader("Inline Highlights")
    for name, text in texts:
        st.markdown(f"### Report: {name}")
        result = evaluate_report(text, language)
        html = highlight_violations(text, result, language)
        st.markdown(html, unsafe_allow_html=True)

elif st.button("Check Compliance"):
    st.warning("Please input or upload at least one report.")
