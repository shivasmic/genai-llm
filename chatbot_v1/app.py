import streamlit as st
from prompt_helper import create_qa_chain

st.title('How can I help you today?')

question = st.text_input("Ask me a question: ")
if question:
    chain = create_qa_chain()
    response = chain(question)
    st.header("Answer: ")
    st.write(response['result'])
