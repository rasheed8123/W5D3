# Automated Quiz Generator

This project is an advanced assessment generation system that creates personalized quizzes, assignments, and tests based on educational content. Instructors can upload educational documents, and the system generates diverse question types with explanations, leveraging Hybrid RAG and advanced reranking.

## Features
- Document upload & processing (PDF, DOCX, TXT)
- Hybrid RAG (dense + sparse retrieval: sentence-transformers + BM25)
- Contextual compression with dynamic chunk sizing
- Advanced reranking (cross-encoder)
- Redis caching for frequently accessed content and generated assessments
- Tool calling for educational APIs and dynamic difficulty adjustment
- Streamlit UI for quiz generation and user interaction
- Uses only free, open-source resources

## Setup
1. Clone this repository.
2. Navigate to the `automated_quiz_generator` directory.
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Run the Streamlit app:
   ```bash
   streamlit run app.py
   ```

## Usage
- Upload educational documents (PDF, DOCX, TXT) via the UI.
- Select topic, difficulty, and question types.
- Generate quizzes with explanations and citations.

## Notes
- All models and libraries used are free and open-source.
- For local LLMs, ensure you have sufficient memory (RAM/VRAM) or use smaller models. 