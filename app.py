# File: app.py

import streamlit as st
from utils.risk_assessment import run_risk_assessment
from utils.recommend_products import run_product_recommendation
from utils.claim_advisor import run_claim_advisor
from utils.agent_mode import run_agent_mode

# Sidebar Navigation
st.set_page_config(page_title="BFSI GenAI Assistant", layout="wide")
st.title("🤖 GenAI Assistant")

st.sidebar.title("🔍 Choose a Feature")

app_mode = st.sidebar.radio("Go to", [
    "🏠 Home",
    "📊 Risk Assessment",
    "🛡️ Product Recommendation",
    "📄 Claim Readiness Advisor",
    "🧑‍💼 Agent Advisor Mode",
    "🎓 Field Sales Training Agent"

])

if app_mode == "🏠 Home":
    st.markdown("""
    ## 👋 Welcome to the BFSI GenAI Assistant
    This intelligent assistant is designed to help both **customers** and **field agents** in the Insurance & BFSI domain.

    ### 💼 Features:
    - **Risk Assessment**: Know your insurance risk category
    - **Product Recommendation**: Get AI-based insurance plan suggestions
    - **Claim Advisor**: Checklist for document readiness
    - **Agent Mode**: Personalized sales pitch generator

    > Built with 💡 using Streamlit + OpenAI GPT-4o
    """)

elif app_mode == "📊 Risk Assessment":
    run_risk_assessment()

elif app_mode == "🛡️ Product Recommendation":
    run_product_recommendation()

elif app_mode == "📄 Claim Readiness Advisor":
    run_claim_advisor()

elif app_mode == "🧑‍💼 Agent Advisor Mode":
    run_agent_mode()

elif app_mode == "🎓 Field Sales Training Agent":
    from utils.training_agent import run_field_sales_training
    run_field_sales_training()

