#!/usr/bin/env python

'''
cli.py - Command line tool to query index
'''

import argparse
from bodega import Bodega, Merchant

PARSER = argparse.ArgumentParser(description='category lookup')
PARSER.add_argument('merchant', type=str, help='merchant to lookup')

ARGS = PARSER.parse_args()
MERCHANT = Merchant(ARGS.merchant.lower())


def main():
    bodega = Bodega()

    res = bodega.index.get_merchant_category(MERCHANT)

    if not res:
        res = bodega.index.search(MERCHANT)

    print res

if __name__ == "__main__":
    main()
