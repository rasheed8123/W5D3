import streamlit as st
from rag_engine import process_uploaded_files, generate_quiz

st.title('Automated Quiz Generator')

uploaded_files = st.file_uploader('Upload educational documents (PDF, DOCX, TXT)', type=['pdf', 'docx', 'txt'], accept_multiple_files=True)

if uploaded_files:
    with st.spinner('Processing documents...'):
        process_uploaded_files(uploaded_files)
    st.success('Documents processed and added to knowledge base.')

st.header('Quiz Generation')
topic = st.text_input('Topic (optional)')
difficulty = st.selectbox('Difficulty Level', ['Easy', 'Medium', 'Hard'])
question_types = st.multiselect('Question Types', ['MCQ', 'Short Answer', 'True/False', 'Fill in the Blanks'])

if st.button('Generate Quiz'):
    with st.spinner('Generating quiz...'):
        quiz = generate_quiz(topic, difficulty, question_types)
    st.markdown(quiz, unsafe_allow_html=True) 