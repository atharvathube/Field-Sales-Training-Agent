# File: utils/agent_mode.py
import streamlit as st
from utils.gemini_helper import get_gemini_response
from utils.client_profile_parser import extract_client_info

def run_agent_mode():
    st.subheader("🧑‍💼 Advisor Mode – Sales Pitch Generator")

    if "client_profile_raw" in st.session_state:
        profile = extract_client_info(st.session_state.client_profile_raw)
        name = profile.get("name", "Client")
        age = profile.get("age", 30)
        marital_status = profile.get("marital_status", "Single")
        income = profile.get("income", 100000)
        health_issues = profile.get("health_issues", [])
        goal = profile.get("goal", "Life Protection")
        objection = ""
    else:
        name = st.text_input("Client's Name", value="Client")
        age = st.slider("Client's Age", 18, 100)
        marital_status = st.selectbox("Marital Status", ["Single", "Married", "Divorced", "Widowed"])
        income = st.number_input("Annual Income (₹)", min_value=0, step=10000)
        health_issues = st.multiselect("Health Issues", ["Diabetes", "Heart Disease", "Hypertension", "Asthma", "None"])
        goal = st.selectbox("Client's Insurance Goal", [
            "Life Protection", "Health Security", "Tax Saving", "Retirement Planning", "Child Education"
        ])
        objection = st.text_area("Client's Objection / Question", placeholder="e.g., I'm not sure this is affordable.")

    if st.button("Generate Pitch"):
        health_summary = ", ".join(health_issues) if health_issues else "None"

        prompt = f"""
        You are an insurance advisor preparing a personalized pitch.

        Client Details:
        - Name: {name}
        - Age: {age}
        - Marital Status: {marital_status}
        - Annual Income: ₹{income}
        - Health Issues: {health_summary}
        - Insurance Goal: {goal}
        {'- Objection/Question: ' + objection if objection else ''}

        Generate a concise, friendly sales pitch tailored to this client.

        Output:
        - Personalized pitch
        - How to address the client's objection/question (if any)
        """

        pitch = get_gemini_response(prompt)
        st.markdown("### 🗣️ AI-Powered Sales Pitch")
        st.write(pitch)
