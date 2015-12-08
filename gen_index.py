#!/usr/bin/env python

'''
gen_index - Generate a crystal ball index
'''

import json
import os
import argparse

PARSER = argparse.ArgumentParser(description='index generator')
PARSER.add_argument('merchant', type=str, help='file to read')

ARGS = PARSER.parse_args()

SOURCE = ARGS.merchant
INDEX = 'index.json'
LENGTH = 8
MERCHANTS = {}

if os.path.isfile(INDEX):
    with open(INDEX) as h:
        MERCHANTS = json.load(h)

with open(SOURCE) as f:
    for line in f:
        item, category = line.rstrip().split("\t")
        MERCHANTS[item[:LENGTH]] = category

with open(INDEX, 'w') as g:
    g.write(json.dumps(MERCHANTS))
