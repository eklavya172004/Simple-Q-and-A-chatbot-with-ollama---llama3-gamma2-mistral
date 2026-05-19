import streamlit as st
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate

import os
from dotenv import load_dotenv

load_dotenv()

# Langsmith tracking
os.environ['LANGCHAIN_API_KEY']=os.getenv("LANGCHAIN_API_KEY")
os.environ['LANGCHAIN_TRACING_V2']="true"
os.environ['LANGCHAIN_PROJECT']="simpleQNA"


# Prompt Template
prompt=ChatPromptTemplate.from_messages(
    [
        ("system","You are a helpfull assistant.Please respond to the user queries."),
        ("user","Question:{question}")
    ]
)

def generate_response(question,api_key,llm,temperature,max_tokens):
    llm=ChatOpenAI(model=llm, api_key=api_key, temperature=temperature, max_tokens=max_tokens)
    output_parser=StrOutputParser()
    chain=prompt|llm|output_parser
    answer=chain.invoke({'question':question})
    return answer

# StrOutputParser() is converting the LLM response into a normal string.
# Without it, ChatOpenAI returns a more complex AI message object, not plain text.

## Title of the app
st.title("Enhanced Q&A chatbot with OpenAi key")

#Sidebar for settings
st.sidebar.title("Settings")
api_key=st.sidebar.text_input("Enter your Open AI API key:",type="password")

# Drop Down to select various Open AI models
llm=st.sidebar.selectbox("Select the Open Ai model",["gpt-4o-mini","gpt-4o"])

# Adjust reponse parameter
temperature=st.sidebar.slider("Temperature",min_value=0.0,max_value=1.0,value=0.7)
max_tokens=st.sidebar.slider("Max Tokens",min_value=50,max_value=300,value=150)

# Main interface for user input
st.write("Go ahead and ask any question")
user_input=st.text_input("You:")
if user_input and api_key:
    response=generate_response(user_input,api_key,llm,temperature,max_tokens)
    st.write(response)
else:
    st.write("Please provide the query")