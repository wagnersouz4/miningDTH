#!/bin/env python3
# -*- coding:utf-8 -*-

from math import log2


class TF(object):
    def __init__(self, text):
        self.text = text
        self.build()

    def build(self):
        self.tf_list = []
        term_visited = []
        for term in self.text.split(' '):
            if term not in term_visited and self.isEnglish(term):
                term_visited.append(term)
                self.tf_list.append((term, 1 +
                                     log2(self.text.count(term))))

        # ordering the list according to its tf value
        self.tf_list.sort(key=lambda x: float(x[1]), reverse=True)

    def topwords(self, nwords):
        return [x[0] for x in self.tf_list[:nwords]]

    def isEnglish(self, word):
        try:
            word.encode('utf8').decode('ascii')
        except UnicodeDecodeError:
            return False
        else:
            return True
