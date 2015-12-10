#!/usr/bin/env python

'''
cli.py - Command line tool to query index
'''

import argparse
import json
from fuzzywuzzy import fuzz

PARSER = argparse.ArgumentParser(description='category lookup')
PARSER.add_argument('merchant', type=str, help='merchant to lookup')

ARGS = PARSER.parse_args()
MERCHANT = ARGS.merchant.lower()

INDEX_NAME = 'index.json'

with open(INDEX_NAME) as f:
    INDEX = json.load(f)

if MERCHANT in INDEX:
    print INDEX[MERCHANT]
else:
    KEYS = INDEX.keys()
    for key in KEYS:
        if fuzz.partial_ratio(MERCHANT, key) > 70:
            print "FZ", key, INDEX[key]

