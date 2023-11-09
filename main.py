import os
import streamlit as st
from streamlit_chat import message
from config import OPENAI_API_KEY
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from langchain.chat_models import ChatOpenAI
from langchain.schema import SystemMessage, HumanMessage, AIMessage
from langchain.memory import ConversationBufferMemory
from langchain.chains.question_answering import load_qa_chain

os.environ["OPENAI_API_KEY"] = OPENAI_API_KEY

st.set_page_config(
    page_title="Trading Chatbot",
    page_icon=":robot_face",
)

st.header("Custom Trading Chatbot")

# openai_llm = ChatOpenAI(streaming = True, temperature = 0, model_name = 'ft:gpt-3.5-turbo-0613:personal::8FeSw7Cz')
llm = ChatOpenAI(streaming = True, temperature = 0, model_name = 'gpt-3.5-turbo')

if "messages" not in st.session_state:
    st.session_state.messages = [
        SystemMessage(content="You are a coding expert who is fluent and writes error free code in different programming languages")
    ]

user_input = st.text_input("Your message: ", key = "user_input")

if user_input:
    st.session_state.messages.append(HumanMessage(content=user_input))
    with st.spinner("Thinking..."):
        response = llm(st.session_state.messages)
    st.session_state.messages.append(AIMessage(content=response.content))

messages = st.session_state.get('messages', [])
for i, msg in enumerate(messages[1:]):
    if i % 2 == 0:
        message(msg.content, is_user=True, key=str(i) + '_user')
    else:
        message(msg.content, is_user=False, key=str(i) + '_ai')