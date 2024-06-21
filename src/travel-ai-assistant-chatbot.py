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

    # Debugging: Print payload before sending request
    print("Payload sent to LLM:")
    print(payload)

    response = requests.post(url, headers=headers, data=json.dumps(payload))
    
    # Debugging: Print response from LLM
    print("Response from LLM:")
    print(response.json())

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

# Initialize session state if not already initialized
if "history" not in st.session_state:
    st.session_state.history = [
        {"role": "system", "content": "Hello! I'm TravelBot. How can I assist you with your travel plans today?"}
    ]

# Text input for user query
user_input = st.text_input("You: ")

# Handle user input and button click
if st.button("Send") and user_input:
    # Add user input to history
    st.session_state.history.append({"role": "user", "content": user_input})
    
    # Get response from LLM
    response = local_llm_response(st.session_state.history)
    
    # Add LLM response to history
    st.session_state.history.append({"role": "system", "content": response})

    # Clear input field by resetting user_input (not st.session_state.input)
    user_input = ""

# Display conversation history
for message in st.session_state.history:
    if message["role"] == "user":
        st.write(f"**You:** {message['content']}")
    else:
        st.write(f"**TravelBot:** {message['content']}")

# Button to clear the chat history
if st.button("Clear Chat"):
    st.session_state.history = [
        {"role": "system", "content": "Hello! I'm TravelBot. How can I assist you with your travel plans today?"}
    ]
