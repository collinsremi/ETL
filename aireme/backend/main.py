from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from dotenv import load_dotenv
from prompt import build_prompt
import requests
import os

load_dotenv()

required_env_vars = ['NVIDIA_API_KEY', 'SUPABASE_URL', 'SUPABASE_KEY']
for var in required_env_vars:
    if not os.getenv(var):
        raise ValueError(f"Missing required environment variable: {var}")

app = FastAPI()

FRONTEND_URL = os.getenv("FRONTEND_URL", "http://localhost:3000")
app.add_middleware(
    CORSMiddleware,
    allow_origins=[FRONTEND_URL],
    allow_methods=["POST", "GET"],
    allow_headers=["Content-Type"],
)

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

class PropertyInput(BaseModel):
    property_type: str
    location: str
    price: str
    features: str
    target_buyer: str
    user_id: str

@app.post("/generate")
def generate_content(data: PropertyInput):
    if len(data.property_type) > 100:
        raise HTTPException(status_code=400, detail="Property type too long")
    if len(data.location) > 100:
        raise HTTPException(status_code=400, detail="Location too long")
    if len(data.features) > 500:
        raise HTTPException(status_code=400, detail="Features too long")

    prompt = build_prompt(
        data.property_type,
        data.location,
        data.price,
        data.features,
        data.target_buyer
    )

    headers = {
        "Authorization": f"Bearer {os.getenv('NVIDIA_API_KEY')}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": "meta/llama-3.1-70b-instruct",
        "messages": [{"role": "user", "content": prompt}],
        "max_tokens": 1024,
        "temperature": 0.7
    }

    try:
        response = requests.post(
            "https://integrate.api.nvidia.com/v1/chat/completions",
            headers=headers,
            json=payload,
            timeout=60
        )
        response.raise_for_status()
        result = response.json()
        if "choices" not in result or len(result["choices"]) == 0:
            raise HTTPException(status_code=500, detail="Invalid API response")
        content = result["choices"][0]["message"]["content"]
    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=500, detail=f"NVIDIA API error: {str(e)}")

    supabase_headers = {
        "apikey": SUPABASE_KEY,
        "Authorization": f"Bearer {SUPABASE_KEY}",
        "Content-Type": "application/json"
    }

    try:
        requests.post(
            f"{SUPABASE_URL}/rest/v1/generations",
            headers=supabase_headers,
            json={
                "user_id": data.user_id,
                "property_type": data.property_type,
                "location": data.location,
                "price": data.price,
                "features": data.features,
                "target_buyer": data.target_buyer,
                "output": content
            },
            timeout=10
        )
    except requests.exceptions.RequestException as e:
        print(f"Warning: Failed to save to database: {str(e)}")

    return {"output": content}

@app.get("/history/{user_id}")
def get_history(user_id: str):
    supabase_headers = {
        "apikey": SUPABASE_KEY,
        "Authorization": f"Bearer {SUPABASE_KEY}",
    }
    response = requests.get(
        f"{SUPABASE_URL}/rest/v1/generations?user_id=eq.{user_id}&order=created_at.desc&limit=20",
        headers=supabase_headers
    )
    return {"history": response.json()}

@app.get("/")
def root():
    return {"message": "AIREME backend is running"}