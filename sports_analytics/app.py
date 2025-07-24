import streamlit as st
from rag_engine import answer_query

st.title('Sports Analytics RAG System')

query = st.text_area('Enter your sports analytics question:')

if st.button('Get Answer'):
    if query.strip():
        with st.spinner('Processing...'):
            response = answer_query(query)
        st.markdown(response)
    else:
        st.warning('Please enter a question.') 