# File: utils/gemini_helper.py
import os
from dotenv import load_dotenv
import google.generativeai as genai

# Configure Gemini
load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

model = genai.GenerativeModel('gemini-2.0-flash')

def get_gemini_response(prompt):
    response = model.generate_content(prompt)
    return response.text
