from pathlib import Path


# zhaw CAI servers
SERVERS = [
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
    'abdk': 8600
}


# lms
EVAL_LMS = [
    'openhermes:latest',
    'nous-hermes2:34b',
    'llama3-gradient:latest',
    'yi:latest',
    'dolphin3:latest',
    'llama2-uncensored:latest',

    'llama3.3:70b-instruct-q8_0',
    'llama3.3:70b',
    'llama3.1:8b-instruct-q8_0',
    'deepseek-r1:14b',
]


# data
DB_URL = 'sqlite:///mars.db'
FAISS_INDEX = 'index.faiss'
DOCX_DIR = Path('data/docxs')
TEXT_DIR = Path('data/texts')
PDF_DIR = Path('data/pdfs')
CHAT_DB_URL = Path('data/chat.json')
RESULT_DB_URL = Path('data/result.json')


# sentence transformer model
SENTENCE_TRANSFORMER_NAME = 'all-MiniLM-L6-v2'


# RAG
L2_THRESHOLD = 0.8
CHUNK_SIZE = 512
OVERLAP = 64
SEPARATORS = ['\n\n', '. ', '\n', ' ']

DOC_CHUNK_SIZE = 1024
DOC_SEPARATORS = ['\n\n']


# lm operation modes
OP_MODES = {'base': 'Base',
            'agentic': 'Agentic'}


# tools
TOOLS = {'rag': 'RAG'}


# evaluation
SCORE_KEYS = ['complete', 'irrelevant', 'concise']
SCORE_VALUES = ['yes', 'no', 'undefined']


ALLOWED_HEADINGS = {
    'Diagnosen',
    'Psychiatrische und somatische Nebendiagnosen',
    'Einweisungsumstände',
    'Zusammenfassung der Anamnese',
    'Psychiatrische Vorgeschichte',
    'Somatische Vorgeschichte',
    'Soziobiografische Anamnese',
    'Familienanamnese',
    'Drogen und Genussmittel',
    'Fremdanamnese',
    'Forensische Anamnese',
    'Untersuchungsbefunde Psychostatus',
    'Somatoneurostatus',
    'Weitere Untersuchungen',
    'Therapie und Verlauf',
    'Ad diagnostischer Einordnung',
    'Ad integriertem Therapieprogramm',
    'Ad Psychopharmakologie',
    'Ad psychotherapeutischen Themen',
    'Ad sozialer Situation',
    'Ad Verlauf',
    'Medikation bei Austritt',
    'Procedere',
}
