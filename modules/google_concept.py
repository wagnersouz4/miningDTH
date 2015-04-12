#!/usr/bin/env python3
# -*- coding:utf-8 -*-

from google import search
from webpage_content import WebPageContent


class GoogleConcept(object):

    def __init__(self, text, pages_limit=10):
        self.text = text
        self.pages_limit = pages_limit
        self.build()

    def build(self):
        pages = list(search(self.text, stop=self.pages_limit,
                            lang="en"))
        pages_content = WebPageContent(pages)
        self.content = ' '.join(pages_content.pages_content_list)
