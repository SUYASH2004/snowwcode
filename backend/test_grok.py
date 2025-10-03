# test_grok.py
from grok_client import call_grok, get_available_models

def test_grok_connection():
    print("🔄 Testing Groq API connection...")
    print(f"📋 Available models: {get_available_models()}")
    
    # Test with different models
    test_models = get_available_models()
    
    for model in test_models:
        try:
            print(f"\n🧪 Testing model: {model}")
            test_messages = [
                {"role": "system", "content": "You are a helpful assistant. Respond with just 'Hello World!'"},
                {"role": "user", "content": "Say hello"}
            ]
            response = call_grok(test_messages, model=model, max_tokens=50)
            print(f"✅ {model} is working!")
            print(f"📝 Response: {response}")
            return model  # Return the first working model
            
        except Exception as e:
            print(f"❌ {model} failed: {e}")
            continue
    
    print("❌ No models are working. Please check your API key and connection.")
    return None

if __name__ == "__main__":
    working_model = test_grok_connection()
    if working_model:
        print(f"\n🎉 Success! Use model: {working_model}")
    else:
        print("\n💥 All models failed. Please check:")
        print("1. Your GROK_KEY in .env file")
        print("2. Your internet connection")
        print("3. Groq API status at https://status.groq.com/")