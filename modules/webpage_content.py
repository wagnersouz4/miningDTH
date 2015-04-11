#!/bin/env python3
# -*- coding:utf-8 -*-

from bs4 import BeautifulSoup
from requests import get
from nltk import word_tokenize, tag, data
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
        for html_tag in soup.findAll(['p', 'h1', 'h2',
                                      'h3', 'h4', 'h5']):

            # if there is content between the tags
            if html_tag.string:
                content += tag.string+' '

        # using the html tag <title> as a source as well
        if soup.title:
            content += soup.title.string+' '

        return self.clean_text(content)

    def clean_text(self, text):

        text = self.remove_http(text)

        symbols = '! @ # $ % ^ & * ( ) - _ + = == { [ } \
                   ] \\ | : ; \' \" ? / . > < , \n \r'

        # removing special symbos and blank space duplicates
        for s in symbols.split(' '):
            text = text.replace(s, '')

        text = self.remove_stopwords(text.replace('  ', '').strip())
        return self.meaning_words(text)

    def remove_http(self, text):

        if 'http://' in text:
            text = re.sub('http://.*', '', text).rstrip()
        return text

    def remove_stopwords(self, text):
        stop = stopwords.words('english')
        return ' '.join([t for t in word_tokenize(text) if t not in stop])

    def meaning_words(self, text):

        # meaning tags nouns and adjective only
        meaning_tags = ['NN', 'NNP', 'NNPS', 'JJ']
        default_tagger = data.load(tag._POS_TAGGER)

        meaning_words = ' '.join([w for w, c in default_tagger.tag(
                                 word_tokenize(text)) if c in
                                 meaning_tags and (len(w) > 2)])

        '''if no meaning words are found, using this approach then
            return the whole text
        '''
        if not meaning_words:
            return text.split(' ')
        else:
            return meaning_words
