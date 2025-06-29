🧠 BFSI GenAI Assistant – AI-Powered Insurance Advisor & Trainer

This project is a multifunctional GenAI-powered insurance assistant designed for the **Insurance** sector. It provides client simulation, field sales training, risk assessment, insurance product recommendations, and claim readiness analysis using **Google Gemini Pro API** and **Streamlit**.

---


🔗 [[Click here to try the hosted app](https://field-sales-training-agentant.streamlit.app/)]

---

## 📌 Use Case

The assistant helps:
- **Field Sales Executives** simulate realistic client conversations and get AI coaching.
- **Insurance Agents** generate personalized product pitches.
- **Clients** assess risk and get claim guidance.
- **Businesses** train new insurance agents using AI-generated mock profiles.

---

## 🧩 Key Modules

### 1. 🎓 Field Sales Training Agent
- Generates a **realistic insurance client scenario** using Gemini.
- Users reply as an agent; Gemini plays the **client role**.
- Real-time AI feedback on responses.
- Conversation history downloadable.
  
### 2. 🧑‍💼 Advisor Mode
- Auto-fills from the generated client profile.
- Creates **tailored sales pitches** based on the client’s:
  - Age
  - Income
  - Health conditions
  - Insurance goal
  - Objection (if any)

### 3. 📊 Risk Assessment
- Calculates risk based on:
  - Age
  - Occupation
  - Health issues
- Explains **why the risk level was assigned** using Gemini.
  
### 4. 🛡️ Product Recommendation
- Recommends the most suitable insurance product.
- Uses:
  - Insurance goal
  - Income (used as proxy for budget)
  - Risk profile

### 5. 📄 Claim Advisor
- Identifies policy type and returns a **document checklist**.
- Checklist generated using Gemini.
- Works with or without a policy PDF upload.

---

## 🧠 AI Model

- **Model Used**: [Google Gemini Pro API](https://ai.google.dev)
- **Integration**: Modular prompt-based system with dynamic prompt construction
- **Client Profile Parsing**: Custom parser to extract structured info from Gemini-generated profiles

---

## 🗂️ Folder Structure


project-root/

│

├── app.py # Main Streamlit app entry point

├── utils/

│ ├── gemini_helper.py # API wrapper for Gemini Pro

│ ├── client_profile_parser.py # Extracts structured fields from raw profile

│ ├── training_agent.py # Field sales trainer

│ ├── agent_mode.py # Sales pitch generator

│ ├── risk_assessment.py # Risk level evaluator

│ ├── recommend_products.py # Product recommender

│ └── claim_advisor.py # Claim checklist generator

├── requirements.txt # Python dependencies

└── README.md # Project documentation


---

## 🛠️ Setup Instructions

### 🔧 Prerequisites
- Python 3.9+
- A valid [Gemini API Key](https://ai.google.dev)
- Streamlit installed

### 🧪 Local Setup

1. **Clone the repo**
git clone https://github.com/your-username/bfsi-genai-assistant.git
cd bfsi-genai-assistant

2. Install dependencies
pip install -r requirements.txt


3. Add Gemini API Key
Pass it directly in your gemini_helper.py.

4. Run the Streamlit app
streamlit run app.py


🧪 Example Use Flow
Click Start Simulation to get a random client profile.
Have a conversation with the simulated client.
Switch to other modules:
Advisor Mode: Get sales pitch
Risk Assessment: Get risk level and reasoning
Product Recommendation: Get product fit
Claim Advisor: Get claim document checklist
End the conversation to get AI feedback summary.

🧠 Future Enhancements
Use vector DB to store past client conversations
Add OCR support to extract policy details from PDFs
Multi-language client simulation
Role-specific dashboards (Agent vs Trainer)

👨‍💻 Contributing
Want to improve or extend this tool? Fork it, enhance it, and make a pull request!

📜 License
MIT License. Use freely with attribution.

🤝 Acknowledgements
Streamlit
Gemini API
Data Science Wizards Hackathon inspiration
