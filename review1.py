import streamlit as st
import google.generativeai as genai

# Configure the Generative AI API
genai.configure(api_key="AIzaSyAMjhGfJB86nvfUlLyEjLJMHYEUEPR0kaE")

# Initialize the LLM model
llm = genai.GenerativeModel("models/gemini-1.5-flash")

# Function to format history for the model
def format_history_for_model(history):
    """Format history entries to match the model's expected structure."""
    formatted_history = []
    for entry in history:
        formatted_history.append({
            "role": entry["role"],
            "parts": [{"text": entry["content"]}]
        })
    return formatted_history

# Function to get the response from the AI reviewer
def review_code(code):
    """Generate a review for the submitted code."""
    if "history" not in st.session_state:
        st.session_state.history = []

    formatted_history = format_history_for_model(st.session_state.history)
    reviewer = llm.start_chat(history=formatted_history)

    # Prompt for reviewing the code
    message = f"Review the following Python code for bugs and improvements:\n\n{code}"
    response = reviewer.send_message(message)

    # Update history
    st.session_state.history.append({"role": "user", "content": code})
    st.session_state.history.append({"role": "assistant", "content": response.text})

    return response.text

# Streamlit App
st.title("AI Code Reviewer")

# Initialize session state for chat history
if "history" not in st.session_state:
    st.session_state.history = []

# Display chat history
for entry in st.session_state.history:
    if entry["role"] == "user":
        st.chat_message("human").write(entry["content"])
    else:
        st.chat_message("ai").write(entry["content"])

# Input for code review
user_code = st.text_area("Paste your Python code here for review:", height=300)
if st.button("Review Code"):
    if user_code.strip():
        st.chat_message("human").write(user_code)
        with st.spinner("Reviewing your code..."):
            try:
                response = review_code(user_code)
                st.chat_message("ai").write(response)
            except Exception as e:
                st.error(f"An error occurred: {e}")
    else:
        st.warning("Please paste some Python code to review!")
