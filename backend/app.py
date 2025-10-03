from flask import Flask, request, jsonify
from flask_cors import CORS
from grok_client import ask_grok_for_explanation, get_available_models
import traceback
import json

app = Flask(__name__)
app.config["DEBUG"] = True 
CORS(app)

@app.route("/api/explain", methods=["GET", "POST"])
def explain_code():
    """
    Endpoint to explain code using Groq API.
    Expects JSON payload:
    {
        "code": "...",
        "language": "python",   # optional
        "level": "detailed",    # optional
        "model": "llama-3.1-8b-instant"  # optional
    }
    """
    if request.method == "GET":
        return jsonify({
            "message": "Use POST with JSON {code, language, level, model}",
            "available_models": get_available_models()
        }), 200
    
    try:
        data = request.get_json()
        if not data or "code" not in data:
            return jsonify({"error": "❌ 'code' field is required"}), 400
        
        code = data["code"]
        language = data.get("language", "python")
        level = data.get("level", "detailed")
        model = data.get("model", "llama-3.1-8b-instant")

        explanation = ask_grok_for_explanation(
            code, 
            language=language, 
            level=level, 
            model=model
        )

        # Try to parse as JSON, if fails return raw response
        try: 
            explanation_json = json.loads(explanation)
            return jsonify(explanation_json), 200
        except Exception:
            return jsonify({"raw_response": explanation}), 200
            
    except Exception as e:
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500

@app.route("/api/models", methods=["GET"])
def get_models():
    """Endpoint to get available Groq models"""
    return jsonify({"available_models": get_available_models()})

@app.route("/", methods=["GET"])
def home():
    return jsonify({
        "message": "Code Explainer API is running!",
        "endpoints": {
            "GET /api/explain": "Get usage instructions",
            "POST /api/explain": "Explain code",
            "GET /api/models": "Get available models"
        }
    })

if __name__ == "__main__":
    app.run(debug=True)