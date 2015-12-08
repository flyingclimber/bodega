#!/usr/bin/env python

import argparse
import json

PARSER = argparse.ArgumentParser(description='category lookup')
PARSER.add_argument('merchant', type=str, help='merchant to lookup')

ARGS = PARSER.parse_args()

INDEX = 'index.json'
LENGTH = 8

with open(INDEX) as f:
    MERCHANTS = json.load(f)

    if MERCHANTS.has_key(ARGS.merchant[:LENGTH]):
        print MERCHANTS[ARGS.merchant[:LENGTH]]

