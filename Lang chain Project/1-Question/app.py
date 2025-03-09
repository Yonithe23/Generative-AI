import os
import streamlit as st
import openai
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Set project tracking
project_name = os.getenv("LANGCHAIN_PROJECT", "default_project")
os.environ["LANGCHAIN_PROJECT"] = project_name

# Ensure API key is set safely
api_key = os.getenv("OPENAI_API_KEY")

if api_key:  # ✅ Only set if not None
    os.environ["OPENAI_API_KEY"] = api_key

# Enable LangChain Tracing
os.environ["LANGCHAIN_TRACING_V2"] = "true"

# Define Prompt Template
prompt = ChatPromptTemplate.from_messages(
    [
        ("system", "You are a helpful assistant. Please respond to user queries."),
        ("user", "Question: {question}")
    ]
)

# Function to generate response
def generate_response(question, api_key, engine, temperature, max_tokens):
    if not api_key:
        st.error("❌ OpenAI API Key is missing. Please enter it in the sidebar.")
        return
    
    openai.api_key = api_key  # Ensure API key is set properly
    llm = ChatOpenAI(model=engine, openai_api_key=api_key)  # ✅ Pass API key explicitly

    output_parser = StrOutputParser()
    chain = prompt | llm | output_parser
    answer = chain.invoke({'question': question})
    return answer

# Streamlit UI
st.title("Enhanced Q&A Chatbot With OpenAI")

# Sidebar settings
st.sidebar.title("Settings")
api_key = st.sidebar.text_input("Enter your OpenAI API Key:", type="password")

# Select OpenAI model
engine = st.sidebar.selectbox("Select OpenAI model", ["gpt-4o", "gpt-4-turbo", "gpt-4"])

# Adjust response parameters
temperature = st.sidebar.slider("Temperature", min_value=0.0, max_value=1.0, value=0.7)
max_tokens = st.sidebar.slider("Max Tokens", min_value=50, max_value=300, value=150)

# Main interface for user input
st.write("Go ahead and ask any question")
user_input = st.text_input("You:")

if user_input and api_key:
    try:
        response = generate_response(user_input, api_key, engine, temperature, max_tokens)
        if response:
            st.write("🤖 Chatbot:", response)
    except Exception as e:
        st.error(f"❌ Error: {e}")

elif user_input:
    st.warning("⚠ Please enter the OpenAI API key in the sidebar.")
else:
    st.write("📌 Please provide a question.")
