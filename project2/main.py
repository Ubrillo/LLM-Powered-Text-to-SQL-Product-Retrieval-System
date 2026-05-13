from langchain_helper import get_llm_chain, ask
import streamlit as st

st.title("AtliQ T shirts: Database Q&A")

question = st.text_input("Question: ")

if question:
    chain = get_llm_chain()
    answer = ask(question, chain)
    st.header("Answer:")
    st.write(answer)
