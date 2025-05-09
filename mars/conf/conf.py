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
    'ahmed': 8600
}


# prompts
SYSTEM_PROMPTS = Path('mars/conf/prompts.toml')


# data
DB_URL = 'sqlite:///mars.db'
FAISS_INDEX = 'index.faiss'
DOCX_DIR = Path('data/docxs')
PDF_DIR = Path('data/pdfs')
RESULTS_DIR = Path('data/results')


# sentence transformer model
SENTENCE_TRANSFORMER_NAME = 'all-MiniLM-L6-v2'


# RAG
L2_THRESHOLD = 0.8
CHUNK_SIZE = 512
OVERLAP = 64
SEPARATORS = ['\n\n', '. ', '\n', ' ']


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
