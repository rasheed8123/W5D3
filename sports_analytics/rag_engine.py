# rag_engine.py
# Implements the RAG pipeline for sports analytics
import os
from sentence_transformers import SentenceTransformer
import chromadb
from chromadb.config import Settings
from chromadb.utils import embedding_functions
from transformers import pipeline
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

DATA_DIR = os.path.join(os.path.dirname(__file__), 'data', 'sample_docs')
CHROMA_DIR = os.path.join(os.path.dirname(__file__), 'chroma_db')
EMBED_MODEL = 'all-MiniLM-L6-v2'

# Initialize embedding model
embedder = SentenceTransformer(EMBED_MODEL)

# Initialize ChromaDB client
chroma_client = chromadb.Client(Settings(persist_directory=CHROMA_DIR))
collection = chroma_client.get_or_create_collection('sports_docs')

# Load and index documents if not already indexed

def load_documents():
    docs = []
    for fname in os.listdir(DATA_DIR):
        if fname.endswith('.txt'):
            with open(os.path.join(DATA_DIR, fname), 'r', encoding='utf-8') as f:
                docs.append({'id': fname, 'text': f.read()})
    return docs

def index_documents():
    if len(collection.get()['ids']) == 0:
        docs = load_documents()
        texts = [doc['text'] for doc in docs]
        ids = [doc['id'] for doc in docs]
        embeddings = embedder.encode(texts).tolist()
        collection.add(documents=texts, embeddings=embeddings, ids=ids)

index_documents()

def retrieve(query, top_k=3):
    query_emb = embedder.encode([query])[0].tolist()
    results = collection.query(query_embeddings=[query_emb], n_results=top_k)
    docs = []
    for i in range(len(results['ids'][0])):
        docs.append({
            'id': results['ids'][0][i],
            'text': results['documents'][0][i],
            'score': results['distances'][0][i]
        })
    return docs

# Load Flan-T5 for query decomposition
try:
    decompose_pipe = pipeline('text2text-generation', model='google/flan-t5-base', max_length=128)
except Exception as e:
    decompose_pipe = None
    print(f"Warning: Could not load Flan-T5 model for query decomposition: {e}")

def decompose_query(query):
    """
    Use an LLM to break down a complex query into sub-questions.
    """
    if decompose_pipe is None:
        return [query]
    prompt = f"Break down this sports analytics question into clear sub-questions, separated by semicolons: {query}"
    result = decompose_pipe(prompt, do_sample=False)[0]['generated_text']
    subqs = [q.strip() for q in result.split(';') if q.strip()]
    return subqs if subqs else [query]

def compress_context(query, doc_text):
    """
    Use LLM to filter out irrelevant sentences from a document chunk for the given query.
    """
    if decompose_pipe is None:
        return doc_text
    prompt = f"Given the question: '{query}', keep only the most relevant sentences from this text: {doc_text}"
    result = decompose_pipe(prompt, do_sample=False)[0]['generated_text']
    return result.strip() if result.strip() else doc_text

def rerank_docs(query, docs):
    """
    Rerank docs by cosine similarity between query and compressed text.
    """
    if not docs:
        return docs
    query_emb = embedder.encode([query])[0].reshape(1, -1)
    doc_embs = embedder.encode([doc['compressed_text'] for doc in docs])
    sims = cosine_similarity(query_emb, doc_embs)[0]
    for i, doc in enumerate(docs):
        doc['similarity'] = sims[i]
    return sorted(docs, key=lambda d: d['similarity'], reverse=True)

def format_citations(query, docs):
    """
    Format the answer with citations for each supporting document.
    """
    answer = f"## Answer for: {query}\n"
    for i, doc in enumerate(docs):
        answer += f"\n### Source [{i+1}]: {doc['id']} (Similarity: {doc['similarity']:.2f})\n"
        answer += doc['compressed_text'][:500] + ('...' if len(doc['compressed_text']) > 500 else '')
    answer += "\n\n---\nCitations: "
    answer += ', '.join([f"[{i+1}] {doc['id']}" for i, doc in enumerate(docs)])
    return answer

def answer_query(query):
    """
    Main entry point for answering a user query.
    Steps:
    1. Query decomposition
    2. Document retrieval
    3. Contextual compression
    4. Reranking
    5. Citation formatting
    """
    # Query decomposition
    sub_questions = decompose_query(query)
    all_docs = []
    for subq in sub_questions:
        docs = retrieve(subq)
        for doc in docs:
            # Contextual compression
            compressed = compress_context(subq, doc['text'])
            doc['compressed_text'] = compressed
        all_docs.extend(docs)
    # Remove duplicates by doc id
    seen = set()
    unique_docs = []
    for doc in all_docs:
        if doc['id'] not in seen:
            unique_docs.append(doc)
            seen.add(doc['id'])
    # Rerank
    reranked_docs = rerank_docs(query, unique_docs)
    # Format with citations
    response = format_citations(query, reranked_docs)
    return response 