#!/bin/python
import argparse
import logging
import sys

from build.libs.generator import generate, generate_all

# Command line parsing

parser = argparse.ArgumentParser(description="Generates a whole tree of mock data files",
                                 formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument("--src", help="source directory tree")
parser.add_argument("--dest", help="destination directory tree", default=".")
parser.add_argument("--clear-directory", help="clears the destination directory before generating data files", default=True)
args = parser.parse_args()

# Some inits
logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)

generate_all(args.src, args.dest, args.clear_directory)
