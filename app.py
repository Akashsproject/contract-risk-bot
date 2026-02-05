import streamlit as st
import re
from io import BytesIO
from datetime import datetime

# PDF handling
import PyPDF2

# PDF export
from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib.styles import getSampleStyleSheet

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="Contract Analysis & Risk Assessment Bot",
    layout="centered"
)

st.title("📄 Contract Analysis & Risk Assessment Bot")
st.caption("GenAI-powered legal assistant for Indian SMEs (Student Demo Project)")

# ---------------- FILE UPLOAD ----------------
uploaded_file = st.file_uploader(
    "Upload contract file (TXT or PDF)",
    type=["txt", "pdf"]
)

contract_text = ""

if uploaded_file:
    if uploaded_file.name.endswith(".txt"):
        contract_text = uploaded_file.read().decode("utf-8")

    elif uploaded_file.name.endswith(".pdf"):
        reader = PyPDF2.PdfReader(uploaded_file)
        for page in reader.pages:
            contract_text += page.extract_text() + "\n"

# ---------------- UTIL FUNCTIONS ----------------
def extract_clauses(text):
    clauses = re.split(r"\n\d+\.|\n[A-Z ]{5,}:", text)
    return [c.strip() for c in clauses if len(c.strip()) > 40]

def detect_risks(text):
    risks = []

    patterns = {
        "Termination": r"terminate|termination",
        "Penalty": r"penalty|fine|late fee",
        "Indemnity": r"indemnify|indemnification",
        "Jurisdiction": r"jurisdiction|court",
        "IP Ownership": r"intellectual property|IP|ownership",
        "Auto Renewal": r"auto renew|automatic renewal"
    }

    for name, pattern in patterns.items():
        if re.search(pattern, text, re.IGNORECASE):
            risks.append(name)

    return risks

def risk_score(risks):
    if len(risks) <= 2:
        return "LOW"
    elif len(risks) <= 4:
        return "MEDIUM"
    else:
        return "HIGH"

# ---------------- ANALYZE ----------------
if st.button("Analyze Contract"):

    if not contract_text.strip():
        st.warning("Please upload a contract file.")
    else:
        with st.spinner("Analyzing contract..."):

            clauses = extract_clauses(contract_text)
            risks = detect_risks(contract_text)
            score = risk_score(risks)

            summary = f"""
This contract appears to be a **service or commercial agreement**.
It outlines obligations, payments, and legal terms between two parties.
Some clauses may expose one party to legal or financial risks.
"""

        st.subheader("📊 Risk Assessment")
        st.write(f"**Overall Risk Score:** {score}")

        st.subheader("⚠️ Identified Risk Areas")
        if risks:
            for r in risks:
                st.write(f"- {r}")
        else:
            st.write("No major risk clauses detected.")

        st.subheader("🧾 Clause-by-Clause Overview")
        for i, clause in enumerate(clauses[:5], 1):
            st.markdown(f"**Clause {i}:** {clause[:300]}...")

        st.subheader("💡 Risk Mitigation Suggestions")
        st.write("""
- Ensure termination rights are mutual
- Clarify intellectual property ownership
- Negotiate fair penalty and notice periods
- Avoid one-sided jurisdiction clauses
""")

        # ---------------- PDF EXPORT ----------------
        buffer = BytesIO()
        doc = SimpleDocTemplate(buffer)
        styles = getSampleStyleSheet()
        content = []

        content.append(Paragraph("<b>Contract Risk Assessment Report</b>", styles["Title"]))
        content.append(Paragraph(f"Generated on: {datetime.now()}", styles["Normal"]))
        content.append(Paragraph(f"<b>Overall Risk Score:</b> {score}", styles["Normal"]))

        content.append(Paragraph("<b>Identified Risks:</b>", styles["Heading2"]))
        for r in risks:
            content.append(Paragraph(f"- {r}", styles["Normal"]))

        content.append(Paragraph("<b>Summary:</b>", styles["Heading2"]))
        content.append(Paragraph(summary, styles["Normal"]))

        doc.build(content)
        buffer.seek(0)

        st.download_button(
            "📥 Download Risk Report (PDF)",
            buffer,
            file_name="contract_risk_report.pdf",
            mime="application/pdf"
        )
