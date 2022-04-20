import argparse


def create_args():
    args = argparse.ArgumentParser()
    args.add_argument("--input", nargs=1, help="input")
    args.add_argument("--source", nargs=1, help="source")


    args = args.parse_args()


    return args


def get_source(args):
    if args.source:
        try:
            src = open(str(args.source[0]))
        except:
            exit(11)
        return src


def get_read_input(args):
    if args.input:
        try:
            read_input = open(str(args.input[0]))
        except:
            exit(11)
        return read_input
