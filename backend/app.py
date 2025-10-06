from flask import Flask, request, jsonify
from flask_cors import CORS
from grok_client import ask_grok_for_explanation, get_available_models
import traceback
import os

app = Flask(__name__)
# Set debug to False for production on Render
app.config["DEBUG"] = os.environ.get('DEBUG', 'False').lower() == 'true'
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

        print(f"🔍 Processing request: {language}, {level}, {model}")
        
        # This now returns a DICTIONARY, not a string
        explanation = ask_grok_for_explanation(
            code, 
            language=language, 
            level=level, 
            model=model
        )

        # explanation is already a dictionary, so just return it directly
        return jsonify(explanation), 200
            
    except Exception as e:
        print(f"❌ Error in explain_code: {str(e)}")
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500

@app.route("/api/models", methods=["GET"])
def get_models():
    """Endpoint to get available Groq models"""
    return jsonify({"available_models": get_available_models()})

@app.route("/health", methods=["GET"])
def health_check():
    """Health check endpoint for Render"""
    return jsonify({
        "status": "healthy",
        "service": "SnowwCode Agent API"
    })

@app.route("/", methods=["GET"])
def home():
    return jsonify({
        "message": "🚀 Code Explainer API is running!",
        "endpoints": {
            "GET /": "This information",
            "GET /health": "Health check", 
            "GET /api/explain": "Get usage instructions",
            "POST /api/explain": "Explain code",
            "GET /api/models": "Get available models"
        }
    })

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port, debug=app.config["DEBUG"])