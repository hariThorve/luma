import os
from dotenv import load_dotenv
import google.generativeai as genai

# Load environment variables
load_dotenv()

# Get API keys
gemini_api_key = os.getenv("GEMINI_API_KEY")
groq_api_key = os.getenv("GROQ_API_KEY")

print(f"Gemini API Key: {'Found' if gemini_api_key else 'Not found'}")
print(f"Groq API Key: {'Found' if groq_api_key else 'Not found'}")

# Test Gemini API
if gemini_api_key:
    try:
        genai.configure(api_key=gemini_api_key)
        model = genai.GenerativeModel('gemini-pro')
        response = model.generate_content("Hello, world!")
        print("Gemini API test: Success")
        print(f"Response: {response.text}")
    except Exception as e:
        print(f"Gemini API test: Failed - {str(e)}") 