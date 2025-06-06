import requests
import subprocess
from docx import Document

# project imports
from mars.core.conf import DOCX_DIR, TEXT_DIR, MD_DIR
from mars.core import ref
from mars.core import prompts
from mars.schema.res import SystemMessage
from mars.db.chat_repo import ChatRepository
from mars.db.eval_repo import EvalRepository


def get_username() -> str:
    result = subprocess.run(['whoami'], capture_output=True, text=True)
    username = result.stdout.strip()
    return username


def get_chat_repo() -> ChatRepository:
    return ChatRepository()


def get_eval_repo() -> EvalRepository:
    return EvalRepository()


def get_models(base_url: str) -> list[str]:
    response = requests.get(f'{base_url}/api/tags')
    response.raise_for_status()
    data = response.json()
    models = [model['name'] for model in data.get('models', [])]
    return models


def load_system_messages():
    lst = []
    for name in dir(prompts):
        if not name.startswith('_'):
            text = getattr(prompts, name)
            sm = SystemMessage(key=name,
                               text=text)
            lst.append(sm)
    return lst


def fetch_documents(dtype: str) -> dict[str, str]:
    match dtype:
        case 'docx':
            target = DOCX_DIR.glob('*.docx')
            def extract(file):
                doc = Document(file)
                return '\n'.join(
                    para.text for para in doc.paragraphs if para.text.strip()
                )
        case 'text':
            target = TEXT_DIR.glob('*.txt')
            def extract(file):
                with open(file) as f:
                    return f.read()
        case 'markdown':
            target = MD_DIR.glob('*.md')
            def extract(file):
                with open(file) as f:
                    return f.read()
        case _:
            raise NotImplementedError
    return {file_path.stem: extract(file_path) for file_path in target}


def psychopharma():
    t = 'fehlende_psychopharmakologie.md'
    t1 = 'unvollstaendige_diagnosen.md'
    with open(MD_DIR.joinpath(t)) as f:
        text = f.read()
    return {'psycho': text}


def get_refs(filename: str) -> dict[str, int]:
    match filename:
        case 'fehlende_psychopharmakologie':
            return ref.ref_fehlende_psychopharmakologie
        case 'fehlender_verlauf':
            return ref.ref_fehlender_verlauf
        case 'fehlende_substanzanamnese':
            return ref.ref_fehlende_substanzanamnese
        case 'fehlende_vorgeschichte':
            return ref.ref_fehlende_vorgeschichte
        case 'unvollstaendige_diagnosen':
            return ref.ref_unvollstaendige_diagnosen
        case 'vollstaendig_mit_anmerkungen':
            return ref.ref_complete
        case 'vollstaendig_ohne_anmerkungen':
            return ref.ref_complete
        case _:
            raise NotImplementedError
