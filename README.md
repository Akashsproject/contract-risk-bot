📄 Contract Risk Intelligence Platform

A web-based application that analyzes contract documents and highlights potential legal and business risks using rule-based text analysis.
Designed for students, freshers, and hackathon demonstrations.

🚀 Overview

The Contract Risk Intelligence Platform helps users upload contract documents and receive a structured overview of key clauses and possible risk indicators such as termination terms, penalties, indemnity clauses, and jurisdiction details.
The application focuses on clarity, usability, and professional presentation, making it suitable for academic projects and hackathons.

✨ Features

Upload contract documents (.txt and .pdf)
Automatic clause extraction
Detection of common contractual risk indicators
Overall risk classification (Low / Medium / High)
Clean, professional, and colorful UI
PDF risk assessment report generation
Fully browser-based (no local setup needed)

🛠️ Tech Stack

Python
Streamlit (UI & App Framework)
Regular Expressions (Clause & Risk Detection)
PyPDF2 (PDF parsing)
ReportLab (PDF report generation)

📂 Project Structure
contract-risk-bot/
│
├── app.py               # Main Streamlit application
├── requirements.txt     # Python dependencies
├── README.md            # Project documentation
└── sample_contract.txt  # Sample contract for testing

⚙️ Installation & Setup (Local)
pip install -r requirements.txt
streamlit run app.py
The app will automatically open in your browser.

🌐 Deployment

This project can be deployed easily using Streamlit Cloud by connecting the GitHub repository and selecting app.py as the entry point.
Recommended Python version:
Python 3.10 or 3.11

🧪 Sample Usage

Upload a contract file (.txt or .pdf)
Click Analyze Contract

View:
Risk level
Identified risk indicators
Clause highlights
Download the generated PDF report

⚠️ Disclaimer

This application is intended for educational and demonstration purposes only.
It does not provide legal advice and should not be used for real-world legal decision-making.

👨‍💻 Author

S. Akash
B.Tech – Information Technology
Fresher | Aspiring Software Engineer
