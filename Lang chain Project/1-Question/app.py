import os
import streamlit as st
import openai

from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI


from dotenv import load_dotenv
load_dotenv()

#langsmith tracking
os.environ["LANGCHAIN_PROJECT"] = os.getenv("LANGCHAIN_PROJECT", "default_value")
os.environ["LANGCHAIN_API_KEY"] = os.getenv("LANGCHAIN_API_KEY")
os.environ["LANGCHAIN_TRACING-V2"] = "true"


prompt = ChatPromptTemplate.from_messages(
    [
        ("system", "You are helpfull asistance. please responce to the user query"),
        ("user", "Question:{question}"),
    ]
)


def generate_repsonse( question,api_key,llm,temperature , max_tokens):
    openai.api_key = api_key
    llm = ChatOpenAI(model= llm)
    out_parser = StrOutputParser()
    chain = prompt| llm | out_parser
    answer = chain.invoke({'question':question})
    return answer

#Title of the App
st.title("Question and Answer Chatbot With OpenAI")

st.sidebar.title("setting")
api_key = st.sidebar.text_input("Enter Your OpenAI API Key:" , type = "password")

llm = st.sidebar.selectbox("Select an Open AI Model", ["GPT-4 Turbo","GPT-4","GPT-4o"])
temperature =st.sidebar.slider("Temperature" , min_value=0.0 ,max_value=1.0 ,value=0.7)
max_tokens = st.sidebar.slider("Max Tokens" , min_value=50,max_value=300,value=150)

st.write("what is you question ?")
user_input = st.text_input("You:")

if user_input:
    response = generate_repsonse(user_input , api_key,llm ,temperature,max_tokens)
    st.write(response)
else:
    st.write("please provide the query")