import argparse
from .version import *
from .proj import *


def arg_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('--version',
                        action='version',
                        version=f'{PROJECT} {get_version()}')
    parser.add_argument(
        '-i',
        '--ide',
        choices=[vscode_ide_name],
        default=vscode_ide_name)
    parser.add_argument('proj_type', choices=['app', 'lib'])
    parser.add_argument('dir', type=str)
    return parser
