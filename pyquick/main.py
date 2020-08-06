import argparse

def arg_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('--version', action='version', version='quick 0.0.1')
    return parser

def hi(a,b,/,c):
    print(a,b,c)

def main():
    hi('I', 'Like', c='955')
    args = arg_parser().parse_args()

if __name__ == '__main__':
    main()
