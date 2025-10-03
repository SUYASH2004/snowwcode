import os, json, requests
from dotenv import load_dotenv

load_dotenv()
GROK_API_KEY = os.getenv("GROK_KEY")

# Use the direct endpoint URL
CHAT_COMPLETIONS_URL = "https://api.groq.com/openai/v1/chat/completions"

# List of currently available Groq models
AVAILABLE_MODELS = [
    "llama-3.1-8b-instant",  # Fastest model
    "llama-3.3-70b-versatile",  # Most capable model
    "llama-3.2-3b-preview",  # Lightweight model
    "llama-3.2-1b-preview",  # Lightest model
]

def call_grok(messages, model="llama-3.1-8b-instant", temperature=0.2, max_tokens=1000, timeout=30):
    """
    Calls Groq API's chat/completions endpoint.
    """
    if not GROK_API_KEY:
        raise EnvironmentError("❌ GROK_KEY not set in .env file")
    
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
        
        # If model error, suggest alternatives
        if "model_decommissioned" in response.text:
            print(f"💡 Available models: {', '.join(AVAILABLE_MODELS)}")
        
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
            "You MUST return ONLY valid JSON format. Do not include any markdown, code blocks, or additional text.\n\n"
            "Required JSON structure:\n"
            "{\n"
            '  "summary": "Brief overview of the code",\n'
            '  "line_by_line": ["Explanation line 1", "Explanation line 2", ...],\n'
            '  "time_complexity": "O(n) format",\n'
            '  "space_complexity": "O(n) format",\n'
            '  "vulnerabilities": ["Vuln 1", "Vuln 2", ...],\n'
            '  "suggestions": ["Suggestion 1", "Suggestion 2", ...],\n'
            '  "tests": ["Test case 1", "Test case 2", ...]\n'
            "}\n\n"
            "Rules:\n"
            "1. Return ONLY the JSON object, no other text\n"
            "2. Use double quotes for all strings\n"
            "3. Escape any special characters in strings\n"
            "4. If a section has no content, use empty array []\n"
            "5. Do not use markdown formatting"
        )
    }
    
    user_msg = {
        "role": "user",
        "content": f"Explain this {language} code at {level} level:\n```{language}\n{code}\n```"
    }

    return call_grok([system_msg, user_msg], model=model)
def get_available_models():
    """Returns list of available Groq models"""
    return AVAILABLE_MODELS