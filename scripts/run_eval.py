from pathlib import Path
from argparse import ArgumentParser
import requests
from docx import Document
import json

# project imports
from mars.conf import DOCX_DIR
from mars.utils.prompt import load_prompts
from mars.service.bot import Bot


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
    bot = Bot()
    lms = get_lms(base_url)
    system_message = load_prompts()[0]['text']
    for docx_path in DOCX_DIR.glob('*.docx'):
        text = read_docx(docx_path)
        print('evaluating {}'.format(docx_path))
        for lm_name in lms:
            res0 = bot.handle_query(base_url=base_url,
                                    lm_name=lm_name,
                                    agent_type='base',
                                    system_message=system_message,
                                    query=text)
            res1 = bot.handle_query(base_url=base_url,
                                    lm_name=lm_name,
                                    agent_type='rag',
                                    system_message=system_message,
                                    query=text)
            res2 = bot.handle_query(base_url=base_url,
                                    lm_name=lm_name,
                                    agent_type='agentic_rag',
                                    system_message=system_message,
                                    query=text)
            results = [{'base': res0,
                        'rag': res1,
                        'agentic_rag': res2}]
            json.dump(results, docx_path.stem + '.json', indent=2)


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
