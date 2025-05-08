import time
import toml
from pathlib import Path
from argparse import ArgumentParser
import json
import os
from docx import Document

# project imports
from mars.conf.conf import DOCX_DIR, RESULTS_DIR
from mars.utils.helpers import (read_docx,
                                format_as_markdown,
                                get_number_of_runs,
                                clean_medical_body,
                                load_system_messages)
from mars.schemas import Evaluation
from mars.service.service import (get_lms, run_baseline)


def main():
    parser = create_parser()
    args = parser.parse_args()
    sm = toml.load('mars/conf/prompts.toml')
    system_message = sm['medical_analyst_4']['system']
    runs = get_number_of_runs()
    os.mkdir(f'{RESULTS_DIR}/run{runs}')
    run_eval(base_url=args.ollama_server,
             system_message=system_message,
             result_dir=Path.joinpath(RESULTS_DIR, f'run{runs}'))


def create_parser() -> ArgumentParser:
    parser = ArgumentParser()
    parser.add_argument('ollama_server',
                        nargs='?',
                        default='http://localhost:11434')
    parser.add_argument('system_message',
                        nargs='?',
                        default='medical_analyst_2')
    return parser


def run_eval(base_url, system_message, result_dir):
    lms = get_lms(base_url)
    print(system_message)
    for docx_path in DOCX_DIR.glob('*.docx'):
        start_t = time.time()
        doc = Document(docx_path)
        dix = clean_medical_body(doc)
        # text = read_docx(docx_path)
        print('evaluating {}'.format(docx_path))
        results = Evaluation(server=base_url,
                             filename=docx_path.name,
                             system_message=system_message)
        for lm_name in lms:
            print('lm_name: ', lm_name)
            responses = []
            for k, v in dix.items():
                res_chat = run_baseline(base_url=base_url,
                                        lm_name=lm_name,
                                        system_message=system_message,
                                        query='\n'.join(v))
                responses.append(res_chat)
            results.lm_names.append(lm_name)
            results.outputs.append(format_as_markdown('\n'.join(responses)))
        output_path = Path.joinpath(result_dir, docx_path.stem + '.json')
        with open(output_path, 'w') as f:
            json.dump(results.model_dump(), f, indent=2, ensure_ascii=False)

        print('evaluation took {:.2f} seconds'.format(time.time() - start_t))


if __name__ == '__main__':
    main()
