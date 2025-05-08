import time
from pathlib import Path
from argparse import ArgumentParser
import json
import os

# project imports
from mars.conf.conf import DOCX_DIR, RESULTS_DIR
from mars.utils.helpers import (read_docx,
                                format_as_markdown,
                                get_number_of_runs,
                                load_system_messages)
from mars.schemas import Evaluation
from mars.service.service import (get_lms, run_baseline)


def main():
    parser = create_parser()
    args = parser.parse_args()
    system_messages = load_system_messages()
    runs = get_number_of_runs()
    os.mkdir(f'{RESULTS_DIR}/run{runs}')
    system_message = """
    Du bist ein medizinischer Assistent.
Analysiere den folgenden psychiatrischen Entlassungsbericht.
Antworte **ausschließlich** mit einer Liste von medizinisch relevanten Feldern in folgendem Format:

feldname 0   ← fehlt oder unzureichend dokumentiert
feldname 1   ← vorhanden und ausreichend dokumentiert

Beispielausgabe:
substanz_anamnese 0
familien_anamnese 1
forensik 0

Vermeide jegliche Erklärungen, Einleitungen oder Begründungen.
Antworte nur mit der Liste.
    """
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
    lms = ['openhermes:latest']
    print(system_message)
    for docx_path in DOCX_DIR.glob('*.docx'):
        start_t = time.time()
        text = read_docx(docx_path)
        print('evaluating {}'.format(docx_path))
        results = Evaluation(server=base_url,
                             filename=docx_path.name,
                             system_message=system_message)
        for lm_name in lms:
            print('lm_name: ', lm_name)
            res_chat = run_baseline(base_url=base_url,
                                    lm_name=lm_name,
                                    system_message=system_message,
                                    query=text,
                                    chat_mode=False)
            results.lm_names.append(lm_name)
            results.outputs.append(format_as_markdown(res_chat))
        output_path = Path.joinpath(result_dir, docx_path.stem + '.json')
        with open(output_path, 'w') as f:
            json.dump(results.model_dump(), f, indent=2, ensure_ascii=False)

        print('evaluation took {:.2f} seconds'.format(time.time() - start_t))


if __name__ == '__main__':
    main()
