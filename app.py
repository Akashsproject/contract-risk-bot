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
body {
    background-color: #f5f7fb;
}
.main {
    padding: 2rem;
}
h1 {
    color: #1f2a44;
    font-weight: 700;
}
h2, h3 {
    color: #243a5e;
}
.card {
    background-color: #ffffff;
    padding: 1.5rem;
    border-radius: 12px;
    box-shadow: 0 6px 18px rgba(0,0,0,0.08);
    margin-bottom: 1.5rem;
}
.risk-low {
    color: #1b7f5a;
    font-weight: 700;
}
.risk-medium {
    color: #c47f00;
    font-weight: 700;
}
.risk-high {
    color: #c0392b;
    font-weight: 700;
}
</style>
""", unsafe_allow_html=True)

st.markdown("<h1>Contract Risk Intelligence Platform</h1>", unsafe_allow_html=True)
st.markdown(
    "<p style='font-size:16px;color:#4a5d7a;'>"
    "AI-assisted contract analysis to help businesses understand legal exposure, obligations, and risk areas."
    "</p>",
    unsafe_allow_html=True
)

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
    raw = re.split(r"\n\d+\.|\n[A-Z ]{4,}:", text)
    return [c.strip() for c in raw if len(c.strip()) > 50]

def detect_risks(text):
    mapping = {
        "Termination Rights": r"terminate|termination",
        "Penalty / Late Fees": r"penalty|fine|late fee",
        "Indemnity Obligations": r"indemnify|indemnification",
        "Jurisdiction Clause": r"jurisdiction|court",
        "Intellectual Property Transfer": r"intellectual property|IP|ownership",
        "Auto Renewal Clause": r"auto renew|automatic renewal"
    }
    found = []
    for name, pattern in mapping.items():
        if re.search(pattern, text, re.IGNORECASE):
            found.append(name)
    return found

def calculate_risk_level(count):
    if count <= 2:
        return "LOW"
    if count <= 4:
        return "MEDIUM"
    return "HIGH"

if st.button("Run Contract Analysis", use_container_width=True):

    if not contract_text.strip():
        st.warning("Please upload a valid contract document to proceed.")
    else:
        clauses = extract_clauses(contract_text)
        risks = detect_risks(contract_text)
        level = calculate_risk_level(len(risks))

        if level == "LOW":
            risk_class = "risk-low"
        elif level == "MEDIUM":
            risk_class = "risk-medium"
        else:
            risk_class = "risk-high"

        col1, col2 = st.columns(2)

        with col1:
            st.markdown("<div class='card'>", unsafe_allow_html=True)
            st.markdown("<h3>Overall Risk Assessment</h3>", unsafe_allow_html=True)
            st.markdown(
                f"<p class='{risk_class}'>Risk Level: {level}</p>",
                unsafe_allow_html=True
            )
            st.markdown(
                "<p>"
                "The contract has been evaluated based on common legal risk indicators. "
                "Identified clauses may require review or renegotiation to reduce exposure."
                "</p>",
                unsafe_allow_html=True
            )
            st.markdown("</div>", unsafe_allow_html=True)

        with col2:
            st.markdown("<div class='card'>", unsafe_allow_html=True)
            st.markdown("<h3>Detected Risk Areas</h3>", unsafe_allow_html=True)
            if risks:
                for r in risks:
                    st.markdown(f"- {r}")
            else:
                st.markdown("No significant risk indicators detected.")
            st.markdown("</div>", unsafe_allow_html=True)

        st.markdown("<div class='card'>", unsafe_allow_html=True)
        st.markdown("<h3>Clause Overview</h3>", unsafe_allow_html=True)
        for i, clause in enumerate(clauses[:6], 1):
            st.markdown(f"**Clause {i}:** {clause[:400]}...")
        st.markdown("</div>", unsafe_allow_html=True)

        st.markdown("<div class='card'>", unsafe_allow_html=True)
        st.markdown("<h3>Recommended Risk Mitigation</h3>", unsafe_allow_html=True)
        st.markdown("""
- Ensure termination rights are balanced for both parties  
- Clarify ownership and usage rights of intellectual property  
- Review penalty clauses for proportionality  
- Avoid restrictive jurisdiction unless necessary  
""")
        st.markdown("</div>", unsafe_allow_html=True)

        buffer = BytesIO()
        doc = SimpleDocTemplate(buffer)
        styles = getSampleStyleSheet()
        content = []

        content.append(Paragraph("<b>Contract Risk Assessment Report</b>", styles["Title"]))
        content.append(Paragraph(f"Generated on: {datetime.now()}", styles["Normal"]))
        content.append(Paragraph(f"<b>Overall Risk Level:</b> {level}", styles["Normal"]))

        content.append(Paragraph("<b>Identified Risk Areas</b>", styles["Heading2"]))
        for r in risks:
            content.append(Paragraph(r, styles["Normal"]))

        content.append(Paragraph("<b>Summary</b>", styles["Heading2"]))
        content.append(Paragraph(
            "This report highlights contractual clauses that may expose the parties "
            "to legal or financial risks and should be reviewed carefully.",
            styles["Normal"]
        ))

        doc.build(content)
        buffer.seek(0)

        st.download_button(
            "Download Professional Risk Report (PDF)",
            buffer,
            file_name="contract_risk_report.pdf",
            mime="application/pdf"
        )
