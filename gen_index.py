#!/usr/bin/env python

'''
gen_index - Generate a bodega index
'''

import json
import os
import argparse

PARSER = argparse.ArgumentParser(description='index generator')
PARSER.add_argument('file', type=str, help='file to read')

ARGS = PARSER.parse_args()

SOURCE = ARGS.file
INDEX = 'index.json'
MERCHANTS = {}

if os.path.isfile(INDEX):
    with open(INDEX) as h:
        MERCHANTS = json.load(h)

with open(SOURCE) as f:
    for line in f:
        item, category = line.rstrip().split(",")
        MERCHANTS[item.lower()] = category

with open(INDEX, 'w') as g:
    g.write(json.dumps(MERCHANTS))
