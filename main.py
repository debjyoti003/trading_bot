import pickle
import streamlit as st
import os
from config import OPENAI_API_KEY
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from langchain.chat_models import ChatOpenAI
from langchain.chains.question_answering import load_qa_chain

os.environ["OPENAI_API_KEY"] = OPENAI_API_KEY

st.set_page_config(
    page_title="Trading Chatbot",
    page_icon=":robot_face",
)

st.title("Trading Chatbot")

openai_llm = ChatOpenAI(streaming = True, temperature = 0, model_name = 'ft:gpt-3.5-turbo-0613:personal::8FeSw7Cz')

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Please ask your question"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""
        for message in st.session_state.messages:
            try:
                llm = ChatOpenAI(streaming = True, temperature = 0, model_name = 'gpt-3.5-turbo')
                template = """Consider yourself as a Trading expert, and you need to answer the given question accordinly: {question}"""
                prompt = PromptTemplate(template=template, input_variables=["question"])
                llm_chain = LLMChain(prompt=prompt, llm=openai_llm)
                # chain = load_qa_chain(llm = openai_llm, chain_type = "stuff")
                response = llm_chain.run(message['content'])
            except:
                response = st.error("OpenAI model currently is overloaded with request, please try to ask your question again")
        message_placeholder.markdown(response)
    st.session_state.messages.append({"role": "assistant", "content": response})