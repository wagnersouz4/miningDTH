#!/bin/env python3
# -*- coding:utf-8 -*-

import json
from google_concept import GoogleConcept
from tf import TF


class Mining(object):

    def __init__(self, json_doc):
        self.json_doc = json_doc
        self.build()

    def build(self):
        print(self.json_doc['title'])
        google_concept = GoogleConcept(self.json_doc['title'], pages_limit=15)
        tf = TF(google_concept.content)
        print(tf.topwords(3))



url = 'https://api.data.gov/nasa/planetary/apod?concept_tags=True&api_key=nBU6LULSiOfryhokGBZVH6hvfu5I00WHZhtDFWLx&date=2015-04-10'
from requests import get
json = json.loads(get(url).text)
m = Mining(json)

