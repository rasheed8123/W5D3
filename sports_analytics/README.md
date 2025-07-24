# Sports Analytics RAG System

This project is a sports analytics Retrieval-Augmented Generation (RAG) system that answers complex queries about player performance, team statistics, and game insights from a collection of sports documents.

## Features
- Query decomposition for complex multi-part questions
- Contextual compression to reduce irrelevant information
- Basic reranking using semantic similarity
- Citation-based responses
- Uses only free, open-source resources
- Streamlit UI

## Setup
1. Clone this repository.
2. Navigate to the `sports_analytics` directory.
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Run the Streamlit app:
   ```bash
   streamlit run app.py
   ```

## Data
Sample sports documents are in `data/sample_docs/`. You can add your own `.txt` files for more data.

## Usage
- Enter a sports analytics question in the Streamlit UI.
- The system will decompose the query, retrieve and compress relevant context, rerank results, and provide an answer with citations.

## Notes
- All models and libraries used are free and open-source.
- For local LLMs, ensure you have sufficient memory (RAM/VRAM) or use smaller models. 