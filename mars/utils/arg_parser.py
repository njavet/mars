import argparse

# project imports
from mars.conf import instruct_3b


def create_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('--base_url',
                        dest='base_url',
                        type=str,
                        default='http://localhost:11434',
                        help='ollama base url')
    parser.add_argument('--model_name',
                        dest='model_name',
                        type=str,
                        default=instruct_3b,
                        help='select the model')
    parser.add_argument('--debug',
                        dest='debug',
                        type=bool,
                        default=False,
                        help='debug mode prints log messages')
    return parser
