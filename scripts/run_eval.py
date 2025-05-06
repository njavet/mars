import time
from pathlib import Path
from argparse import ArgumentParser
import json

# project imports
from mars.conf import DOCX_DIR, RESULTS_DIR
from mars.utils.helpers import read_docx, format_as_markdown, load_prompts
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


def run_eval(base_url):
    lms = get_lms(base_url)
    system_message = load_prompts()[0]['text']
    for docx_path in DOCX_DIR.glob('*.docx'):
        start_t = time.time()
        text = read_docx(docx_path)
        print('evaluating {}'.format(docx_path))
        results = []
        for lm_name in lms:
            print('lm_name: ', lm_name)
            try:
                res_gen = run_baseline(base_url=base_url,
                                       lm_name=lm_name,
                                       system_message=system_message,
                                       query=text,
                                       chat_mode=False)
            except:
                print('no generate')
                res_gen = ''
            try:
                res_chat = run_baseline(base_url=base_url,
                                        lm_name=lm_name,
                                        system_message=system_message,
                                        query=text,
                                        chat_mode=True)
            except:
                res_chat = ''
                print('no chat')
            results.append({'lm_name': lm_name,
                            'output_chat': format_as_markdown(res_chat),
                            'output_generate': format_as_markdown(res_gen),
                            })
        output_path = Path.joinpath(RESULTS_DIR, docx_path.stem + '_2.json')
        with open(output_path, 'w') as f:
            json.dump(results, f, indent=2, ensure_ascii=False)
        print('evaluation took {:.2f} seconds'.format(time.time() - start_t))


if __name__ == '__main__':
    main()
