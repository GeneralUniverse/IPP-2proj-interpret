import argparse


def createArgs():
    args = argparse.ArgumentParser()
    args.add_argument("--input", nargs=1, help="input")
    args.add_argument("--source", nargs=1, help="source")

    args = args.parse_args()
    return args


def getSource(args):
    if args.source:
        src = open(str(args.source[0]))
        return src


def getReadInput(args):
    if args.input:
        readInput = open(str(args.input[0]))
        return readInput
