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
    system_message = sm['medical_analyst_binary_1']['system']
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
                        default='medical_analyst_binary_1')
    return parser




if __name__ == '__main__':
    main()
