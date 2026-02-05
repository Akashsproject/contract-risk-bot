import streamlit as st
import re
from io import BytesIO
from datetime import datetime
import PyPDF2
from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib.styles import getSampleStyleSheet

st.set_page_config(
    page_title="Contract Risk Intelligence Platform",
    layout="wide"
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}

body {
    background: linear-gradient(180deg, #f4f7fc 0%, #eef2f9 100%);
}

.main {
    padding: 2.5rem;
}

h1 {
    color: #0f1f3d;
    font-weight: 700;
}

.subtitle {
    font-size: 16px;
    color: #42526e;
    margin-bottom: 2rem;
}

.card {
    background: linear-gradient(180deg, #ffffff 0%, #f9fbff 100%);
    padding: 1.6rem;
    border-radius: 16px;
    box-shadow: 0 10px 28px rgba(15, 31, 61, 0.08);
    transition: all 0.3s ease;
    margin-bottom: 1.6rem;
}

.card:hover {
    transform: translateY(-4px);
    box-shadow: 0 16px 40px rgba(15, 31, 61, 0.12);
}

.badge {
    display: inline-block;
    padding: 6px 14px;
    border-radius: 20px;
    font-weight: 600;
    font-size: 14px;
}

.low {
    background-color: #e6f6ef;
    color: #127a53;
}

.medium {
    background-color: #fff4e5;
    color: #b26a00;
}

.high {
    background-color: #fdecea;
    color: #b42318;
}

.action-btn button {
    background: linear-gradient(90deg, #1f4fd8, #3b82f6);
    color: white;
    font-weight: 600;
    border-radius: 12px;
    padding: 0.6rem 1.2rem;
    border: none;
}

.action-btn button:hover {
    background: linear-gradient(90deg, #1a3fb8, #2563eb);
}

ul {
    padding-left: 1.2rem;
}

</style>
""", unsafe_allow_html=True)

st.markdown("<h1>Contract Risk Intelligence Platform</h1>", unsafe_allow_html=True)
st.markdown(
    "<div class='subtitle'>AI-assisted legal risk analysis for smarter contract decisions</div>",
    unsafe_allow_html=True
)

uploaded_file = st.file_uploader(
    "Upload Contract Document",
    type=["txt", "pdf"]
)

contract_text = ""

if uploaded_file:
    if uploaded_file.name.endswith(".txt"):
        contract_text = uploaded_file.read().decode("utf-8")
    else:
        reader = PyPDF2.PdfReader(uploaded_file)
        for page in reader.pages:
            contract_text += page.extract_text() + "\n"

def extract_clauses(text):
    blocks = re.split(r"\n\d+\.|\n[A-Z ]{4,}:", text)
    return [b.strip() for b in blocks if len(b.strip()) > 60]

def detect_risks(text):
    rules = {
        "Termination Conditions": r"terminate|termination",
        "Financial Penalties": r"penalty|fine|late fee",
        "Indemnification Clause": r"indemnify|indemnification",
        "Jurisdiction Restriction": r"jurisdiction|court",
        "Intellectual Property Rights": r"intellectual property|IP|ownership",
        "Automatic Renewal": r"auto renew|automatic renewal"
    }
    return [name for name, pattern in rules.items() if re.search(pattern, text, re.I)]

def risk_level(score):
    if score <= 2:
        return "LOW", "low"
    if score <= 4:
        return "MEDIUM", "medium"
    return "HIGH", "high"

if st.button("Analyze Contract", use_container_width=True):

    if not contract_text.strip():
        st.warning("Please upload a valid contract document.")
    else:
        clauses = extract_clauses(contract_text)
        risks = detect_risks(contract_text)
        level_text, level_class = risk_level(len(risks))

        col1, col2 = st.columns([1, 1])

        with col1:
            st.markdown("<div class='card'>", unsafe_allow_html=True)
            st.markdown("<h3>Overall Risk Status</h3>", unsafe_allow_html=True)
            st.markdown(
                f"<span class='badge {level_class}'>{level_text} RISK</span>",
                unsafe_allow_html=True
            )
            st.markdown(
                "<p style='margin-top:12px;color:#42526e;'>"
                "Risk score is derived from contractual obligations, penalties, "
                "termination clauses, and jurisdictional exposure."
                "</p>",
                unsafe_allow_html=True
            )
            st.markdown("</div>", unsafe_allow_html=True)

        with col2:
            st.markdown("<div class='card'>", unsafe_allow_html=True)
            st.markdown("<h3>Key Risk Indicators</h3>", unsafe_allow_html=True)
            if risks:
                for r in risks:
                    st.markdown(f"• {r}")
            else:
                st.markdown("No significant contractual risks detected.")
            st.markdown("</div>", unsafe_allow_html=True)

        st.markdown("<div class='card'>", unsafe_allow_html=True)
        st.markdown("<h3>Clause Highlights</h3>", unsafe_allow_html=True)
        for i, c in enumerate(clauses[:5], 1):
            st.markdown(f"**Clause {i}** — {c[:350]}...")
        st.markdown("</div>", unsafe_allow_html=True)

        st.markdown("<div class='card'>", unsafe_allow_html=True)
        st.markdown("<h3>Suggested Improvements</h3>", unsafe_allow_html=True)
        st.markdown("""
- Balance termination rights between parties  
- Limit financial penalties to reasonable thresholds  
- Clearly define IP ownership and usage rights  
- Avoid restrictive jurisdiction unless legally required  
""")
        st.markdown("</div>", unsafe_allow_html=True)

        buffer = BytesIO()
        doc = SimpleDocTemplate(buffer)
        styles = getSampleStyleSheet()
        story = []

        story.append(Paragraph("Contract Risk Assessment Report", styles["Title"]))
        story.append(Paragraph(f"Generated on {datetime.now()}", styles["Normal"]))
        story.append(Paragraph(f"Overall Risk Level: {level_text}", styles["Heading2"]))

        for r in risks:
            story.append(Paragraph(r, styles["Normal"]))

        doc.build(story)
        buffer.seek(0)

        st.download_button(
            "Download Executive PDF Report",
            buffer,
            file_name="contract_risk_report.pdf",
            mime="application/pdf"
        )
