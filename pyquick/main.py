import argparse

def arg_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('--version', action='version', version='quick 0.0.1')
    return parser

def main():
    args = arg_parser().parse_args()

if __name__ == '__main__':
    main()
