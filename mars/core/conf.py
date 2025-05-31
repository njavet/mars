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
OLLAMA_PORTS = {
    'default': 11434,
    'noe': 8800,
    'tosh': 8800,
    'abdk': 8604
}


EVAL_LMS = [
    'mistral:7b-instruct',
    'openhermes:latest',
    'yi:latest',
    'dolphin3:latest',
    'zephyr:7b',
    'llama3.3:70b',
    'llama3.3:70b-instruct-q8_0',
    'llama3.1:8b',
    'llama3.1:8b-instruct-q8_0',
]


# db
DOCX_DIR = Path('data/docx_reports')
TEXT_DIR = Path('data/text_reports')
MD_DIR = Path('data/md_reports')
CHAT_DB_URL = Path('data/chat.json')
RESULT_DB_URL = Path('data/result.json')


# evaluation
SCORE_KEYS = ['complete', 'irrelevant', 'concise']
SCORE_VALUES = ['yes', 'no', 'undefined']
