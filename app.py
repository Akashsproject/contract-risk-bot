import streamlit as st
import re
from openai import OpenAI

# ---------------- CONFIG ----------------
st.set_page_config(page_title="Contract Risk Assessment Bot", layout="centered")

st.title("📄 Contract Analysis & Risk Assessment Bot")
st.write("Upload a contract and get a plain-English risk analysis for Indian SMEs.")

# ---------------- OPENAI CLIENT ----------------
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

# ---------------- FILE UPLOAD ----------------
uploaded_file = st.file_uploader("Upload contract (.txt only for demo)", type=["txt"])

contract_text = ""

if uploaded_file:
    contract_text = uploaded_file.read().decode("utf-8")

# ---------------- ANALYZE BUTTON ----------------
analyze_clicked = st.button("Analyze Contract")

if analyze_clicked:
    if not contract_text:
        st.warning("Please upload a contract file first.")
    else:
        with st.spinner("Analyzing contract..."):
            prompt = f"""
You are a legal assistant for Indian small businesses.

Tasks:
1. Identify the contract type.
2. Summarize the contract in simple business English.
3. Identify risky clauses (termination, penalty, indemnity, jurisdiction, auto-renewal).
4. Assign an overall risk score: Low, Medium, or High.
5. Suggest 2 renegotiation tips.

Contract Text:
{contract_text}
"""

            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[{"role": "user", "content": prompt}]
            )

            result = response.choices[0].message.content

        st.subheader("📊 Analysis Result")
        st.write(result)
