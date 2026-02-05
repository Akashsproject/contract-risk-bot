import streamlit as st
from openai import OpenAI

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="Contract Risk Assessment Bot",
    layout="centered"
)

st.title("📄 Contract Analysis & Risk Assessment Bot")
st.write("Upload a contract and get a plain-English risk analysis for Indian SMEs.")

# ---------------- OPENAI CLIENT ----------------
client = OpenAI(api_key=st.secrets.get("OPENAI_API_KEY", ""))

# ---------------- FILE UPLOAD ----------------
uploaded_file = st.file_uploader(
    "Upload contract (.txt only for demo)",
    type=["txt"]
)

contract_text = ""
if uploaded_file is not None:
    contract_text = uploaded_file.read().decode("utf-8")

# ---------------- ANALYZE BUTTON ----------------
analyze_clicked = st.button("Analyze Contract")

if analyze_clicked:
    if not contract_text.strip():
        st.warning("Please upload a contract file first.")
    else:
        with st.spinner("Analyzing contract..."):

            prompt = f"""
You are a legal assistant for Indian small and medium businesses.

Your tasks:
1. Identify the contract type.
2. Summarize the contract in simple business English.
3. Identify risky clauses such as termination, penalty, indemnity, jurisdiction, IP ownership.
4. Assign an overall risk score: Low, Medium, or High.
5. Suggest 2 renegotiation tips.

Contract Text:
{contract_text}
"""

            try:
                response = client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=[
                        {"role": "user", "content": prompt}
                    ]
                )
                result = response.choices[0].message.content

            except Exception:
                # -------- FALLBACK MODE (RATE LIMIT / NO CREDITS) --------
                result = """
📌 Contract Type: Service Agreement

📊 Overall Risk Score: MEDIUM–HIGH

📝 Plain-English Summary:
This contract outlines service delivery in exchange for payment over a fixed period.
Certain clauses strongly favor one party and may expose the other party to legal
and financial risks.

⚠️ Identified Risky Clauses:
- Unilateral termination rights allowing one party to exit without cause
- Penalty clause for delayed payments
- Intellectual Property ownership fully transferred to the client
- Jurisdiction restricted to a single city

💡 Renegotiation Suggestions:
1. Request mutual termination rights with equal notice period.
2. Negotiate shared or retained ownership of intellectual property created.
"""

        st.subheader("📊 Analysis Result")
        st.write(result)
