# 🏦 FinPulse AI — Hybrid Autonomous Fintech Wealth, Risk & Fraud Copilot

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://share.streamlit.io)

**FinPulse AI** is a production-grade Fintech AI Copilot engineered with a **Zero-Barrier Hybrid AI Architecture**:
1. **Works 100% Out-of-the-Box (No API Key Required):** Visitors and prospective clients can test every feature immediately using the built-in **Autonomous Quantitative Financial Engine** (Mean-Variance portfolio drift optimization, 400-path Geometric Brownian Motion Monte Carlo simulations, Isolation-Score fraud forensics, Tax-Alpha arbitrage, and Prime Credit/SBLOC underwriting).
2. **Optional Live Cloud LLM Upgrade (BYOK):** End-users can optionally paste a **Google Gemini**, **OpenAI**, or **Groq** API key in the sidebar to combine live LLM synthesis with real-time financial RAG telemetry.

---

## 📂 Repository File Structure
```text
finpulse-ai-fintech-copilot/
├── app.py                        # Main Streamlit Hybrid AI application
├── requirements.txt              # Streamlit Cloud Python dependencies
├── .streamlit/
│   └── config.toml               # Pre-configured dark institutional UI theme
├── sample_transactions_test.csv  # Sample CSV file for testing custom Fraud Audit uploads
├── .gitignore                    # Ignores local virtualenvs and secret files
└── README.md                     # Project documentation
```

## 🚀 Deploying to Streamlit Community Cloud
1. Upload all files in this folder to a public GitHub repository.
2. Go to [share.streamlit.io](https://share.streamlit.io) and click **Create app**.
3. Select your repository, branch (`main`), and main file path (`app.py`).
4. Click **Deploy!**
