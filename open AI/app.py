import os 
from dotenv import load_dotenv
load_dotenv()

from langchain_openai import ChatOpenAI

os.environ["LANGCHAIN_API_KEY"]=os.getenv("LANGCHAIN_API_KEY")
os.environ["LANGCHAIN_TRACING_V2"]="true"
os.environ["LANGCHAIN_PROJECT"]=os.getenv("LANGCHAIN_PROJECT")


# CREATE MODEL

model = ChatOpenAI(model="gpt-4o")

from langchain_core.prompts import ChatPromptTemplate
template = ChatPromptTemplate.from_messages([
            ("system", "You are a helpful AI bot. Your name is Carl."),
            ("human", "Question:{question}"),
        ])
from langchain_core.output_parsers import StrOutputParser
output = StrOutputParser()

chain = template|model|output

import streamlit as st
st.title("Langchain Demo With Gemma Model")
input_text=st.text_input("What question you have in mind?")

if input_text:
    st.write(chain.invoke({"question":input_text}))
