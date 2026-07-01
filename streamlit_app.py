import streamlit as st
from chatbot import ask_taxassist

st.set_page_config(
    page_title="TaxAssist AI",
    page_icon="💬",
    layout="centered"
)

st.title("TaxAssist AI")
st.write("Singapore Individual Income Tax Assistant")
st.write("Ask a question based on the IRAS knowledge base.")

question = st.text_input("Enter your tax question:")

if st.button("Ask TaxAssist AI"):
    if question.strip() == "":
        st.warning("Please enter a question.")
    else:
        with st.spinner("Thinking..."):
            answer = ask_taxassist(question)

        st.subheader("Answer")
        st.write(answer)

st.caption("Prototype for academic research. Answers are generated using retrieved IRAS document context.")