import streamlit as st
from utils.gemini_helper import get_gemini_response
import json

# Format chat for display/download
def format_chat_history(history):
    return "\n".join([
        f"{'Agent' if m['role'] == 'agent' else 'Client'}: {m['content']}"
        for m in history
    ])

# Download chat as .txt
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

# Save chat as JSON locally
def save_chat_to_file(history, file_path="chat_history.json"):
    if not history:
        return
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(history, f, indent=2)

# Main Simulation Entry
def run_field_sales_training():
    st.subheader("🎓 Field Sales Training Agent (Autonomous Client Mode)")

    # Session state variables
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

    # Start/Info Buttons
    col1, col2 = st.columns([2, 1])
    with col1:
        if st.button("▶️ Start Simulation"):
            prompt = """
            Create a realistic and unique insurance client scenario. Every time this prompt runs, generate fresh and random details that sound authentic.

            Include in point-wise format:
            - Full name
            - Age
            - Marital status
            - Children (if any)
            - Occupation and employment type
            - Annual income
            - Location (city and state)
            - Health issues (if any – minor, chronic, or serious)
            - Existing insurance policies (if any)
            - Specific insurance needs or goals
            - A brief client concern or question (written in their own words)

            Then write a short client opening message (as if they’re starting a real conversation). Keep this natural, polite, and under 3 short sentences.

            IMPORTANT: Format the entire output as plain text only. Do NOT use Markdown, special characters, or formatting symbols like *, _, >, #, or -.
            """


            response = get_gemini_response(prompt)
            # After scenario creation
            st.session_state.client_profile = response.split("\n\n", 1)[0]
            st.session_state.client_profile_raw = st.session_state.client_profile  # Needed!

            st.session_state.history = []
            st.session_state.client_profile = response.split("\n\n", 1)[0]
            first_message = response.split("\n\n", 1)[1]
            st.session_state.history.append({"role": "client", "content": first_message})
            st.success("✅ Client scenario created. Scroll down to begin the conversation.")

    with col2:
        if st.button("🧠 Need Info"):
            st.session_state.show_info = True

    # Insurance Info Search
    if st.session_state.show_info:
        st.markdown("#### 🔍 Ask for Insurance-Related Info")
        query = st.text_input("Enter a keyword or question (e.g., term life insurance, deductible, bundling policies):", key="info_query")
        if st.button("Get Info"):
            info_prompt = f"""
            You are a helpful insurance expert assistant. The user has asked the following question:\n\n"{query}"

            Please provide:
            1. A clear, beginner-friendly explanation.
            2. A realistic example or client scenario where this concept applies.
            
            IMPORTANT: Format the response as plain text, not Markdown. Avoid using **bold**, *italics*, or special formatting characters.
            Please return the answer as preformatted plain text. Do not use markdown, bullet points, bold, italics, or symbols like *, _, #, or >.
            """
            answer = get_gemini_response(info_prompt)
            st.markdown("### 📘 Response")
            st.write(answer)

    # Display client profile and chat
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
            You are role-playing as a realistic insurance client based on the profile below. Stay fully in character.

            Client Profile:
            {st.session_state.client_profile}

            Conversation so far:
            {chat_history}

            Now respond naturally as the client. Keep it:
            - Human-like and realistic
            - 3 to 4 sentences short
            - Focused on the current topic
            - Not overly detailed or robotic

            If you're ready to proceed with a decision, express that clearly. Otherwise, continue with a short, relevant question or comment.

            IMPORTANT: Return plain text only. Do NOT use Markdown or any formatting characters like *, _, >, or #.
            """


            client_reply = get_gemini_response(client_prompt)
            st.session_state.history.append({"role": "client", "content": client_reply})

            st.markdown("### 🤖 Client")
            st.write(client_reply)

            if any(kw in client_reply.lower() for kw in ["i'm ready", "i have decided", "let's proceed"]):
                st.session_state.client_done = True

        # Conversation History with ❔ hint for client replies
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

            # Show contextual hint popup
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
                1. 1–2 short, helpful follow-up points or questions the agent could ask next. Keep it to 5–6 lines.
                2. 1–2 thoughtful questions the agent can ask based on the client's message and profile.
                3. Relevant insurance products or coverage options the agent could consider offering.

                IMPORTANT: Keep the entire response in plain text only. Avoid using any Markdown, special characters, or formatting like *, _, >, or #.
                """

                hint = get_gemini_response(hint_prompt)
                st.info(f"💡 Hint based on message: \n\n{hint}")

        # Final summary
        if st.button("⏹️ End Simulation") or st.session_state.client_done:
            st.markdown("### 📊 Final Coaching Summary")
            chat_text = format_chat_history(st.session_state.history)

            summary_prompt = f"""
            You are a supportive sales training coach.

            Client Profile:
            {st.session_state.client_profile}

            Conversation:
            {chat_text}

            Now write a medium-length, clear summary of the agent's performance.

            Include:
            - What the agent did well (1–2 clear points)
            - What could be improved (1–2 specific suggestions)
            - Missed opportunities to offer relevant insurance solutions
            - An overall score out of 10
            - Suggestions for specific products or policy types that could have helped the client

            IMPORTANT: Keep the language simple, human, and easy to understand. Use plain text only — no formatting, Markdown, or symbols like *, _, >, or #.
            """


            summary = get_gemini_response(summary_prompt)
            st.write(summary)

            save_chat_to_file(st.session_state.history)
            download_chat_button(st.session_state.history)

            for key in ["client_profile", "history", "client_done", "hint_index", "show_info"]:
                st.session_state.pop(key, None)
