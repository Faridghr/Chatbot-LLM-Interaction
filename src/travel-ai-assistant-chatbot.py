import streamlit as st
import requests
import json

# Function to get response from local LLM
def local_llm_response(messages):
    url = "http://localhost:11434/api/chat"
    headers = {"Content-Type": "application/json"}
    payload = {
        "model": "llama3",
        "messages": messages
    }
    response = requests.post(url, headers=headers, data=json.dumps(payload))
    if response.status_code == 200:
        return response.json().get("reply", "Error: No response from LLM")
    else:
        return f"Error: {response.status_code}"

# Streamlit UI
st.title("Travel Planning and Recommendations Chatbot")

st.write("""
    Welcome to the Travel Planning and Recommendations Chatbot!
    I'm TravelBot, your friendly and knowledgeable travel assistant.
    Ask me anything about travel planning, and I'll provide you with personalized recommendations and tips.
""")

if "history" not in st.session_state:
    st.session_state.history = [
        {"role": "bot", "content": "Hello! I'm TravelBot. How can I assist you with your travel plans today?"}
    ]

def clear_history():
    st.session_state.history = [
        {"role": "bot", "content": "Hello! I'm TravelBot. How can I assist you with your travel plans today?"}
    ]

# Text input for user query
user_input = st.text_input("You: ", key="input")

if st.button("Send"):
    if user_input:
        # Add user input to history
        st.session_state.history.append({"role": "user", "content": user_input})
        
        # Get response from LLM
        response = local_llm_response(st.session_state.history)
        
        # Add LLM response to history
        st.session_state.history.append({"role": "bot", "content": response})
        
        # Clear input field
        st.session_state.input = ""

# Display conversation history
for message in st.session_state.history:
    if message["role"] == "user":
        st.write(f"**You:** {message['content']}")
    else:
        st.write(f"**TravelBot:** {message['content']}")

# Button to clear the chat history
if st.button("Clear Chat"):
    clear_history()
