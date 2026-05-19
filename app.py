import streamlit as st
import openai
import os
from dotenv import load_dotenv

load_dotenv()

# Set page config
st.set_page_config(page_title="Q&A Chatbot", layout="centered")

# Title
st.title("Enhanced Q&A Chatbot with OpenAI")

# Sidebar for settings
st.sidebar.title("Settings")
api_key = st.sidebar.text_input("Enter your OpenAI API key:", type="password")

# Model selection
model = st.sidebar.selectbox("Select OpenAI Model", ["gpt-4o-mini", "gpt-4o", "gpt-3.5-turbo"])

# Temperature and max tokens
temperature = st.sidebar.slider("Temperature", min_value=0.0, max_value=1.0, value=0.7)
max_tokens = st.sidebar.slider("Max Tokens", min_value=50, max_value=300, value=150)

def generate_response(question, api_key, model, temperature, max_tokens):
    """Generate response using OpenAI API directly"""
    client = openai.OpenAI(api_key=api_key)
    
    response = client.chat.completions.create(
        model=model,
        messages=[
            {
                "role": "system",
                "content": "You are a helpful assistant. Please respond to the user queries."
            },
            {
                "role": "user",
                "content": question
            }
        ],
        temperature=temperature,
        max_tokens=max_tokens
    )
    
    return response.choices[0].message.content

# Main interface
st.write("Go ahead and ask any question:")
user_input = st.text_input("You:")

if user_input and api_key:
    try:
        response = generate_response(user_input, api_key, model, temperature, max_tokens)
        st.write(response)
    except Exception as e:
        st.error(f"Error: {str(e)}")
else:
    if user_input and not api_key:
        st.warning("Please provide your OpenAI API key")
    else:
        st.info("Please provide the query")