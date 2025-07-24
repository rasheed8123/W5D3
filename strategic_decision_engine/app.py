import streamlit as st
from rag_engine import answer_query, process_uploaded_files

st.title('AI-Powered Strategic Planning Platform')

uploaded_files = st.file_uploader('Upload company documents (PDF, DOCX, TXT, CSV)', type=['pdf', 'docx', 'txt', 'csv'], accept_multiple_files=True)

if uploaded_files:
    with st.spinner('Processing documents...'):
        process_uploaded_files(uploaded_files)
    st.success('Documents processed and added to knowledge base.')

query = st.text_area('Enter your strategic business question:')

if st.button('Get Insights'):
    if query.strip():
        with st.spinner('Analyzing...'):
            response = answer_query(query)
        st.markdown(response, unsafe_allow_html=True)
    else:
        st.warning('Please enter a question.') 