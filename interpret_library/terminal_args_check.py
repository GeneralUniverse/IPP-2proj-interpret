import argparse


def create_args():
    args = argparse.ArgumentParser()
    args.add_argument("--input", nargs=1, help="input")
    args.add_argument("--source", nargs=1, help="source")

    args = args.parse_args()
    return args


def get_source(args):
    if args.source:
        src = open(str(args.source[0]))
        return src


def get_read_input(args):
    if args.input:
        read_input = open(str(args.input[0]))
        return read_input
