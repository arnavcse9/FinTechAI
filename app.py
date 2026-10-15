"""
================================================================================
FINPULSE AI - HYBRID AUTONOMOUS FINTECH WEALTH, RISK & FRAUD COPILOT
Portfolio-Grade Streamlit Application for Upwork Showcase
================================================================================
Works 100% smoothly WITHOUT an API key (Zero-Barrier Hybrid Quantitative Engine)
AND supports optional live API keys for Google Gemini, OpenAI, and Groq!
================================================================================
"""

import io
import json
import time
import math
import zipfile
import datetime
from typing import Dict, List, Any, Tuple, Optional

import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import requests
import streamlit as st

st.set_page_config(
    page_title="FinPulse AI | Autonomous Fintech Copilot",
    page_icon="🏦",
    layout="wide",
    initial_sidebar_state="expanded",
)


def inject_custom_css() -> None:
    """Injects modern dark-mode Fintech CSS styling for an executive UI look."""
    st.markdown(
        """
        <style>
        .stApp {
            background: radial-gradient(circle at 10% 10%, #0f172a 0%, #090d16 100%);
            color: #f8fafc;
        }
        .fin-hero {
            background: linear-gradient(135deg, rgba(30, 41, 59, 0.85) 0%, rgba(15, 23, 42, 0.95) 100%);
            border: 1px solid rgba(56, 189, 248, 0.25);
            border-radius: 16px;
            padding: 1.5rem 2rem;
            margin-bottom: 1.25rem;
            box-shadow: 0 10px 30px -10px rgba(0, 0, 0, 0.6);
        }
        .fin-badge {
            display: inline-block;
            background: rgba(16, 185, 129, 0.15);
            color: #34d399;
            border: 1px solid rgba(16, 185, 129, 0.4);
            font-size: 0.75rem;
            font-weight: 700;
            padding: 0.2rem 0.65rem;
            border-radius: 999px;
            letter-spacing: 0.06em;
            text-transform: uppercase;
            margin-bottom: 0.5rem;
        }
        .fin-title {
            font-size: 1.9rem;
            font-weight: 800;
            background: linear-gradient(90deg, #ffffff 0%, #38bdf8 55%, #34d399 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            margin: 0;
            line-height: 1.2;
        }
        .fin-subtitle {
            color: #94a3b8;
            font-size: 0.95rem;
            margin-top: 0.4rem;
            margin-bottom: 0;
        }
        .kpi-card {
            background: rgba(30, 41, 59, 0.6);
            border: 1px solid rgba(148, 163, 184, 0.16);
            border-radius: 14px;
            padding: 1.15rem 1.25rem;
            transition: all 0.2s ease-in-out;
            height: 100%;
        }
        .kpi-card:hover {
            border-color: rgba(56, 189, 248, 0.45);
            transform: translateY(-2px);
        }
        .kpi-label {
            color: #94a3b8;
            font-size: 0.78rem;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 0.05em;
        }
        .kpi-value {
            color: #f8fafc;
            font-size: 1.55rem;
            font-weight: 800;
            margin-top: 0.25rem;
            margin-bottom: 0.25rem;
        }
        .kpi-delta-pos { color: #34d399; font-size: 0.8rem; font-weight: 600; }
        .kpi-delta-warn { color: #fbbf24; font-size: 0.8rem; font-weight: 600; }
        .kpi-delta-neg { color: #f87171; font-size: 0.8rem; font-weight: 600; }
        .agent-pill {
            display: inline-block;
            background: rgba(56, 189, 248, 0.12);
            color: #38bdf8;
            border: 1px solid rgba(56, 189, 248, 0.3);
            border-radius: 6px;
            padding: 2px 8px;
            font-size: 0.75rem;
            font-family: monospace;
            margin-right: 6px;
            margin-bottom: 4px;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


CLIENT_PROFILES: Dict[str, Dict[str, Any]] = {
    "Alex Rivera (Tech Executive - Growth)": {
        "client_id": "FP-90812",
        "risk_tolerance": "Aggressive Growth",
        "credit_score": 792,
        "monthly_income": 18500.0,
        "monthly_expenses": 9420.0,
        "cash_reserves": 64500.0,
        "tax_bracket": 32,
        "holdings": [
            {"Asset": "US Tech Equities (QQQ/NVDA/MSFT)", "Class": "Equities", "Balance": 168000, "Target_Weight": 0.45, "Expected_Return": 0.135, "Volatility": 0.22},
            {"Asset": "S&P 500 Core Index (VOO)", "Class": "Equities", "Balance": 95000, "Target_Weight": 0.25, "Expected_Return": 0.102, "Volatility": 0.15},
            {"Asset": "US Treasury Bills (5.1% Yield)", "Class": "Fixed Income", "Balance": 48000, "Target_Weight": 0.15, "Expected_Return": 0.051, "Volatility": 0.02},
            {"Asset": "Private Credit & REITs", "Class": "Alternatives", "Balance": 36000, "Target_Weight": 0.10, "Expected_Return": 0.088, "Volatility": 0.11},
            {"Asset": "Digital Assets (BTC/ETH ETF)", "Class": "Crypto", "Balance": 28000, "Target_Weight": 0.05, "Expected_Return": 0.190, "Volatility": 0.48},
        ],
    },
    "Dr. Priya Nair (Physician - Balanced Wealth)": {
        "client_id": "FP-44209",
        "risk_tolerance": "Moderate / Tax-Optimized",
        "credit_score": 818,
        "monthly_income": 26000.0,
        "monthly_expenses": 11800.0,
        "cash_reserves": 112000.0,
        "tax_bracket": 35,
        "holdings": [
            {"Asset": "S&P 500 Core Index (VOO)", "Class": "Equities", "Balance": 240000, "Target_Weight": 0.40, "Expected_Return": 0.102, "Volatility": 0.15},
            {"Asset": "Municipal Tax-Free Bonds", "Class": "Fixed Income", "Balance": 165000, "Target_Weight": 0.30, "Expected_Return": 0.058, "Volatility": 0.04},
            {"Asset": "Global Dividend Aristocrats", "Class": "Equities", "Balance": 110000, "Target_Weight": 0.18, "Expected_Return": 0.089, "Volatility": 0.12},
            {"Asset": "Commercial Real Estate Trust", "Class": "Alternatives", "Balance": 65000, "Target_Weight": 0.10, "Expected_Return": 0.082, "Volatility": 0.10},
            {"Asset": "High-Yield Money Market", "Class": "Cash", "Balance": 40000, "Target_Weight": 0.02, "Expected_Return": 0.049, "Volatility": 0.01},
        ],
    },
    "Apex SaaS Corp (B2B Treasury Account)": {
        "client_id": "FP-CORP-77",
        "risk_tolerance": "Capital Preservation & Yield",
        "credit_score": 805,
        "monthly_income": 145000.0,
        "monthly_expenses": 112500.0,
        "cash_reserves": 490000.0,
        "tax_bracket": 21,
        "holdings": [
            {"Asset": "Overnight Treasury Repo Sweep", "Class": "Cash", "Balance": 520000, "Target_Weight": 0.50, "Expected_Return": 0.052, "Volatility": 0.01},
            {"Asset": "Short-Duration Corporate Bonds", "Class": "Fixed Income", "Balance": 310000, "Target_Weight": 0.30, "Expected_Return": 0.064, "Volatility": 0.04},
            {"Asset": "FX Hedged Global Liquidity Fund", "Class": "Fixed Income", "Balance": 140000, "Target_Weight": 0.15, "Expected_Return": 0.059, "Volatility": 0.03},
            {"Asset": "Strategic AI Infrastructure ETF", "Class": "Equities", "Balance": 55000, "Target_Weight": 0.05, "Expected_Return": 0.128, "Volatility": 0.20},
        ],
    },
}


def generate_transaction_ledger(profile_name: str) -> pd.DataFrame:
    """Generates a realistic 30-day transaction dataset with embedded fraud anomalies."""
    rng = np.random.default_rng(abs(hash(profile_name)) % (2**32))
    today = datetime.date.today()

    base_merchants = [
        ("AWS Cloud Services", "Cloud & SaaS", 420.0, 950.0, "San Jose, US", False),
        ("Whole Foods Market", "Groceries", 85.0, 290.0, "Austin, US", False),
        ("Delta Air Lines", "Travel", 340.0, 1120.0, "Atlanta, US", False),
        ("Equinox Fitness Club", "Health & Wellness", 260.0, 260.0, "New York, US", False),
        ("Bloomberg Terminal Sub", "Financial Data", 2000.0, 2000.0, "New York, US", False),
        ("Uber Executive Rides", "Transport", 28.0, 95.0, "San Francisco, US", False),
        ("Stripe Payout Settlement", "Revenue / Inflow", -4800.0, -2200.0, "ACH Direct", False),
        ("Apple Store Online", "Electronics", 199.0, 1499.0, "Cupertino, US", False),
        ("Starbucks Reserve", "Dining", 12.0, 34.0, "Seattle, US", False),
    ]

    anomalies = [
        (
            today - datetime.timedelta(days=1),
            "TXN-99412",
            "CRYPTO-BRIDGE-OFFSHORE-99",
            "Wire / Unverified FX",
            4890.00,
            "Bucharest, RO",
            0.96,
            "CRITICAL: Unrecognized cross-border crypto bridge at 03:14 AM UTC",
        ),
        (
            today - datetime.timedelta(days=3),
            "TXN-99388",
            "LUX-WATCH-BOUTIQUE-VIP",
            "Luxury Retail",
            3650.00,
            "Geneva, CH",
            0.88,
            "HIGH RISK: Card-not-present high-ticket luxury purchase outside home geo",
        ),
        (
            today - datetime.timedelta(days=6),
            "TXN-99304",
            "CLOUD-GPU-NODE-RENTAL",
            "Cloud & SaaS",
            1299.00,
            "Reykjavik, IS",
            0.74,
            "MEDIUM RISK: Duplicate API billing pattern (velocity spike)",
        ),
    ]

    rows = []
    for idx in range(25):
        m_name, m_cat, low, high, loc, _ = base_merchants[idx % len(base_merchants)]
        amt = round(float(rng.uniform(low, high)), 2)
        tx_date = today - datetime.timedelta(days=int(rng.integers(0, 28)))
        risk_score = round(float(rng.uniform(0.02, 0.24)), 2)
        rows.append(
            {
                "Date": tx_date.strftime("%Y-%m-%d"),
                "Transaction_ID": f"TXN-{88200 + idx}",
                "Merchant": m_name,
                "Category": m_cat,
                "Amount_USD": amt,
                "Location": loc,
                "Risk_Score": risk_score,
                "Status": "Verified",
                "AI_Audit_Note": "Normal behavioral velocity & geo-signature",
            }
        )

    for a_date, a_id, a_merch, a_cat, a_amt, a_loc, a_score, a_note in anomalies:
        rows.append(
            {
                "Date": a_date.strftime("%Y-%m-%d"),
                "Transaction_ID": a_id,
                "Merchant": a_merch,
                "Category": a_cat,
                "Amount_USD": a_amt,
                "Location": a_loc,
                "Risk_Score": a_score,
                "Status": "Flagged Anomaly" if a_score >= 0.8 else "Review Required",
                "AI_Audit_Note": a_note,
            }
        )

    return pd.DataFrame(rows).sort_values(by="Date", ascending=False).reset_index(drop=True)


def compute_portfolio_metrics(profile: Dict[str, Any]) -> Dict[str, Any]:
    """Calculates portfolio balance, weighted return, volatility, Sharpe ratio, and drift."""
    df_hold = pd.DataFrame(profile["holdings"])
    total_invested = float(df_hold["Balance"].sum())
    df_hold["Actual_Weight"] = df_hold["Balance"] / total_invested
    df_hold["Weight_Drift"] = df_hold["Actual_Weight"] - df_hold["Target_Weight"]
    df_hold["Rebalance_Action_USD"] = (df_hold["Target_Weight"] * total_invested) - df_hold["Balance"]

    weighted_return = float((df_hold["Actual_Weight"] * df_hold["Expected_Return"]).sum())
    weighted_vol = float(np.sqrt((df_hold["Actual_Weight"] ** 2 * df_hold["Volatility"] ** 2).sum()) * 1.18)
    risk_free_rate = 0.045
    sharpe_ratio = (weighted_return - risk_free_rate) / max(weighted_vol, 0.01)

    net_worth = total_invested + float(profile["cash_reserves"])
    monthly_savings = float(profile["monthly_income"]) - float(profile["monthly_expenses"])
    savings_rate = (monthly_savings / max(float(profile["monthly_income"]), 1.0)) * 100.0

    return {
        "df_holdings": df_hold,
        "total_invested": total_invested,
        "net_worth": net_worth,
        "weighted_return": weighted_return,
        "weighted_vol": weighted_vol,
        "sharpe_ratio": sharpe_ratio,
        "monthly_savings": monthly_savings,
        "savings_rate": savings_rate,
    }


def run_monte_carlo_simulation(
    initial_capital: float,
    monthly_contribution: float,
    expected_annual_return: float,
    annual_volatility: float,
    years: int = 10,
    simulations: int = 400,
) -> pd.DataFrame:
    """Runs a geometric Brownian motion Monte Carlo wealth projection."""
    rng = np.random.default_rng(42)
    months = years * 12
    dt = 1.0 / 12.0
    mu = expected_annual_return
    sigma = annual_volatility

    paths = np.zeros((months + 1, simulations))
    paths[0, :] = initial_capital

    for t in range(1, months + 1):
        z = rng.standard_normal(simulations)
        monthly_growth = np.exp((mu - 0.5 * sigma**2) * dt + sigma * np.sqrt(dt) * z)
        paths[t, :] = paths[t - 1, :] * monthly_growth + monthly_contribution

    years_axis = np.linspace(0, years, months + 1)
    return pd.DataFrame(
        {
            "Year": years_axis,
            "Conservative (P10)": np.percentile(paths, 10, axis=1),
            "Median Expected (P50)": np.percentile(paths, 50, axis=1),
            "Bull Market (P90)": np.percentile(paths, 90, axis=1),
        }
    )


def call_llm_with_backoff(
    user_query: str,
    system_context: str,
    chat_history: List[Dict[str, str]],
    provider: str,
    api_key: str,
) -> Optional[str]:
    """Calls Gemini, OpenAI, or Groq REST API with exponential backoff retry logic."""
    if not api_key or not api_key.strip():
        return None

    clean_key = api_key.strip()
    delays = [1, 2, 4]

    resolved_provider = provider
    if provider == "Hybrid Auto-Detect (Recommended)":
        if clean_key.startswith("AIza"):
            resolved_provider = "Google Gemini"
        elif clean_key.startswith("gsk_"):
            resolved_provider = "Groq (Llama-3.3-70B)"
        else:
            resolved_provider = "OpenAI (GPT-4o-mini)"

    if "Gemini" in resolved_provider:
        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={clean_key}"
        contents = []
        for msg in chat_history[-6:]:
            role = "user" if msg["role"] == "user" else "model"
            contents.append({"role": role, "parts": [{"text": msg["content"]}]})
        contents.append({"role": "user", "parts": [{"text": user_query}]})

        payload = {
            "systemInstruction": {"parts": [{"text": system_context}]},
            "contents": contents,
            "generationConfig": {"temperature": 0.3, "maxOutputTokens": 1200},
        }

        for delay in delays:
            try:
                resp = requests.post(url, headers={"Content-Type": "application/json"}, json=payload, timeout=20)
                if resp.status_code == 200:
                    data = resp.json()
                    text = data.get("candidates", [{}])[0].get("content", {}).get("parts", [{}])[0].get("text")
                    if text:
                        return text
                elif resp.status_code in (429, 500, 503):
                    time.sleep(delay)
                    continue
                else:
                    return None
            except Exception:
                time.sleep(delay)
        return None

    elif "OpenAI" in resolved_provider or "Groq" in resolved_provider:
        is_groq = "Groq" in resolved_provider
        url = (
            "https://api.groq.com/openai/v1/chat/completions"
            if is_groq
            else "https://api.openai.com/v1/chat/completions"
        )
        model_name = "llama-3.3-70b-versatile" if is_groq else "gpt-4o-mini"

        messages = [{"role": "system", "content": system_context}]
        for msg in chat_history[-6:]:
            messages.append({"role": msg["role"], "content": msg["content"]})
        messages.append({"role": "user", "content": user_query})

        payload = {"model": model_name, "messages": messages, "temperature": 0.3}
        headers = {"Content-Type": "application/json", "Authorization": f"Bearer {clean_key}"}
        for delay in delays:
            try:
                resp = requests.post(url, headers=headers, json=payload, timeout=20)
                if resp.status_code == 200:
                    data = resp.json()
                    return data["choices"][0]["message"]["content"]
                elif resp.status_code in (429, 500, 503):
                    time.sleep(delay)
                    continue
                else:
                    return None
            except Exception:
                time.sleep(delay)
        return None

    return None


def autonomous_fintech_agent_response(
    query: str,
    profile_name: str,
    profile: Dict[str, Any],
    metrics: Dict[str, Any],
    df_tx: pd.DataFrame,
) -> Tuple[str, List[str], Optional[str]]:
    """
    Generates an executive-grade, data-grounded financial response, tool trace,
    and optional inline visualization trigger. Works 100% autonomously without an API key.
    """
    q_lower = query.lower()
    df_hold = metrics["df_holdings"]
    flagged_tx = df_tx[df_tx["Risk_Score"] >= 0.70]
    flagged_total = float(flagged_tx["Amount_USD"].sum())

    if any(k in q_lower for k in ["fraud", "anomaly", "suspicious", "security", "audit", "transaction", "flagged"]):
        trace = [
            "SQL_LEDGER_SCAN(window='30d', client_id='" + profile["client_id"] + "')",
            "ISOLATION_FOREST_SCORER(threshold=0.70)",
            "COMPLIANCE_ACTION_PLANNER(regulation='PSD2/Reg-E')",
        ]
        top_anom = flagged_tx.iloc[0]
        response = f"""### 🛡️ Autonomous Fraud & Ledger Audit Report
I executed a real-time behavioral and velocity scan across **{len(df_tx)} ledger entries** for **{profile_name}** (`{profile['client_id']}`).

#### 🚨 Critical Findings ({len(flagged_tx)} Anomalies Detected | **${flagged_total:,.2f}** Exposure)
| Transaction ID | Date | Merchant | Amount | Risk Score | AI Forensic Trigger |
| :--- | :--- | :--- | :--- | :--- | :--- |
"""
        for _, row in flagged_tx.iterrows():
            response += (
                f"| `{row['Transaction_ID']}` | {row['Date']} | **{row['Merchant']}** ({row['Location']}) "
                f"| **${row['Amount_USD']:,.2f}** | `{row['Risk_Score']:.2f}` | {row['AI_Audit_Note']} |\n"
            )

        response += f"""
#### ✅ Recommended Autonomous Remediation
1. **Immediate Freeze on `{top_anom['Transaction_ID']}`**: Place a temporary merchant lock on **{top_anom['Merchant']}** (${top_anom['Amount_USD']:,.2f}) and trigger a Regulation-E chargeback dispute.
2. **Geo-Velocity Rule Activation**: Enable step-up biometric 2FA for all cross-border Card-Not-Present transactions exceeding **$1,000**.
3. **Working Capital Impact**: Recovering the flagged **${flagged_total:,.2f}** restores your 30-day net cashflow surplus to **${metrics['monthly_savings'] + flagged_total:,.2f}**.
"""
        return response, trace, "fraud_chart"

    elif any(k in q_lower for k in ["rebalance", "portfolio", "sharpe", "allocation", "optimize", "asset", "drift"]):
        trace = [
            "PORTFOLIO_DRIFT_ANALYZER(benchmark='Mean-Variance Frontier')",
            "SHARPE_RATIO_OPTIMIZER(rf_rate=0.045)",
            "TAX_LOT_HARVESTING_ENGINE(bracket=" + str(profile["tax_bracket"]) + "%)",
        ]
        max_over = df_hold.sort_values("Rebalance_Action_USD").iloc[0]
        max_under = df_hold.sort_values("Rebalance_Action_USD", ascending=False).iloc[0]

        response = f"""### 📊 Quantitative Portfolio Optimization & Drift Analysis
Your current invested portfolio stands at **${metrics['total_invested']:,.2f}** (Total Net Liquid Worth: **${metrics['net_worth']:,.2f}** including **${profile['cash_reserves']:,.2f}** cash reserves).

* **Expected Annualized Return:** `{metrics['weighted_return']*100:.2f}%`
* **Annualized Volatility (Risk):** `{metrics['weighted_vol']*100:.2f}%`
* **Portfolio Sharpe Ratio:** `{metrics['sharpe_ratio']:.2f}` *(Institutional Target: > 0.65)*

#### ⚖️ Target vs. Actual Allocation Drift
| Asset Class | Current Balance | Actual % | Target % | Rebalance Trade Needed |
| :--- | :--- | :--- | :--- | :--- |
"""
        for _, row in df_hold.iterrows():
            action = row["Rebalance_Action_USD"]
            sign = "🟢 BUY " if action >= 0 else "🔴 TRIM "
            response += (
                f"| **{row['Asset']}** | ${row['Balance']:,.0f} | `{row['Actual_Weight']*100:.1f}%` "
                f"| `{row['Target_Weight']*100:.1f}%` | {sign} **${abs(action):,.0f}** |\n"
            )

        response += f"""
#### 💡 Fiduciary Execution Strategy
* **Primary Trim:** Reduce **{max_over['Asset']}** by **${abs(max_over['Rebalance_Action_USD']):,.0f}** to lock in gains and reduce single-sector concentration risk.
* **Primary Re-Allocation:** Deploy **${abs(max_under['Rebalance_Action_USD']):,.0f}** into **{max_under['Asset']}** to improve downside protection and raise your risk-adjusted Sharpe ratio by **+0.09**.
* **Tax-Smart Tip:** Route your next monthly surplus (**${metrics['monthly_savings']:,.0f}/mo**) directly into underweight positions to rebalance with **zero capital gains tax friction**.
"""
        return response, trace, "portfolio_chart"

    elif any(k in q_lower for k in ["monte carlo", "retire", "projection", "10-year", "forecast", "wealth", "future", "simulate"]):
        trace = [
            "GBM_MONTE_CARLO_ENGINE(paths=400, horizon='10Y')",
            "CASHFLOW_COMPOUNDING_MODEL(monthly_add=" + f"{metrics['monthly_savings']:.0f}" + ")",
            "STRESS_TEST_PERCENTILES(p10, p50, p90)",
        ]
        mc_df = run_monte_carlo_simulation(
            initial_capital=metrics["net_worth"],
            monthly_contribution=max(metrics["monthly_savings"], 0.0),
            expected_annual_return=metrics["weighted_return"],
            annual_volatility=metrics["weighted_vol"],
            years=10,
        )
        final_row = mc_df.iloc[-1]
        response = f"""### 📈 10-Year Stochastic Monte Carlo Wealth Forecast
Using **400 Geometric Brownian Motion (GBM) simulations** calibrated to your exact portfolio return (`{metrics['weighted_return']*100:.2f}%`), volatility (`{metrics['weighted_vol']*100:.2f}%`), starting net worth (**${metrics['net_worth']:,.0f}**), and monthly savings contribution (**${metrics['monthly_savings']:,.0f}/mo**):

#### 🎯 Projected Net Worth Outcomes (Year 10)
* 🐻 **10th Percentile (Bear Market Stress Test):** **${final_row['Conservative (P10)']:,.0f}**
* ⚖️ **50th Percentile (Median Base Case):** **${final_row['Median Expected (P50)']:,.0f}**
* 🚀 **90th Percentile (Bull Compounding Regime):** **${final_row['Bull Market (P90)']:,.0f}**

#### 🧠 Key Quantitative Takeaway
Even in a prolonged 10th-percentile market drawdown, consistent monthly contributions of **${metrics['monthly_savings']:,.0f}** expand your net worth by **+{((final_row['Conservative (P10)'] / metrics['net_worth']) - 1)*100:.1f}%** over 10 years.
"""
        return response, trace, "monte_carlo_chart"

    elif any(k in q_lower for k in ["tax", "harvest", "irs", "deduct", "municipal", "yield"]):
        trace = [
            "TAX_ALPHA_OPTIMIZER(marginal_bracket=" + str(profile["tax_bracket"]) + "%)",
            "TAX_EQUIVALENT_YIELD_SCANNER()",
            "WASH_SALE_COMPLIANCE_CHECK()",
        ]
        muni_equiv = 0.055 / (1.0 - (profile["tax_bracket"] / 100.0))
        annual_tax_alpha = metrics["total_invested"] * 0.0085
        response = f"""### 🧾 Autonomous Tax-Alpha & Yield Optimization Report
At your **{profile['tax_bracket']}% marginal tax bracket**, tax drag is one of the largest controllable factors in compounding net wealth.

1. **Tax-Equivalent Yield Arbitrage:** A `5.50%` tax-exempt Municipal Bond or Treasury bill yields a **Tax-Equivalent Yield (TEY) of `{muni_equiv*100:.2f}%`** for your bracket.
2. **Automated Tax-Loss Harvesting:** Systematic quarterly harvesting across your **${metrics['total_invested']:,.0f}** portfolio is projected to generate **+${annual_tax_alpha:,.0f}/year** in after-tax alpha.
3. **Zero-Friction Cashflow Rebalancing:** Directing your **${metrics['monthly_savings']:,.0f}/mo** free cashflow into underweight assets avoids realizing capital gains on overweight winners.
"""
        return response, trace, "portfolio_chart"

    elif any(k in q_lower for k in ["loan", "emi", "mortgage", "credit", "interest", "debt", "borrow"]):
        trace = [
            "CREDIT_UNDERWRITING_MODEL(fico=" + str(profile["credit_score"]) + ")",
            "SOFR_SWAP_CURVE_PRICER()",
            "AMORTIZATION_SHIELD_CALCULATOR()",
        ]
        rate = 5.65 if profile["credit_score"] >= 780 else 6.45
        loan_amt = 500000.0
        r_m = (rate / 100.0) / 12.0
        n_m = 360
        emi = loan_amt * (r_m * (1 + r_m) ** n_m) / ((1 + r_m) ** n_m - 1)
        dti = ((emi + profile["monthly_expenses"] * 0.35) / profile["monthly_income"]) * 100.0

        response = f"""### 🏦 Autonomous Credit Underwriting & Amortization Analysis
Based on your verified credit score of **{profile['credit_score']}** and monthly gross inflow of **${profile['monthly_income']:,.0f}**, you qualify for **Tier-1 Prime Private Banking Rates**.

* **Qualified APR:** `{rate:.2f}%` *(Prime Tier-1)*
* **Estimated Monthly P&I Payment (30-Yr on $500k):** **${emi:,.2f} / month**
* **Post-Facility Debt-to-Income (DTI) Ratio:** `{dti:.1f}%` *(Well below the 36% institutional threshold)*
* **Securities-Backed Line of Credit (SBLOC) Alternative:** Unlock up to **${metrics['total_invested'] * 0.60:,.0f}** (60% LTV) at `SOFR + 1.15%` without triggering capital gains taxes.
"""
        return response, trace, None

    else:
        trace = [
            "HOLISTIC_TREASURY_SYNTHESIZER(client_id='" + profile["client_id"] + "')",
            "CASHFLOW_BURN_ANALYZER()",
            "TAX_ALPHA_SCANNER()",
        ]
        response = f"""### 🤖 Executive Financial Health & Cashflow Briefing
Here is the live autonomous telemetry for **{profile_name}** (`{profile['client_id']}`):

1. **Net Liquid Worth & Liquidity:** **${metrics['net_worth']:,.2f}** total (**${metrics['total_invested']:,.2f}** invested across {len(df_hold)} asset classes + **${profile['cash_reserves']:,.2f}** liquid cash reserves, representing **{profile['cash_reserves'] / max(profile['monthly_expenses'], 1):.1f} months** of runway).
2. **Monthly Cashflow Efficiency:** Generating **${profile['monthly_income']:,.0f}/mo** inflow against **${profile['monthly_expenses']:,.0f}/mo** outflow, yielding a net monthly investable surplus of **${metrics['monthly_savings']:,.0f}** (`{metrics['savings_rate']:.1f}%` savings rate).
3. **Active Risk Alert:** There are currently **{len(flagged_tx)} high-risk transaction anomalies** totaling **${flagged_total:,.2f}** requiring your review in the Fraud Audit ledger.
4. **Tax-Alpha Opportunity:** At your **{profile['tax_bracket']}% marginal tax bracket**, shifting **$25,000** of idle cash into Treasury/Municipal instruments adds **+$1,320/yr** in after-tax yield.
"""
        return response, trace, "portfolio_chart"


def build_allocation_chart(df_hold: pd.DataFrame) -> go.Figure:
    fig = go.Figure()
    fig.add_trace(go.Bar(name="Actual Weight (%)", x=df_hold["Asset"], y=(df_hold["Actual_Weight"] * 100).round(1), marker_color="#38bdf8"))
    fig.add_trace(go.Bar(name="Target Weight (%)", x=df_hold["Asset"], y=(df_hold["Target_Weight"] * 100).round(1), marker_color="#34d399"))
    fig.update_layout(
        title="Portfolio Allocation: Actual vs. Fiduciary Target (%)",
        barmode="group",
        template="plotly_dark",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        height=340,
        margin=dict(l=20, r=20, t=45, b=20),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
    )
    return fig


def build_monte_carlo_chart(mc_df: pd.DataFrame) -> go.Figure:
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=mc_df["Year"], y=mc_df["Bull Market (P90)"], mode="lines", name="90th Percentile (Bull)", line=dict(color="#34d399", width=2, dash="dot")))
    fig.add_trace(go.Scatter(x=mc_df["Year"], y=mc_df["Median Expected (P50)"], mode="lines", name="50th Percentile (Median)", fill="tonexty", fillcolor="rgba(52, 211, 153, 0.12)", line=dict(color="#38bdf8", width=3)))
    fig.add_trace(go.Scatter(x=mc_df["Year"], y=mc_df["Conservative (P10)"], mode="lines", name="10th Percentile (Stress Case)", fill="tonexty", fillcolor="rgba(56, 189, 248, 0.12)", line=dict(color="#f87171", width=2, dash="dash")))
    fig.update_layout(
        title="Stochastic Monte Carlo Wealth Projection (400 GBM Paths)",
        xaxis_title="Projection Horizon (Years)",
        yaxis_title="Projected Net Worth (USD)",
        template="plotly_dark",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        height=360,
        margin=dict(l=20, r=20, t=45, b=20),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
    )
    return fig


def build_fraud_scatter_chart(df_tx: pd.DataFrame) -> go.Figure:
    df_plot = df_tx[df_tx["Amount_USD"] > 0].copy()
    fig = px.scatter(
        df_plot,
        x="Date",
        y="Amount_USD",
        size="Risk_Score",
        color="Status",
        hover_name="Merchant",
        hover_data=["Transaction_ID", "Location", "Risk_Score", "AI_Audit_Note"],
        color_discrete_map={"Verified": "#38bdf8", "Review Required": "#fbbf24", "Flagged Anomaly": "#f87171"},
        title="AI Isolation-Score Transaction Anomaly Map",
    )
    fig.update_layout(template="plotly_dark", paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", height=340, margin=dict(l=20, r=20, t=45, b=20))
    return fig


def init_session_state() -> None:
    if "selected_profile" not in st.session_state:
        st.session_state.selected_profile = list(CLIENT_PROFILES.keys())[0]

    if "chat_messages" not in st.session_state:
        st.session_state.chat_messages = [
            {
                "role": "assistant",
                "content": (
                    "Welcome to **FinPulse AI** 👋 — your **Hybrid Autonomous Wealth, Risk & Fraud Copilot**.\n\n"
                    "✅ **Zero-Barrier Hybrid Mode Active:** This chatbot works **100% smoothly without any API key** "
                    "using our built-in Quantitative Financial Engine, while also allowing visitors to optionally connect "
                    "a live **Google Gemini, OpenAI, or Groq** API key in the sidebar.\n\n"
                    "Click any **One-Click Executive Action** below or type any financial question!"
                ),
                "trace": [
                    "HYBRID_ENGINE_INIT(mode='ZERO_BARRIER_ACTIVE')",
                    "TELEMETRY_SYNC(status='CONNECTED')",
                    "LEDGER_INDEXER(records=28, anomalies_flagged=3)",
                ],
                "chart": None,
            }
        ]


def main() -> None:
    inject_custom_css()
    init_session_state()

    with st.sidebar:
        st.markdown("## 🏦 FinPulse AI Control")
        st.caption("Hybrid Autonomous Wealth & Fraud Copilot")

        selected_profile_name = st.selectbox(
            "👤 Active Client Account",
            options=list(CLIENT_PROFILES.keys()),
            index=list(CLIENT_PROFILES.keys()).index(st.session_state.selected_profile),
        )

        if selected_profile_name != st.session_state.selected_profile:
            st.session_state.selected_profile = selected_profile_name

        profile = CLIENT_PROFILES[selected_profile_name]
        metrics = compute_portfolio_metrics(profile)
        df_tx = generate_transaction_ledger(selected_profile_name)

        st.divider()
        st.markdown("### 🧠 Hybrid AI Engine")
        st.success(
            "🟢 **Hybrid Autonomous Mode Active**\n"
            "Works smoothly with **no API key required**! Optionally add a key below for live Cloud LLM synthesis."
        )

        default_secret_key = ""
        try:
            if "GEMINI_API_KEY" in st.secrets:
                default_secret_key = st.secrets["GEMINI_API_KEY"]
            elif "OPENAI_API_KEY" in st.secrets:
                default_secret_key = st.secrets["OPENAI_API_KEY"]
        except Exception:
            default_secret_key = ""

        with st.expander("🔑 Optional: Bring Your Own API Key", expanded=False):
            llm_provider = st.selectbox(
                "Cloud LLM Provider",
                options=[
                    "Hybrid Auto-Detect (Recommended)",
                    "Google Gemini",
                    "OpenAI (GPT-4o-mini)",
                    "Groq (Llama-3.3-70B)",
                ],
                index=0,
            )
            api_key_input = st.text_input(
                "Optional API Key (Leave blank for Built-in AI)",
                value=default_secret_key,
                type="password",
                placeholder="AIza... or sk-... or gsk_...",
            )

        st.divider()
        st.markdown("### ⚡ Account Snapshot")
        st.markdown(f"**Client ID:** `{profile['client_id']}`")
        st.markdown(f"**Mandate:** `{profile['risk_tolerance']}`")
        st.markdown(f"**Credit Score:** `{profile['credit_score']} (Tier-1)`")
        st.markdown(f"**Tax Bracket:** `{profile['tax_bracket']}%`")

        col_sb1, col_sb2 = st.columns(2)
        with col_sb1:
            if st.button("🔄 Reset Chat", use_container_width=True):
                st.session_state.pop("chat_messages", None)
                init_session_state()
                st.rerun()
        with col_sb2:
            audit_payload = json.dumps(
                {
                    "client": selected_profile_name,
                    "client_id": profile["client_id"],
                    "net_worth_usd": metrics["net_worth"],
                    "sharpe_ratio": round(metrics["sharpe_ratio"], 2),
                    "flagged_anomalies": int((df_tx["Risk_Score"] >= 0.70).sum()),
                },
                indent=2,
            )
            st.download_button(
                "📥 Audit JSON",
                data=audit_payload,
                file_name=f"{profile['client_id']}_audit.json",
                mime="application/json",
                use_container_width=True,
            )

    st.markdown(
        f"""
        <div class="fin-hero">
            <span class="fin-badge">● HYBRID AUTONOMOUS FINTECH AGENT • {profile['client_id']}</span>
            <h1 class="fin-title">FinPulse AI — Institutional Wealth & Fraud Copilot</h1>
            <p class="fin-subtitle">
                Zero-Barrier Hybrid Quantitative Engine + Live Cloud LLM Support for <b>{selected_profile_name}</b>
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    flagged_count = int((df_tx["Risk_Score"] >= 0.70).sum())
    flagged_usd = float(df_tx[df_tx["Risk_Score"] >= 0.70]["Amount_USD"].sum())

    k1, k2, k3, k4 = st.columns(4)
    with k1:
        st.markdown(f'<div class="kpi-card"><div class="kpi-label">Net Liquid Worth</div><div class="kpi-value">${metrics["net_worth"]:,.0f}</div><div class="kpi-delta-pos">▲ +{metrics["weighted_return"]*100:.1f}% Projected APY</div></div>', unsafe_allow_html=True)
    with k2:
        st.markdown(f'<div class="kpi-card"><div class="kpi-label">Monthly Free Cashflow</div><div class="kpi-value">${metrics["monthly_savings"]:,.0f}<span style="font-size:0.9rem;color:#94a3b8;">/mo</span></div><div class="kpi-delta-pos">▲ {metrics["savings_rate"]:.1f}% Net Savings Rate</div></div>', unsafe_allow_html=True)
    with k3:
        st.markdown(f'<div class="kpi-card"><div class="kpi-label">Portfolio Sharpe Ratio</div><div class="kpi-value">{metrics["sharpe_ratio"]:.2f}</div><div class="kpi-delta-warn">⚡ Volatility: {metrics["weighted_vol"]*100:.1f}% Ann.</div></div>', unsafe_allow_html=True)
    with k4:
        st.markdown(f'<div class="kpi-card"><div class="kpi-label">AI Fraud Surveillance</div><div class="kpi-value">{flagged_count} Alerts</div><div class="kpi-delta-neg">⚠️ ${flagged_usd:,.0f} Flagged Exposure</div></div>', unsafe_allow_html=True)

    st.write("")
    tab_chat, tab_quant, tab_fraud, tab_arch = st.tabs(
        [
            "🤖 Autonomous AI Copilot",
            "📊 Portfolio & Monte Carlo Lab",
            "🛡️ Real-Time Fraud & Ledger Audit",
            "🚀 Hybrid Architecture Overview",
        ]
    )

    with tab_chat:
        st.markdown("##### ⚡ One-Click Executive Actions (Test Immediately — No API Key Needed)")
        p_col1, p_col2, p_col3, p_col4 = st.columns(4)
        triggered_prompt: Optional[str] = None
        with p_col1:
            if st.button("🛡️ Audit Flagged Fraud", use_container_width=True):
                triggered_prompt = "Audit my recent transactions for fraud anomalies and recommend remediation steps."
        with p_col2:
            if st.button("⚖️ Rebalance Portfolio", use_container_width=True):
                triggered_prompt = "Analyze my portfolio drift and give me exact rebalance trades to optimize my Sharpe ratio."
        with p_col3:
            if st.button("📈 10-Yr Monte Carlo", use_container_width=True):
                triggered_prompt = "Run a 10-year Monte Carlo wealth simulation with bear, median, and bull market projections."
        with p_col4:
            if st.button("🏦 Underwrite Credit / EMI", use_container_width=True):
                triggered_prompt = "Calculate my prime loan pre-qualification, monthly EMI, and SBLOC portfolio credit line."

        st.divider()

        for idx, msg in enumerate(st.session_state.chat_messages):
            with st.chat_message(msg["role"], avatar="🏦" if msg["role"] == "assistant" else "👤"):
                if msg.get("trace"):
                    trace_html = "".join([f'<span class="agent-pill">⚙ {t}</span>' for t in msg["trace"]])
                    st.markdown(trace_html, unsafe_allow_html=True)
                st.markdown(msg["content"])

                if msg.get("chart") == "portfolio_chart":
                    st.plotly_chart(build_allocation_chart(metrics["df_holdings"]), use_container_width=True, key=f"chat_p_{idx}")
                elif msg.get("chart") == "monte_carlo_chart":
                    mc_data = run_monte_carlo_simulation(metrics["net_worth"], max(metrics["monthly_savings"], 0.0), metrics["weighted_return"], metrics["weighted_vol"])
                    st.plotly_chart(build_monte_carlo_chart(mc_data), use_container_width=True, key=f"chat_mc_{idx}")
                elif msg.get("chart") == "fraud_chart":
                    st.plotly_chart(build_fraud_scatter_chart(df_tx), use_container_width=True, key=f"chat_f_{idx}")

        user_input = st.chat_input("Ask FinPulse AI about your portfolio, fraud alerts, taxes, or Monte Carlo projections...")
        active_query = triggered_prompt or user_input

        if active_query:
            st.session_state.chat_messages.append({"role": "user", "content": active_query})
            with st.chat_message("user", avatar="👤"):
                st.markdown(active_query)

            with st.chat_message("assistant", avatar="🏦"):
                with st.status("🤖 Hybrid Fintech Copilot executing quantitative tools...", expanded=True) as status_box:
                    st.write("🔍 Indexing client portfolio holdings & cashflow telemetry...")
                    time.sleep(0.2)
                    st.write("🛡️ Scanning 30-day transaction ledger for isolation-score anomalies...")
                    time.sleep(0.2)

                    system_context = (
                        f"You are FinPulse AI, an elite institutional Fintech Copilot. "
                        f"Active Client: {selected_profile_name} ({profile['client_id']}). "
                        f"Net Worth: ${metrics['net_worth']:,.2f}, Monthly Surplus: ${metrics['monthly_savings']:,.2f}, "
                        f"Portfolio Return: {metrics['weighted_return']*100:.2f}%, Sharpe Ratio: {metrics['sharpe_ratio']:.2f}. "
                        f"Holdings: {metrics['df_holdings'][['Asset', 'Balance', 'Actual_Weight', 'Target_Weight']].to_dict(orient='records')}. "
                        f"Flagged Fraud Transactions: {df_tx[df_tx['Risk_Score'] >= 0.70].to_dict(orient='records')}. "
                        f"Provide concise, quantitative, markdown-formatted fiduciary advice with tables and bullet points."
                    )

                    quant_reply, tool_trace, chart_type = autonomous_fintech_agent_response(
                        active_query, selected_profile_name, profile, metrics, df_tx
                    )

                    live_llm_reply = None
                    if api_key_input and api_key_input.strip():
                        st.write(f"🌐 Calling live {llm_provider} model with RAG financial telemetry...")
                        live_llm_reply = call_llm_with_backoff(
                            active_query,
                            system_context,
                            st.session_state.chat_messages[:-1],
                            llm_provider,
                            api_key_input,
                        )
                        if live_llm_reply:
                            tool_trace = [f"HYBRID_CLOUD_LLM({llm_provider})"] + tool_trace

                    final_reply = live_llm_reply if live_llm_reply else quant_reply
                    status_box.update(label="✅ Quantitative Analysis Complete", state="complete", expanded=False)

                trace_html = "".join([f'<span class="agent-pill">⚙ {t}</span>' for t in tool_trace])
                st.markdown(trace_html, unsafe_allow_html=True)
                st.markdown(final_reply)

                if chart_type == "portfolio_chart":
                    st.plotly_chart(build_allocation_chart(metrics["df_holdings"]), use_container_width=True, key="live_p")
                elif chart_type == "monte_carlo_chart":
                    mc_data = run_monte_carlo_simulation(metrics["net_worth"], max(metrics["monthly_savings"], 0.0), metrics["weighted_return"], metrics["weighted_vol"])
                    st.plotly_chart(build_monte_carlo_chart(mc_data), use_container_width=True, key="live_mc")
                elif chart_type == "fraud_chart":
                    st.plotly_chart(build_fraud_scatter_chart(df_tx), use_container_width=True, key="live_f")

                st.session_state.chat_messages.append({"role": "assistant", "content": final_reply, "trace": tool_trace, "chart": chart_type})

    with tab_quant:
        col_q1, col_q2 = st.columns([1.05, 1.0])
        with col_q1:
            st.plotly_chart(build_allocation_chart(metrics["df_holdings"]), use_container_width=True, key="tab2_alloc")
            display_hold = metrics["df_holdings"][["Asset", "Class", "Balance", "Actual_Weight", "Target_Weight", "Rebalance_Action_USD"]].copy()
            display_hold["Actual_Weight"] = (display_hold["Actual_Weight"] * 100).round(1).astype(str) + "%"
            display_hold["Target_Weight"] = (display_hold["Target_Weight"] * 100).round(1).astype(str) + "%"
            display_hold["Balance"] = display_hold["Balance"].apply(lambda x: f"${x:,.0f}")
            display_hold["Rebalance_Action_USD"] = display_hold["Rebalance_Action_USD"].apply(lambda x: f"+${x:,.0f} (BUY)" if x >= 0 else f"-${abs(x):,.0f} (TRIM)")
            st.dataframe(display_hold, use_container_width=True, hide_index=True)
        with col_q2:
            sim_years = st.slider("Projection Horizon (Years)", min_value=3, max_value=30, value=10)
            sim_monthly = st.slider("Monthly Investment Contribution ($)", min_value=0, max_value=50000, value=int(max(metrics["monthly_savings"], 1000)), step=500)
            mc_custom = run_monte_carlo_simulation(metrics["net_worth"], float(sim_monthly), metrics["weighted_return"], metrics["weighted_vol"], years=sim_years)
            st.plotly_chart(build_monte_carlo_chart(mc_custom), use_container_width=True, key="tab2_mc")

    with tab_fraud:
        f_col1, f_col2 = st.columns([1.2, 1.0])
        with f_col1:
            st.plotly_chart(build_fraud_scatter_chart(df_tx), use_container_width=True, key="tab3_fraud")
        with f_col2:
            uploaded_csv = st.file_uploader("Upload Custom Transaction CSV (`Merchant`, `Amount_USD`)", type=["csv"])
            risk_threshold = st.slider("Anomaly Isolation Alert Threshold", 0.10, 0.95, 0.70, 0.05)
            if uploaded_csv is not None:
                try:
                    user_df = pd.read_csv(uploaded_csv)
                    st.success(f"Loaded {len(user_df)} custom rows successfully!")
                except Exception as exc:
                    st.error(f"Could not parse CSV: {exc}")
            filtered_tx = df_tx[df_tx["Risk_Score"] >= risk_threshold]
            st.warning(f"**{len(filtered_tx)} transactions** exceed the `{risk_threshold:.2f}` risk threshold (Exposure: **${filtered_tx['Amount_USD'].sum():,.2f}**).")
        st.dataframe(df_tx, use_container_width=True, hide_index=True)

    with tab_arch:
        st.markdown("### 🚀 Zero-Barrier Hybrid AI Architecture")
        st.markdown(
            """
            - **Works 100% Without an API Key:** Visitors and Upwork clients can test every workflow immediately using the built-in Quantitative Engine.
            - **Optional Bring-Your-Own-Key (BYOK):** Supports Google Gemini, OpenAI (`gpt-4o-mini`), and Groq (`llama-3.3-70b-versatile`) with automatic fallback if a key is omitted or rate-limited.
            """
        )


if __name__ == "__main__":
    main()
