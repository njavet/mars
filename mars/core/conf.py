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


EVAL_LLMS_CONFIG = {
    'num_ctx': 32768,
    'temperature': 0,
    'top_k': 8,
    'top_p': 0.4
}


EVAL_LLMS_0 = [
    'llama3.1:8b',
    'llama3.1:8b-instruct-q8_0',
    'llama3.3:70b',
    'llama3.3:70b-instruct-q8_0',
    'dolphin-llama3:70b',
    'dolphin-llama3:8b',
    'mistral:7b-instruct',
    'gemma2:27b',
    'phi4:latest',
    'hermes3:8b',
]


EVAL_LLMS_LOCAL = [
    'llama3.1:8b',
    'llama3.1:8b-instruct-q8_0',
    'command-r7b:latest',
    'mistral:7b-instruct',
    'hermes3:8b',
]


# db
DOCX_DIR = Path('data/docx_reports')
TEXT_DIR = Path('data/text_reports')
MD_DIR = Path('data/md_reports')
CHAT_DB_URL = Path('data/chat.json')
RESULT_DB_URL = Path('data/result.json')


# evaluation
SCORE_KEYS = ['true_positives',
              'false_positives',
              'true_negatives',
              'false_negatives',
              'prompt_alignment',
              'irrelevant']
