import os
import json
import requests
from dotenv import load_dotenv

# Only load .env file if it exists (for local development)
if os.path.exists('.env'):
    load_dotenv()

GROK_API_KEY = os.getenv("GROK_KEY")

# Use the direct endpoint URL
CHAT_COMPLETIONS_URL = "https://api.groq.com/openai/v1/chat/completions"

# List of currently available Groq models
AVAILABLE_MODELS = [
    "llama-3.1-8b-instant",
    "llama-3.3-70b-versatile", 
    "llama-3.2-3b-preview",
    "llama-3.2-1b-preview",
]

def call_grok(messages, model="llama-3.1-8b-instant", temperature=0.2, max_tokens=1000, timeout=30):
    """
    Calls Groq API's chat/completions endpoint.
    """
    if not GROK_API_KEY:
        raise EnvironmentError("❌ GROK_API_KEY not set. Please set it in environment variables.")
    
    headers = {
        "Authorization": f"Bearer {GROK_API_KEY}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "model": model,
        "messages": messages,
        "temperature": temperature,
        "max_tokens": max_tokens
    }

    try:
        print(f"🔧 Calling Groq API with model: {model}")
        response = requests.post(CHAT_COMPLETIONS_URL, headers=headers, json=payload, timeout=timeout)
        response.raise_for_status()
        data = response.json()
        
        print(f"✅ API call successful!")
        return data["choices"][0]["message"]["content"]
        
    except requests.exceptions.HTTPError as e:
        print(f"❌ HTTP Error: {e}")
        print(f"📄 Response text: {response.text}")
        raise
    except (KeyError, IndexError) as e:
        print(f"❌ Parsing error: {e}")
        print(f"📄 Full response: {data}")
        raise

def ask_grok_for_explanation(code, language="python", level="detailed", model="llama-3.1-8b-instant"):
    """
    Builds a structured prompt and asks Groq model for explanation.
    """
    system_msg = {
        "role": "system",
        "content": (
            "You are a senior software engineer and teacher. "
            "Return ONLY a valid JSON object with these exact keys: "
            "summary, line_by_line, time_complexity, space_complexity, "
            "vulnerabilities, suggestions, tests. "
            "No other text or markdown."
        )
    }
    
    user_msg = {
        "role": "user",
        "content": f"Explain this {language} code at {level} level:\n{code}"
    }

    response = call_grok([system_msg, user_msg], model=model)
    
    # Try to parse JSON, if fails return as raw
    try:
        return json.loads(response)
    except:
        return {"raw_response": response}

def get_available_models():
    """Returns list of available Groq models"""
    return AVAILABLE_MODELS