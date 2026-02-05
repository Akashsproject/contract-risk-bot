import streamlit as st
import re
from io import BytesIO
from datetime import datetime
import PyPDF2
from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib.styles import getSampleStyleSheet

st.set_page_config(
    page_title="Contract Risk Intelligence",
    layout="wide"
)

st.markdown("""
<style>

:root {
    --primary: #1f2a44;
    --secondary: #2f80ed;
    --accent: #00b4d8;
    --bg: #f4f7fb;
    --card: #ffffff;
    --low: #1e7f5a;
    --medium: #d68910;
    --high: #c0392b;
}

html, body, [class*="css"] {
    background-color: var(--bg);
    font-family: 'Segoe UI', sans-serif;
}

.header {
    background: linear-gradient(135deg, #1f2a44, #2f80ed);
    padding: 2rem;
    border-radius: 16px;
    color: white;
    margin-bottom: 2rem;
}

.header h1 {
    margin-bottom: 0.5rem;
}

.header p {
    opacity: 0.9;
    font-size: 16px;
}

.card {
    background-color: var(--card);
    padding: 1.8rem;
    border-radius: 14px;
    box-shadow: 0 10px 30px rgba(0,0,0,0.08);
    transition: transform 0.2s ease, box-shadow 0.2s ease;
    margin-bottom: 1.5rem;
}

.card:hover {
    transform: translateY(-3px);
    box-shadow: 0 14px 35px rgba(0,0,0,0.12);
}

.risk-low {
    color: var(--low);
    font-weight: 700;
    font-size: 18px;
}

.risk-medium {
    color: var(--medium);
    font-weight: 700;
    font-size: 18px;
}

.risk-high {
    color: var(--high);
    font-weight: 700;
    font-size: 18px;
}

.upload-box {
    border: 2px dashed var(--secondary);
    padding: 2rem;
    border-radius: 14px;
    background: rgba(47,128,237,0.05);
}

.stButton>button {
    background: linear-gradient(135deg, #2f80ed, #00b4d8);
    color: white;
    font-weight: 600;
    border-radius: 10px;
    padding: 0.7rem 1.4rem;
    border: none;
}

.stButton>button:hover {
    background: linear-gradient(135deg, #2563eb, #0096c7);
}

</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="header">
    <h1>Contract Risk Intelligence Platform</h1>
    <p>AI-assisted legal risk analysis for contracts, agreements, and business documents</p>
</div>
""", unsafe_allow_html=True)

uploaded_file = st.file_uploader(
    "Upload Contract Document (TXT or PDF)",
    type=["txt", "pdf"]
)

contract_text = ""

if uploaded_file:
    if uploaded_file.name.lower().endswith(".txt"):
        contract_text = uploaded_file.read().decode("utf-8")
    else:
        reader = PyPDF2.PdfReader(uploaded_file)
        for page in reader.pages:
            contract_text += page.extract_text() + "\n"

def extract_clauses(text):
    parts = re.split(r"\n\d+\.|\n[A-Z ]{4,}:", text)
    return [p.strip() for p in parts if len(p.strip()) > 60]

def detect_risks(text):
    rules = {
        "Termination Conditions": r"terminate|termination",
        "Financial Penalties": r"penalty|late fee|liquidated damages",
        "Indemnification": r"indemnify|indemnification",
        "Jurisdiction & Governing Law": r"jurisdiction|governing law|court",
        "Intellectual Property Rights": r"intellectual property|IP|ownership",
        "Automatic Renewal": r"auto renew|automatic renewal"
    }
    return [name for name, pat in rules.items() if re.search(pat, text, re.IGNORECASE)]

def risk_level(count):
    if count <= 2:
        return "LOW"
    if count <= 4:
        return "MEDIUM"
    return "HIGH"

if st.button("Analyze Contract", use_container_width=True):

    if not contract_text.strip():
        st.warning("Please upload a valid contract file to continue.")
    else:
        clauses = extract_clauses(contract_text)
        risks = detect_risks(contract_text)
        level = risk_level(len(risks))

        cls = {
            "LOW": "risk-low",
            "MEDIUM": "risk-medium",
            "HIGH": "risk-high"
        }[level]

        col1, col2 = st.columns(2)

        with col1:
            st.markdown("<div class='card'>", unsafe_allow_html=True)
            st.markdown("<h3>Overall Risk Profile</h3>", unsafe_allow_html=True)
            st.markdown(f"<div class='{cls}'>Risk Level: {level}</div>", unsafe_allow_html=True)
            st.markdown(
                "The document has been evaluated against common contractual risk indicators. "
                "The overall rating reflects potential legal and financial exposure."
            )
            st.markdown("</div>", unsafe_allow_html=True)

        with col2:
            st.markdown("<div class='card'>", unsafe_allow_html=True)
            st.markdown("<h3>Key Risk Indicators</h3>", unsafe_allow_html=True)
            if risks:
                for r in risks:
                    st.markdown(f"• {r}")
            else:
                st.markdown("No major risk indicators identified.")
            st.markdown("</div>", unsafe_allow_html=True)

        st.markdown("<div class='card'>", unsafe_allow_html=True)
        st.markdown("<h3>Clause Highlights</h3>", unsafe_allow_html=True)
        for i, clause in enumerate(clauses[:5], 1):
            st.markdown(f"**Clause {i}**: {clause[:420]}...")
        st.markdown("</div>", unsafe_allow_html=True)

        st.markdown("<div class='card'>", unsafe_allow_html=True)
        st.markdown("<h3>Recommended Actions</h3>", unsafe_allow_html=True)
        st.markdown("""
- Review termination clauses for mutual fairness  
- Confirm ownership and usage rights of intellectual property  
- Ensure penalties are proportionate and capped  
- Avoid restrictive jurisdiction where possible  
""")
        st.markdown("</div>", unsafe_allow_html=True)

        buffer = BytesIO()
        doc = SimpleDocTemplate(buffer)
        styles = getSampleStyleSheet()
        content = []

        content.append(Paragraph("Contract Risk Assessment Report", styles["Title"]))
        content.append(Paragraph(f"Generated on {datetime.now()}", styles["Normal"]))
        content.append(Paragraph(f"Overall Risk Level: {level}", styles["Normal"]))

        for r in risks:
            content.append(Paragraph(r, styles["Normal"]))

        doc.build(content)
        buffer.seek(0)

        st.download_button(
            "Download Risk Assessment Report (PDF)",
            buffer,
            file_name="contract_risk_report.pdf",
            mime="application/pdf"
        )
