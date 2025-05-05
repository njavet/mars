import time
from argparse import ArgumentParser
import json

# project imports
from mars.conf import DOCX_DIR, RESULTS_DIR
from mars.utils.helpers import read_docx, format_as_markdown
from mars.service.service import (get_lms, run_baseline)


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


def get_system_message():
    sys_msg = """
    Nachfolgend ist ein psychiatrischer Austrittsbericht eines Patienten.
    Beurteile den Text kritisch und überprüfe ihn insbesondere auf Vollständigkeit.
    - Antworte kurz und beschreibe stichwortarig wenn etwas fehlt.
    - Keine Zusammenfassung 
    """
    return sys_msg


def run_eval(base_url):
    lms = get_lms(base_url)
    for docx_path in DOCX_DIR.glob('*.docx'):
        start_t = time.time()
        text = read_docx(docx_path)
        print('evaluating {}'.format(docx_path))
        results = []
        for lm_name in lms:
            print('lm_name: ', lm_name)
            res = run_baseline(base_url=base_url,
                               lm_name=lm_name,
                               system_message=get_system_message(),
                               query=text)
            results.append({'lm': lm_name,
                            'output': format_as_markdown(res)})
        output_path = Path.join(RESULTS_DIR, docx_path.stem + '.json')
        with open(output_path, 'w') as f:
            json.dump(results, f, indent=2, ensure_ascii=False)
        print('evaluation took {:.2f} seconds'.format(time.time() - start_t))


if __name__ == '__main__':
    main()
