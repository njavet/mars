from pathlib import Path


# ports
FAST_API_PORT = 8080
OLLAMA_PORT = 11434


# data
DB_URL = 'sqlite:///sentence.db'
FAISS_INDEX = 'index.faiss'
DOCX_DIR = Path('data/docxs')
PDF_DIR = Path('data/pdfs')


# language models


# sentence transformer model
SENTENCE_TRANSFORMER_NAME = 'all-MiniLM-L6-v2'


# prompts
SYSTEM_PROMPT = Path('mars/system_messages.toml')


# RAG
L2_THRESHOLD = 0.8
CHUNK_SIZE = 512
OVERLAP = 64
SEPARATORS = ['\n\n', '. ', '\n', ' ']
