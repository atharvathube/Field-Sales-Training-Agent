# File: utils/risk_assessment.py
import streamlit as st
from utils.gemini_helper import get_gemini_response
from utils.client_profile_parser import extract_client_info

def run_risk_assessment():
    st.subheader("📊 Dynamic Risk Assessment")

    if "client_profile_raw" in st.session_state:
        profile = extract_client_info(st.session_state.client_profile_raw)
        age = profile.get("age")
        if age is None:
            age = 30  # default fallback
        occupation = profile.get("occupation", "Field-Based")
        health_conditions = profile.get("health_issues", [])
        income = profile.get("income", 0)

        score = 0
        if age > 60: score += 2
        if any(x in occupation.lower() for x in ["manual", "driver", "construction", "mining", "enforcement", "security"]):
            score += 2
            occupation_category = "⚙️ Manual / Labor-Intensive"
        else:
            occupation_category = occupation

        score += len(health_conditions)

        risk_level = "Low" if score <= 2 else "Medium" if score <= 4 else "High"
        st.success(f"🏷️ Your assessed risk level is: **{risk_level}**")

        prompt = f"""
        A customer is being evaluated for insurance risk.

        Details:
        - Age: {age}
        - Occupation: {occupation_category}
        - Health conditions: {', '.join(health_conditions) or 'None'}
        - Income: ₹{income or 'Not provided'}

        Their calculated risk level is **{risk_level}**.
        Explain simply why this risk level was given.
        """
        explanation = get_gemini_response(prompt)
        st.markdown("### 🤖 AI Explanation")
        st.write(explanation)

    else:
        with st.form("risk_form"):
            age = st.slider("Age", 18, 100)

            occupation = st.selectbox("Occupation Type", [
                "🪑 Sedentary", 
                "🚶‍♂️ Field-Based", 
                "⚙️ Manual / Labor-Intensive", 
                "🤝 Interpersonal / Client-Facing", 
                "🏥 Healthcare / Medical", 
                "🛡️ Security / Enforcement", 
                "✈️ Travel-Intensive", 
                "🎨 Creative / Artistic"
            ])

            health_conditions = st.multiselect("Health Conditions", ["Diabetes", "Heart Disease", "Hypertension", "Asthma"])
            income = st.number_input("Annual Income (optional)", min_value=0, step=10000, format="%d")
            submitted = st.form_submit_button("Assess Risk")

        if submitted:
            score = 0
            if age > 60: score += 2
            if occupation in ["⚙️ Manual / Labor-Intensive", "🛡️ Security / Enforcement"]:
                score += 2
            score += len(health_conditions)

            risk_level = "Low" if score <= 2 else "Medium" if score <= 4 else "High"
            st.success(f"🏷️ Your assessed risk level is: **{risk_level}**")

            prompt = f"""
            A customer is being evaluated for insurance risk.

            Details:
            - Age: {age}
            - Occupation: {occupation}
            - Health conditions: {', '.join(health_conditions) or 'None'}
            - Income: ₹{income or 'Not provided'}

            Their calculated risk level is **{risk_level}**.
            Explain simply why this risk level was given.
            """
            explanation = get_gemini_response(prompt)
            st.markdown("### 🤖 AI Explanation")
            st.write(explanation)
