import streamlit as st
import re
from io import BytesIO
from datetime import datetime
import PyPDF2
from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib.styles import getSampleStyleSheet
import base64
import requests

st.set_page_config(
    page_title="Contract Risk Intelligence",
    layout="wide"
)

# ---------- BACKGROUND IMAGE ----------
bg_url = "https://images.unsplash.com/photo-1557683316-973673baf926"
bg_image = base64.b64encode(requests.get(bg_url).content).decode()

st.markdown(f"""
<style>

/* Page background */
.stApp {{
    background-image: url("data:image/png;base64,{bg_image}");
    background-size: cover;
    background-attachment: fixed;
}}

/* Main container */
[data-testid="stAppViewContainer"] {{
    background: rgba(245, 248, 255, 0.92);
    padding: 2.5rem;
}}

/* Title */
h1 {{
    color: #0b1f44;
    font-weight: 700;
}}

/* Card style */
.card {{
    background: linear-gradient(180deg, #ffffff, #f3f6ff);
    padding: 1.8rem;
    border-radius: 18px;
    box-shadow: 0 14px 40px rgba(0,0,0,0.12);
    margin-bottom: 1.6rem;
}}

/* Risk badges */
.low {{
    background: #e6f9f0;
    color: #13795b;
    padding: 8px 16px;
    border-radius: 20px;
    font-weight: 600;
}}

.medium {{
    background: #fff4e5;
    color: #9a5b00;
    padding: 8px 16px;
    border-radius: 20px;
    font-weight: 600;
}}

.high {{
    background: #fdecea;
    color: #b42318;
    padding: 8px 16px;
    border-radius: 20px;
    font-weight: 600;
}}

/* Button */
[data-testid="stButton"] button {{
    background: linear-gradient(90deg, #1f3cff, #3b82f6);
    color: white;
    font-weight: 700;
    border-radius: 14px;
    padding: 0.6rem 1.6rem;
    border: none;
}}

[data-testid="stButton"] button:hover {{
    background: linear-gradient(90deg, #1b2ed8, #2563eb);
}}

</style>
""", unsafe_allow_html=True)

# ---------- HEADER ----------
st.markdown("# Contract Risk Intelligence Platform")
st.markdown("### AI-assisted legal risk review for enterprise-ready decisions")

# ---------- FILE UPLOAD ----------
uploaded_file = st.file_uploader("Upload Contract File", type=["txt", "pdf"])

contract_text = ""

if uploaded_file:
    if uploaded_file.name.endswith(".txt"):
        contract_text = uploaded_file.read().decode("utf-8")
    else:
        reader = PyPDF2.PdfReader(uploaded_file)
        for page in reader.pages:
            contract_text += page.extract_text() + "\n"

def extract_clauses(text):
    parts = re.split(r"\n[A-Z ]{4,}:", text)
    return [p.strip() for p in parts if len(p.strip()) > 80]

def detect_risks(text):
    rules = {
        "Termination Rights": r"terminate|termination",
        "Penalty Exposure": r"penalty|late fee|fine",
        "IP Ownership Risk": r"intellectual property|ownership",
        "Jurisdiction Risk": r"jurisdiction|court",
        "Indemnity Obligation": r"indemnify"
    }
    return [k for k, v in rules.items() if re.search(v, text, re.I)]

def risk_level(score):
    if score <= 2:
        return "LOW", "low"
    elif score <= 4:
        return "MEDIUM", "medium"
    else:
        return "HIGH", "high"

# ---------- ANALYSIS ----------
if st.button("Analyze Contract"):

    if not contract_text.strip():
        st.warning("Please upload a valid contract file.")
    else:
        clauses = extract_clauses(contract_text)
        risks = detect_risks(contract_text)
        level, css = risk_level(len(risks))

        col1, col2 = st.columns(2)

        with col1:
            st.markdown(f"""
            <div class="card">
                <h3>Overall Risk Level</h3>
                <span class="{css}">{level} RISK</span>
            </div>
            """, unsafe_allow_html=True)

        with col2:
            st.markdown("<div class='card'><h3>Detected Risk Factors</h3>", unsafe_allow_html=True)
            for r in risks:
                st.markdown(f"- {r}")
            st.markdown("</div>", unsafe_allow_html=True)

        st.markdown("<div class='card'><h3>Key Contract Clauses</h3>", unsafe_allow_html=True)
        for i, c in enumerate(clauses[:5], 1):
            st.markdown(f"**Clause {i}:** {c[:300]}...")
        st.markdown("</div>", unsafe_allow_html=True)

        # PDF export
        buffer = BytesIO()
        doc = SimpleDocTemplate(buffer)
        styles = getSampleStyleSheet()
        story = []

        story.append(Paragraph("Contract Risk Assessment Report", styles["Title"]))
        story.append(Paragraph(f"Generated on {datetime.now()}", styles["Normal"]))
        story.append(Paragraph(f"Overall Risk Level: {level}", styles["Heading2"]))

        for r in risks:
            story.append(Paragraph(r, styles["Normal"]))

        doc.build(story)
        buffer.seek(0)

        st.download_button(
            "Download PDF Report",
            buffer,
            file_name="contract_risk_report.pdf",
            mime="application/pdf"
        )
