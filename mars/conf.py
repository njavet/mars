from pathlib import Path


# ports
FAST_API_PORT = 8080
OLLAMA_PORT = 11434


# data
DB_URL = 'sqlite:///sentence.db'
FAISS_INDEX = 'index.faiss'
PDF_DIR = Path('data/pdfs')


# sentence transformer model
SENTENCE_TRANSFORMER_NAME = 'all-MiniLM-L6-v2'


# prompts
PROMPT_PATH = Path('mars/prompts.toml')
SYS_PROMPT_PATH = Path('mars/sys_prompts.toml')


# RAG
L2_THRESHOLD = 1.0
CHUNK_SIZE = 512
OVERLAP = 64
SEPARATORS = ['\n\n', '. ', '\n', ' ']
