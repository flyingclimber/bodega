#!/usr/bin/env python

import argparse
import json
from fuzzywuzzy import fuzz

PARSER = argparse.ArgumentParser(description='category lookup')
PARSER.add_argument('merchant', type=str, help='merchant to lookup')

ARGS = PARSER.parse_args()
MERCHANT = ARGS.merchant.lower()

INDEX = 'index.json'
LENGTH = 8

with open(INDEX) as f:
    MERCHANTS = json.load(f)

    if MERCHANTS.has_key(MERCHANT[:LENGTH]):
        print MERCHANTS[MERCHANT[:LENGTH]]
    else:
        keys = MERCHANTS.keys()
        for key in keys:
            if fuzz.partial_ratio(ARGS.merchant, key) > 70:
                print 'FZ', MERCHANTS[key]

