#!/bin/python
import argparse
import logging
import sys

from build.libs.generator import generate

# Command line parsing

parser = argparse.ArgumentParser(description="Generates a set of mock data files from the given descriptor file",
                                 formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument("--src", help="descriptor file path")
parser.add_argument("--dest", help="destination directory", default=".")
parser.add_argument("--clear-directory", help="clears the destination directory before generating data files", default=False)
args = parser.parse_args()

# Some inits
logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)

generate(args.src, args.dest, args.clear_directory)
