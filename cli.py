#!/usr/bin/env python

import argparse
import json
from fuzzywuzzy import fuzz

PARSER = argparse.ArgumentParser(description='category lookup')
PARSER.add_argument('merchant', type=str, help='merchant to lookup')

ARGS = PARSER.parse_args()
MERCHANT = ARGS.merchant.lower()

INDEX = 'index.json'

with open(INDEX) as f:
    MERCHANTS = json.load(f)

merchant = MERCHANT.lower()

if MERCHANTS.has_key(merchant):
    print MERCHANTS[merchant]
else:
    keys = MERCHANTS.keys()
    for key in keys:
        if fuzz.partial_ratio(merchant, key) > 70:
            print "FZ", key, MERCHANTS[key]

