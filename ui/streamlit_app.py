# streamlit_app.py
import streamlit as st
import requests
import json

# Backend API URL
BACKEND_URL = "https://snowwcode.onrender.com"

def main():
    st.title("🤖 Code Explainer Agent")
    st.write("Paste your code below and get AI-powered explanations!")
    
    # Code input
    code = st.text_area(
        "Enter your code:",
        height=200,
        placeholder="def hello_world():\n    print('Hello, World!')"
    )
    
    # Options
    col1, col2 = st.columns(2)
    with col1:
        language = st.selectbox(
            "Programming Language:",
            ["python", "javascript", "java", "cpp", "go", "rust"]
        )
    with col2:
        explanation_level = st.selectbox(
            "Explanation Level:",
            ["beginner", "intermediate", "detailed"]
        )
    
    # Explain button
    if st.button("🚀 Explain Code"):
        if not code.strip():
            st.error("Please enter some code to explain.")
            return
        
        with st.spinner("🤔 Analyzing your code..."):
            try:
                payload = {
                    "code": code,
                    "language": language,
                    "level": explanation_level
                }
                
                response = requests.post(BACKEND_URL, json=payload)
                
                if response.status_code == 200:
                    result = response.json()
                    display_explanation(result)
                else:
                    error_msg = response.json().get("error", "Unknown error")
                    st.error(f"❌ Backend error: {error_msg}")
                    
            except requests.exceptions.ConnectionError:
                st.error("🔌 Could not connect to backend. Make sure Flask server is running on http://127.0.0.1:5000")
            except Exception as e:
                st.error(f"💥 Unexpected error: {str(e)}")

def display_explanation(explanation_data):
    """Display the explanation in a structured way"""
    
    # Check if it's raw response or structured JSON
    if "raw_response" in explanation_data:
        st.warning("⚠️ Received raw response (not structured JSON)")
        st.json(explanation_data["raw_response"])
        return
    
    # Structured response
    st.success("✅ Code analysis complete!")
    
    # Summary
    if "summary" in explanation_data:
        st.subheader("📝 Summary")
        st.write(explanation_data["summary"])
    
    # Line by line explanation
    if "line_by_line" in explanation_data:
        st.subheader("🔍 Line by Line Analysis")
        for i, line_explanation in enumerate(explanation_data["line_by_line"]):
            st.write(f"**Line {i+1}:** {line_explanation}")
    
    # Complexity analysis
    col1, col2 = st.columns(2)
    with col1:
        if "time_complexity" in explanation_data:
            st.metric("⏱️ Time Complexity", explanation_data["time_complexity"])
    with col2:
        if "space_complexity" in explanation_data:
            st.metric("💾 Space Complexity", explanation_data["space_complexity"])
    
    # Vulnerabilities
    if "vulnerabilities" in explanation_data and explanation_data["vulnerabilities"]:
        st.subheader("⚠️ Potential Vulnerabilities")
        for vuln in explanation_data["vulnerabilities"]:
            st.write(f"- {vuln}")
    
    # Suggestions
    if "suggestions" in explanation_data and explanation_data["suggestions"]:
        st.subheader("💡 Improvement Suggestions")
        for suggestion in explanation_data["suggestions"]:
            st.write(f"- {suggestion}")
    
    # Test cases
    if "tests" in explanation_data and explanation_data["tests"]:
        st.subheader("🧪 Test Cases")
        for test in explanation_data["tests"]:
            st.write(f"- {test}")

if __name__ == "__main__":
    main()