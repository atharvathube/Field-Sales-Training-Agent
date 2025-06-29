# File: utils/claim_advisor.py
import streamlit as st
from utils.gemini_helper import get_gemini_response
from utils.client_profile_parser import extract_client_info

def run_claim_advisor():
    st.subheader("📄 Claim Readiness Advisor")

    if "client_profile_raw" in st.session_state:
        profile = extract_client_info(st.session_state.client_profile_raw)
        policy_type = "Life Insurance" if "life" in str(profile.get("existing_policies", "")).lower() else "Health Insurance"
        st.info(f"Autodetected policy type from profile: {policy_type}")
        prompt = f"""
        A user wants to file a claim for **{policy_type}**.

        Provide a checklist of required documents with simple explanations for each item.
        """
        checklist = get_gemini_response(prompt)
        st.markdown("### ✅ Claim Checklist")
        st.write(checklist)
    else:
        with st.form("claim_form"):
            policy_type = st.selectbox("Select your policy type:", [
                "Health Insurance", "Life Insurance", "Vehicle Insurance", "Term Plan"
            ])
            uploaded_file = st.file_uploader("📎 Upload your policy PDF (optional)", type=["pdf"])
            submitted = st.form_submit_button("Generate Checklist")
        if submitted:
            prompt = f"""
            A user wants to file a claim for **{policy_type}**.

            Provide a checklist of required documents with simple explanations for each item.
            """
            checklist = get_gemini_response(prompt)
            st.markdown("### ✅ Claim Checklist")
            st.write(checklist)
