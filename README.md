# Incident Report Compliance Checker

This is a bilingual Streamlit app that checks the compliance of incident reports written in **English** or **Portuguese**. It uses spaCy-based NLP, custom rule-checking, and interactive feedback to detect:

- Missing required information (date, time, organization, etc.)
- Vague language (e.g., "something went wrong")
- Whether the report is written in the past tense
- Inline highlights for clarity

## Features
- Supports pasted text or file uploads (`.txt`, `.docx`)
- Works in both English and Portuguese
- Shows summary table of rule violations
- Highlights issues directly in the report text
- Allows exporting results to Excel

## Demo
You can [deploy it on Streamlit Cloud](https://streamlit.io/cloud) or Hugging Face Spaces.

---

## Setup Instructions

### 1. Install Requirements
```bash
pip install -r requirements.txt
python -m spacy download en_core_web_sm
python -m spacy download pt_core_news_sm
```

### 2. Run the App
```bash
streamlit run incident_checker_app.py
```

### 3. Files
- `incident_checker_app.py`: Main Streamlit app
- `requirements.txt`: Dependencies
- `README.md`: This file

---

## Deploying

### Streamlit Cloud
1. Push to a GitHub repository (e.g., `lilferreira/complianceCheck`)
2. Log in at [https://streamlit.io/cloud](https://streamlit.io/cloud)
3. Click "New app", connect your repo, and select `incident_checker_app.py`

### Hugging Face Spaces
1. Create a new **Streamlit Space**
2. Upload the same files (`.py`, `requirements.txt`, etc.)
3. Done! Hugging Face allows iframe embedding.

---

## Embed on Your Website

To embed the demo, use this HTML:

```html
<iframe 
  src="https://your-deployment-url" 
  width="100%" 
  height="700" 
  style="border:none;">
</iframe>
```

If iframe embedding doesn't work, use a launch button instead:

```html
<a href="https://your-deployment-url" target="_blank">Try the Demo</a>
```

---

## Author
Liliana Ferreira — [Mondegreen.ai](https://mondegreen.ai)

For questions or suggestions, open an issue or reach out!
