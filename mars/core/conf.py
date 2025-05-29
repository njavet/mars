from pathlib import Path


# zhaw CAI servers
OLLAMA_SERVERS = [
    'http://sandiego.zhaw.ch',
    'http://sanfrancisco.zhaw.ch',
    'http://losangeles.zhaw.ch',
    'http://sacramento.zhaw.ch',
    'http://sanjose.zhaw.ch',
    'http://fresko.zhaw.ch',
    'http://trinity.zhaw.ch',
    'http://elpaso.zhaw.ch',
    'http://lubbock.zhaw.ch',
    'http://honolulu.zhaw.ch',
    'http://hilo.zhaw.ch'
]


# ports
FAST_API_PORT = 8080
PORTS = {
    'default': 11434,
    'noe': 8800,
    'tosh': 8800,
    'abdk': 8604
}


# lms
TRANSFORMER_LLMS = [
    'teknium/OpenHermes-2.5-Mistral-7B',
]


EVAL_LMS = [
    'openhermes:latest',
    'yi:latest',
    'dolphin3:latest',
    'llama3.3:70b',
    'llama3.3:70b-instruct-q8_0',
    'llama3.1:8b',
    'llama3.1:8b-instruct-q8_0',
]


# db
DOCX_DIR = Path('data/docxs')
TEXT_DIR = Path('data/texts')
CHAT_DB_URL = Path('data/chat.json')
RESULT_DB_URL = Path('data/result.json')


# sentence transformer model
SENTENCE_TRANSFORMER_NAME = 'all-MiniLM-L6-v2'


DOC_CHUNK_SIZE = 1024
DOC_SEPARATORS = ['\n\n']


LIBS = ['ollama', 'transformers']


# evaluation
SCORE_KEYS = ['complete', 'irrelevant', 'concise']
SCORE_VALUES = ['yes', 'no', 'undefined']
