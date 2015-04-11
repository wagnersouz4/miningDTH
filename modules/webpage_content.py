#!/bin/env python3
# -*- coding:utf-8 -*-

from bs4 import BeautifulSoup
from requests import get
from nltk import word_tokenize
from nltk.corpus import stopwords
import re


class WebPageContent(object):

    def __init__(self, pages):
        self.get_content(pages)

    def get_content(self, pages):

        self.pages_content_list = []
        # make sure that pages is a list
        if(pages.__class__ != str and hasattr(pages, '__iter__')):
            for page in pages:

                # obtaining the page text
                soup = BeautifulSoup(get(page).text)

                # if the data was obtained successfully
                if soup:
                    self.pages_content_list.append(
                        self.main_soup_content(soup))

    def main_soup_content(self, soup):
        content = ''

        # using the html tag <p>, <h1-h5> and <span> as a source of information
        for tag in soup.findAll(['p', 'h1', 'h2', 'h3', 'h4', 'h5']):

            # if there is content between the tags
            if tag.string:
                content += ' '+tag.string+' '

        # using the html tag <title> as a source as well
        if soup.title:
            content += ' '+soup.title.string+' '

        return self.clean_text(self.remove_http(content))

    def clean_text(self, text):

        symbols = '! @ # $ % ^ & * ( ) - _ + = == { [ } \
                   ] \\ | : ; \' \" ? / . > < , \n \r'

        # removing special symbos and blank space duplicates
        for s in symbols.split(' '):
            text = text.replace(s, '')

        return self.remove_stopwords(text.replace('  ', '').strip())

    def remove_http(self, text):

        if 'http://' in text:
            text = re.sub('http://.*', '', text).rstrip()
        return text

    def remove_stopwords(self, text):
        stop = stopwords.words('english')
        return ' '.join([t for t in word_tokenize(text) if t not in stop])
