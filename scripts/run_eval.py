import time
from argparse import ArgumentParser
import json

# project imports
from mars.conf import DOCX_DIR
from mars.utils.helpers import read_docx
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

sys_msg = """
Nachfolgend ist ein psychiatrischer Austrittsbericht eines Patienten 
von der Universitätsklinik für Psychiatrie und Psychotherapie.
Beurteile den Text kritisch und überprüfe ihn insbesondere auf Vollständigkeit.
"""

"""
 --- DOCUMENT START ---
 {doc_text}
--- DOCUMENT END ---
"""

def run_eval(base_url):
    lms = get_lms(base_url)
    for docx_path in DOCX_DIR.glob('*.docx'):
        start_t = time.time()
        text = read_docx(docx_path)
        query = '\n'.join(['---DOCUMENT START---', text, '---DOCUMENT END---'])
        print('evaluating {}'.format(docx_path))
        results = []
        for lm_name in lms:
            print('lm_name: ', lm_name)
            res = run_baseline(base_url=base_url,
                               lm_name=lm_name,
                               system_message=sys_msg,
                               query=query)
            results.append({'lm': lm_name,
                            'output': res})
        with open('data/results' + docx_path.stem + '.json', 'w') as f:
            json.dump(results, f, indent=2, ensure_ascii=False)
        print('evaluation took {:.2f} seconds'.format(time.time() - start_t))


if __name__ == '__main__':
    main()
