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
    'jinroh': 8800,
    'tosh': 8800,
    'ahmed': 8600
}


# data
DB_URL = 'sqlite:///sentence.db'
FAISS_INDEX = 'index.faiss'
DOCX_DIR = Path('data/docxs')
PDF_DIR = Path('data/pdfs')
RESULTS_DIR = Path('frontend/public/results')


# sentence transformer model
SENTENCE_TRANSFORMER_NAME = 'all-MiniLM-L6-v2'


# prompts
SYSTEM_PROMPT = Path('mars/conf/prompts.toml')


# RAG
L2_THRESHOLD = 0.8
CHUNK_SIZE = 512
OVERLAP = 64
SEPARATORS = ['\n\n', '. ', '\n', ' ']


# medical report sections
section_headers = [
    'Diagnosen',
    'Einweisungsumstände',
    'Zusammenfassung der Anamnese',
    'Psychopathologischer Befund',
    'Verlauf',
    'Beurteilung',
    'Therapie',
    'Psychopharmakologische Medikation bei Austritt',
    'Weiterführende Massnahmen'
]
