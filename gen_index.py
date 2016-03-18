#!/usr/bin/env python

'''
gen_index - Generate a bodega index
'''

import argparse
from server import Bodega, Merchant

PARSER = argparse.ArgumentParser(description='index generator')
PARSER.add_argument('file', type=str, help='file to read')

ARGS = PARSER.parse_args()
SOURCE = ARGS.file


if __name__ == "__main__":
    bodega = Bodega()

    with open(SOURCE) as f:
        for line in f:
            item, category = line.rstrip().split(",")
            merchant = Merchant(item)
            bodega.index.add_merchant(merchant, category)

    bodega.saveindex()
