import argparse
import xml.etree.ElementTree as etree


def programArgsHandle():
    args = argparse.ArgumentParser()

    args.add_argument("--input", nargs=1, help="input")
    args.add_argument("--source", nargs=1, help="source")

    return args.parse_args()

def XMLLoad():
    args = programArgsHandle()
    src = open("tests/" + str(args.source[0]))
    readInput = open("tests/" + str(args.input[0]))

    print(src.read())
