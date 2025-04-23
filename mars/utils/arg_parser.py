import argparse


def create_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('--base_url',
                        dest='base_url',
                        type=str,
                        default='http://localhost:11434',
                        help='ollama base url')
    parser.add_argument('--debug',
                        dest='debug',
                        type=bool,
                        default=False,
                        help='debug mode prints log messages')
    return parser
