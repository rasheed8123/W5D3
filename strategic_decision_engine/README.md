# Strategic Decision Engine

This project is an AI-powered strategic planning platform for CEOs and business leaders. Upload company documents and get intelligent, cited insights for business strategy development.

## Features
- Document upload & processing (PDF, DOCX, TXT, CSV)
- Query decomposition for complex strategic questions
- Contextual compression to filter relevant business insights
- Hybrid RAG (dense + sparse retrieval)
- Advanced reranking (multi-model ensemble)
- Citation-based responses with source tracking
- Streamlit dashboard with data visualization (charts/tables)
- RAGAS evaluation for explanation quality
- Uses only free, open-source resources

## Setup
1. Clone this repository.
2. Navigate to the `strategic_decision_engine` directory.
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Run the Streamlit app:
   ```bash
   streamlit run app.py
   ```

## Usage
- Upload company documents (PDF, DOCX, TXT, CSV) via the UI.
- Enter a strategic business question.
- The system will analyze, retrieve, and visualize insights with citations.

## Notes
- All models and libraries used are free and open-source.
- For local LLMs, ensure you have sufficient memory (RAM/VRAM) or use smaller models. 