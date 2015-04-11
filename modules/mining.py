#!/bin/env python3
# -*- coding:utf-8 -*-

from google_concept import GoogleConcept
from tf import TF
from IR import IR
from datetime import date


class Mining(object):

    def __init__(self, json_doc):
        self.json_doc = json_doc
        self.build()

    def build(self):
        google_concept = GoogleConcept(self.json_doc['title'] + ' ' +
                                       self.json_doc['explanation'],
                                       pages_limit=15)

        tf = TF(google_concept.content)
        print(tf.topwords(3))


if __name__ == '__main__':
    # Building the thing
    ir = IR()
    m = Mining(ir.getInfo(date(2015, 4, 10)))
