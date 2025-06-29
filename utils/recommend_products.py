# File: utils/recommend_products.py
import streamlit as st
from utils.gemini_helper import get_gemini_response
from utils.client_profile_parser import extract_client_info

def run_product_recommendation():
    st.subheader("🛡️ Insurance Product Recommendation")

    if "client_profile_raw" in st.session_state:
        profile = extract_client_info(st.session_state.client_profile_raw)
        goal = profile.get("goal", "Life Protection")
        risk_level = "High" if any(x in str(profile.get("health_issues", [])).lower() for x in ["chronic", "serious"]) else "Medium"
        budget = profile.get("income", 100000) // 10
    else:
        with st.form("product_form"):
            goal = st.selectbox("What is your primary insurance goal?", [
                "Life Protection", "Health Security", "Tax Saving", "Retirement Planning", "Child Education"
            ])
            risk_level = st.radio("Your risk level", ["Low", "Medium", "High"])
            budget = st.number_input("Your annual premium budget (₹)", min_value=100, step=1000)
            submitted = st.form_submit_button("Get Recommendation")
        if not submitted:
            return

    prompt = f"""
    Suggest an insurance product for a customer with the following:
    - Goal: {goal}
    - Risk level: {risk_level}
    - Annual Budget: ₹{budget}

    Output:
    - Product Name
    - Type of Policy
    - Why this product fits
    - Optional: 1-2 alternative options with pros/cons
    """
    answer = get_gemini_response(prompt)
    st.markdown("### 🤖 AI Suggested Product")
    st.write(answer)
