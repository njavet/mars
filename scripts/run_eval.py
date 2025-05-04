from pathlib import Path
from argparse import ArgumentParser
import requests
from docx import Document
import json

# project imports
from mars.conf import DOCX_DIR
from mars.utils.prompt import load_prompts
from mars.service.service import run_baseline


def main():
    parser = create_parser()
    args = parser.parse_args()
    run_eval(base_url=args.ollama_server)


def create_parser() -> ArgumentParser:
    parser = ArgumentParser()
    parser.add_argument('ollama_server',
                        nargs='?',
                        default='http://localhost:11434')
    return parser


def run_eval(base_url):
    lms = get_lms(base_url)
    system_message = load_prompts()[0]['text']
    for docx_path in DOCX_DIR.glob('*.docx'):
        text = read_docx(docx_path)
        print('evaluating {}'.format(docx_path))
        results = []
        for lm_name in lms:
            res = run_baseline(base_url=base_url,
                               lm_name=lm_name,
                               system_message=system_message,
                               query=text)
            results.append({'lm': lm_name,
                            'system_message': system_message,
                            'input': text,
                            'output': res})
        with open('data/results/' + docx_path.stem + '.json', 'w') as f:
            json.dump(results, f, indent=2)


def read_docx(docx_path: Path):
    doc = Document(docx_path)
    text = '\n'.join([para.text for para in doc.paragraphs])
    return text


def get_lms(base_url):
    response = requests.get(f'{base_url}/api/tags')
    response.raise_for_status()
    data = response.json()
    lms = [lm_name['name'] for lm_name in data.get('models', [])]
    return lms


if __name__ == '__main__':
    main()
