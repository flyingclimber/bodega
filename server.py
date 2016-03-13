#!/usr/bin/env python

'''
server.py - Mini flask API
'''

import json
from fuzzywuzzy import fuzz
from flask import Flask, request, jsonify
from ConfigParser import ConfigParser
import os.path

APP = Flask(__name__)


class Bodega:
    """
        Represents a local market with different types of vendors
    """
    def __init__(self):
        self.jsonindex = 'index.json'
        self.configfile = 'bodega.conf'
        self.api_keys = []
        self.loadconfig()
        self.loadindex()

    def loadconfig(self):
        config = ConfigParser()
        config.readfp(open(self.configfile))
        self.api_keys.append(config.get('API_KEYS', 'KEYS'))

    def loadindex(self):
        if not os.path.isfile(self.jsonindex):
            self.saveindex()

        with open(self.jsonindex) as f:
            self.index = MerchantIndex(json.load(f))

    def saveindex(self):
        with open(self.jsonindex, 'w') as g:
            g.write(json.dumps(self.index.getmerchants()))

    def validapikey(self, key):
        if key in self.api_keys:
            return True
        else:
            return False


class Merchant:
    """
        Individual seller and their details
    """
    def __init__(self, name, category=''):
        self.name = name
        self.category = category


class MerchantIndex:
    """
        The roster of merchants
    """
    def __init__(self, items=''):
        self.merchants = items

    def getmerchantcategory(self, merchant):
        if merchant.name in self.merchants:
            return self.merchants[merchant.name]
        else:
            return ''

    def getmerchants(self):
        return self.merchants

    def addmerchant(self, merchant, category=''):
        self.merchants[merchant.name] = category

    def search(self, term):
        keys = self.merchants.keys()
        res = ''

        for key in keys:
            if fuzz.partial_ratio(term.name, key) > 70:
                res = self.merchants[key]
        return res


@APP.route("/get/<name>")
def get_merchant(name):
    merchant = Merchant(name.lower())
    category = bodega.index.getmerchantcategory(merchant)

    if category:
        res = category
    else:
        res = bodega.index.search(name)

    return jsonify(results=res)


@APP.route("/add", methods=['POST'])
def add_category():

    merchant_name = request.form['merchant'].lower()
    category = request.form['category']
    api_key = request.form['api_key']

    merchant = Merchant(merchant_name, category)

    if not api_key:
        res = 'NO API KEY'
    elif not bodega.validapikey(api_key):
        res = 'INVALID API KEY'
    else:
        if bodega.index.getmerchantcategory(merchant) or\
                        bodega.index.search(merchant) != '':
            res = 'Already Present'
        else:
            bodega.index.addmerchant(merchant, category)
            bodega.saveindex()
            res = 'Added'

    return jsonify(results=res)

if __name__ == "__main__":
    bodega = Bodega()

    APP.run(host='0.0.0.0', debug='true')

