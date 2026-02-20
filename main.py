import os
import json
from fastapi import FastAPI
from pydantic import BaseModel
from dotenv import load_dotenv
from google import genai

# Load environment variables
load_dotenv()

app = FastAPI(title="JanSahayak API")
api_key = os.getenv("GEMINI_API_KEY")
client = genai.Client(api_key=api_key)

# 1. Define the User Profile structure using Pydantic
class UserProfile(BaseModel):
    age: int
    gender: str
    state: str
    income_inr: int
    caste_category: str
    land_ownership_acres: float
    education_level: str

@app.get("/")
def read_root():
    return {"status": "JanSahayak Engine is running! ✅"}

# 2. Create the Eligibility Engine Route (Using POST because we are sending data)
@app.post("/check-eligibility")
def check_eligibility(user: UserProfile):
    try:
        # 3. Create a strict prompt for the AI
        prompt = f"""
        You are JanSahayak, an expert Eligibility Assessment AI for Indian government schemes.
        Analyze this user profile:
        Age: {user.age}, Gender: {user.gender}, State: {user.state}, 
        Income: ₹{user.income_inr}, Caste: {user.caste_category}, 
        Land: {user.land_ownership_acres} acres, Education: {user.education_level}.

        Based on this profile, suggest ONE realistic government scheme they are eligible for.
        You must reply ONLY in this exact JSON format, nothing else:
        {{
            "scheme_name": "Name of the Scheme",
            "is_eligible": true,
            "approval_probability_score": 85,
            "explanation": "Why they are eligible based on their exact data.",
            "estimated_benefit": "What they get",
            "required_documents": ["Doc 1", "Doc 2"]
        }}
        """

        # 4. Send to Gemini
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=prompt
        )
        
        # 5. Clean up the response and send it back as JSON
        ai_text = response.text.replace('```json', '').replace('```', '').strip()
        result_json = json.loads(ai_text)
        
        return result_json
        
    except Exception as e:
        return {"error": str(e)}