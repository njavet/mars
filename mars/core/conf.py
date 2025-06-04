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


# LLMs
ALL_EVAL_LLMS = [
    'zephyr:7b',
    'mistral:7b-instruct',
    'hermes3:8b',
    'openhermes:latest',
    'deepseek-r1:7b',
    'dolphin3:latest',
    'llama3.2:3b',
    'llama3.1:8b',
    'llama3.1:8b-cold',
    'llama3.1:8b-instruct-q6_K',
]


EVAL_LLMS = [
    'deepseek-r1:8b',
    'llama3.1:8b-instruct-q8_0',
    'llama3.1:8b',
    'hermes3:8b',
    'dolphin3:latest',
    'mistral:7b-instruct'
]


JUSTIFIER_LLM = 'dolphin3:latest'


# db
DOCX_DIR = Path('data/docx_reports')
TEXT_DIR = Path('data/text_reports')
MD_DIR = Path('data/md_reports')
CHAT_DB_URL = Path('data/chat.json')
RESULT_DB_URL = Path('data/result.json')


# evaluation
SCORE_KEYS = ['true_positives',
              'false_negatives',
              'irrelevant']


REAL_SECTIONS = [
    'Diagnosen',
    'Einweisungsumstände',
    'Zusammenfassung der Anamnese',
    'Psychiatrische Vorgeschichte',
    'Somatische Vorgeschichte',
    'Soziobiografische Anamnese',
    'Familienanamnese',
    'Drogen und Genussmittel',
    'Fremdanamnese',
    'Forensische Anamnese',
    'Psychostatus',
    'Somatoneurostatus',
    'Weitere Untersuchungen',
    'Ad diagnostischer Einordnung',
    'Ad integriertem Therapieprogramm',
    'Ad Psychopharmakologie',
    'Ad psychotherapeutischen Themen',
    'Ad sozialer Situation',
    'Ad Verlauf',
    'Medikation bei Austritt',
    'Procedere',
]
