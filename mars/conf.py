from pathlib import Path


# ports
FAST_API_PORT = 8080
OLLAMA_PORT = 11434


# data
DB_URL = 'sqlite:///sentence.db'
PDF_DIR = Path('')


# sentence transformer model
SENTENCE_TRANSFORMER_NAME = 'all-MiniLM-L6-v2'


# language models
LMS = [
    'llama3.2:1b',
    'llama3.2:3b',
    'llama3.1:8b',
    'mistral',
    'deepseek-r1:7b',
    'meditron',
    'deepseek-r1:14b',
    'qwen2.5:14b',
    'qwq',
    'deepseek-r1:32b'
]


# prompts
PROMPT_PATH = Path('mars/prompts.toml')
