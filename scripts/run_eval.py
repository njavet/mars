import argparse
import toml

# project imports
from mars.service.eval import Evaluator


def main():
    parser = create_argparser()
    args = parser.parse_args()
    sms = toml.load('mars/conf/prompts.toml')
    try:
        system_message = sms[args.preprompt]['system']
    except KeyError:
        print('No such preprompt')
    else:
        e = Evaluator(base_url=args.base_url,
                      system_message=system_message)
        e.run_eval()


def create_argparser():
    parser = argparse.ArgumentParser()
    parser.add_argument('-s',
                        '--server',
                        dest='base_url',
                        default='http://localhost:11434')
    parser.add_argument('-p',
                        '--preprompt',
                        dest='preprompt',
                        default='medical_analyst_1')
    return parser


if __name__ == '__main__':
    main()
