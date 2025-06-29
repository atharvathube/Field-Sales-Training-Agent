import streamlit as st
from utils.gemini_helper import get_gemini_response
import json

def format_chat_history(history):
    return "\n".join([
        f"{'Agent' if m['role'] == 'agent' else 'Client'}: {m['content']}"
        for m in history
    ])

def download_chat_button(history):
    if not history:
        return
    formatted = format_chat_history(history)
    st.download_button(
        label="📅 Download Chat History",
        data=formatted,
        file_name="field_sales_chat_history.txt",
        mime="text/plain"
    )

def save_chat_to_file(history, file_path="chat_history.json"):
    if not history:
        return
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(history, f, indent=2)

def run_field_sales_training():
    st.subheader("🎓 Field Sales Training Agent (Autonomous Client Mode)")

    # Initialize session state
    if "history" not in st.session_state:
        st.session_state.history = []
    if "client_profile" not in st.session_state:
        st.session_state.client_profile = None
    if "client_done" not in st.session_state:
        st.session_state.client_done = False
    if "hint_index" not in st.session_state:
        st.session_state.hint_index = None
    if "show_info" not in st.session_state:
        st.session_state.show_info = None

    col1, col2 = st.columns([2, 1])
    with col1:
        if st.button("▶️ Start Simulation"):
            prompt = """
            Create a realistic and unique insurance client scenario. Every time this prompt runs, generate fresh and random details that sound authentic.

            Include in point-wise format:
            Full name
            Age
            Marital status
            Children (if any)
            Occupation and employment type
            Annual income
            Location (city and state)
            Health issues (if any – minor, chronic, or serious)
            Existing insurance policies (if any)
            Specific insurance needs or goals
            A brief client concern or question (written in their own words)

            Then write a short client opening message (as if they’re starting a real conversation). Keep this natural, polite, and under 3 short sentences.

            IMPORTANT: Format the entire output as plain text only. Do NOT use Markdown, special characters, or formatting symbols like *, _, >, #, or -.
            """

            response = get_gemini_response(prompt)

            # Attempt clean extraction
            if "Client opening message:" in response:
                parts = response.split("Client opening message:", 1)
                profile = parts[0].strip()
                opening_message = parts[1].strip().strip('"').strip()
            else:
                profile = response.strip()
                opening_message = "Hi, I'm interested in discussing some insurance options."

            st.session_state.client_profile = profile
            st.session_state.history = [{"role": "client", "content": opening_message}]
            st.success("✅ Client scenario created. Scroll down to begin the conversation.")

    with col2:
        if st.button("🧠 Need Info"):
            st.session_state.show_info = True

    if st.session_state.show_info:
        st.markdown("#### 🔍 Ask for Insurance-Related Info")
        query = st.text_input("Enter a keyword or question:", key="info_query")
        if st.button("Get Info"):
            info_prompt = f"""
            You are a helpful insurance expert assistant. The user has asked the following question:\n\n"{query}"

            Please provide:
            1. A clear, beginner-friendly explanation.
            2. A realistic example or client scenario where this concept applies.

            IMPORTANT: Format the response as plain text only.
            """
            answer = get_gemini_response(info_prompt)
            st.markdown("### 📘 Response")
            st.write(answer)

    if st.session_state.client_profile:
        st.markdown("### 🏡 Client Profile")
        st.info(st.session_state.client_profile)

        st.markdown("### 👩‍💼 You (Agent)")
        user_input = st.text_input("Enter your reply:", key="agent_input")

        if st.button("Send") and user_input:
            st.session_state.history.append({"role": "agent", "content": user_input})
            chat_history = format_chat_history(st.session_state.history)

            feedback_prompt = f"""
            The agent said: \"{user_input}\"\n\nClient Profile:\n{st.session_state.client_profile}\n\nEvaluate this agent response with:\n- A score out of 10\n- One-line summary\n- 1-2 improvement suggestions
            """
            feedback = get_gemini_response(feedback_prompt)
            st.markdown("### 🧠 Feedback")
            st.write(feedback)

            client_prompt = f"""
            You are role-playing as a realistic insurance client based on the profile below. Stay in character.

            Client Profile:
            {st.session_state.client_profile}

            Conversation so far:
            {chat_history}

            Respond naturally as the client:
            - Human-like, realistic
            - 3–4 short sentences
            - Focused on the current topic

            IMPORTANT: Return plain text only.
            """
            client_reply = get_gemini_response(client_prompt)
            st.session_state.history.append({"role": "client", "content": client_reply})

            st.markdown("### 🤖 Client")
            st.write(client_reply)

            if any(kw in client_reply.lower() for kw in ["i'm ready", "i have decided", "let's proceed"]):
                st.session_state.client_done = True

        if st.session_state.history:
            st.markdown("---")
            st.markdown("### 📄 Conversation History")
            for i, msg in enumerate(st.session_state.history):
                if msg["role"] == "client":
                    col1, col2 = st.columns([12, 1])
                    with col1:
                        st.markdown(f"**Client**: {msg['content']}")
                    with col2:
                        if st.button("❔", key=f"hint_{i}"):
                            st.session_state.hint_index = i
                else:
                    st.markdown(f"**Agent**: {msg['content']}")

            if st.session_state.hint_index is not None:
                index = st.session_state.hint_index
                client_msg = st.session_state.history[index]["content"]
                chat_history = format_chat_history(st.session_state.history)
                hint_prompt = f"""
                You are coaching an insurance sales agent.

                Client Profile:
                {st.session_state.client_profile}

                Conversation so far:
                {chat_history}

                The client’s last message was:
                "{client_msg}"

                Suggest:
                1. 1–2 helpful follow-up points or questions
                2. 1–2 thoughtful questions based on the profile
                3. Relevant products or coverage to consider

                Keep it plain text only.
                """
                hint = get_gemini_response(hint_prompt)
                st.info(f"💡 Hint based on message:\n\n{hint}")

        if st.button("⏹️ End Simulation") or st.session_state.client_done:
            st.markdown("### 📊 Final Coaching Summary")
            chat_text = format_chat_history(st.session_state.history)

            summary_prompt = f"""
            You are a supportive sales training coach.

            Client Profile:
            {st.session_state.client_profile}

            Conversation:
            {chat_text}

            Now write a clear, medium-length summary of the agent's performance:
            - 1–2 things done well
            - 1–2 improvement points
            - Missed opportunities
            - Overall score out of 10
            - Suggestions for insurance products

            IMPORTANT: Use plain text only.
            """
            summary = get_gemini_response(summary_prompt)
            st.write(summary)

            save_chat_to_file(st.session_state.history)
