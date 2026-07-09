from urllib3 import response
import os
from dotenv import load_dotenv
import streamlit as st
from langchain_groq import ChatGroq


load_dotenv() #loading the .env file, as the .env file is in the same folder we do not need to specify the file name in bracket.

#streamlit page setup

st.set_page_config(
    page_title="💬 Chatbot",
    page_icon="📃",
    layout='centered',
)
st.title("💬 Generative AI Chatbot")

#inititalte chat history

if 'chat_history' not in st.session_state: 
    
    # Here if we write chat_history = [] direct as we did in lanchain, it will not be right as when the user type a message in the chatbox in
    # UI then whole code is run again in thath case if we hard code chat_history = [], then the chat_history will be deleted everytime and 
    # our llm will not have the context of what question was asked earlier. So, we store the chat_history in st.session_state, which is a
    # temporary memory given by streamlit to store the chat_history.
    st.session_state.chat_history = []

#display chat history 
for msg in st.session_state.chat_history:
   with st.chat_message(msg["role"]):
    st.markdown(msg["content"])

#llm initialization 
llm = ChatGroq(
    model='openai/gpt-oss-120b',
    temperature=0.1,
)

#input box
user_prompt = st.chat_input("Ask to Chatbot...")

if user_prompt:
    st.chat_message("user").markdown(user_prompt)
    st.session_state.chat_history.append({"role":"user","content":user_prompt}) 

    response = llm.invoke(
        input = [{"role":"system","content":"You are a helpful assistant"}, *st.session_state.chat_history]
    ) 
    assistant_response = response.content
    st.session_state.chat_history.append({"role":"assistant","content":assistant_response})

    with st.chat_message("assistant"):
        st.markdown(assistant_response)
