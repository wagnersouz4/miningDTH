#!/bin/env python3
# -*- coding:utf-8 -*-

from bs4 import BeautifulSoup
from requests import get
from nltk import word_tokenize, tag, data
from nltk.corpus import stopwords
import re


class WebPageContent(object):

    def __init__(self, pages):
        self.initialize()
        self.get_content(pages)

    def initialize(self):
        '''most common nouns in English, according to
           http://www.linguasorb.com/english/most-common-nouns/
        '''
        common_nouns = ['time', 'issue', 'year', 'side', 'people',
                        'kind', 'way', 'head', 'day', 'house', 'man',
                        'service', 'thing', 'friend', 'woman', 'father',
                        'life', 'power', 'child', 'hour', 'world',
                        'game', 'school', 'line', 'state', 'end',
                        'family', 'member', 'student', 'law', 'group',
                        'car', 'country', 'city', 'problem',
                        'community', 'hand', 'name', 'part',
                        'president', 'place', 'team', 'case', 'minute',
                        'week', 'idea', 'company', 'kid', 'system',
                        'body', 'program', 'information', 'question',
                        'back', 'work', 'parent', 'government', 'face',
                        'number', 'others', 'night', 'level', 'Mr',
                        'office', 'point', 'door', 'home', 'health',
                        'water', 'person', 'room', 'art', 'mother',
                        'war', 'area', 'history', 'money', 'party',
                        'storey', 'result', 'fact', 'change', 'month',
                        'morning', 'lot', 'reason', 'right', 'research',
                        'study', 'girl', 'book', 'guy', 'eye', 'food',
                        'job', 'moment', 'word', 'air', 'business',
                        'teacher']

        common_nouns_capitalzie = [noun.capitalize() for noun
                                   in common_nouns]

        common_nouns_upper = [noun.upper() for noun in common_nouns]

        extra = ['The', 'THE','New', 'new', 'hubble', 'Hubble', 'Space', 'space',
                 'News', 'news', 'Astro', 'astro', 'He', 'She', 'It', 'You', 'We', 'They']

        self.common_words = common_nouns+common_nouns_upper+common_nouns_capitalzie+extra

    def get_content(self, pages):

        self.pages_content_list = []
        # make sure that pages is a list
        if(pages.__class__ != str and hasattr(pages, '__iter__')):
            for page in pages:

                # obtaining the page text
                soup = BeautifulSoup(get(page).text)

                # if the data was obtained successfully
                if soup:
                    text = self.main_soup_content(soup)
                    if text.__class__ == str:
                        self.pages_content_list.append(text)

    def main_soup_content(self, soup):
        content = []

        # using the html tag <p>, <h1-h5> and <span> as a source of information
        for html_tag in soup.findAll(['p', 'h1', 'h2',
                                      'h3', 'h4', 'h5']):

            # if there is content between the tags
            if html_tag.string:
                content.append(html_tag.string + ' ')

        # using the html tag <title> as a source as well
        if soup.title:
            content.append(soup.title.string + ' ')
        return self.clean_text(' '.join(content))

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

    # create a duty tagger
    def meaning_words(self, text):



        # meaning tags nouns and adjective only
        meaning_tags = ['NN', 'NNP', 'NNPS', 'JJ']
        default_tagger = data.load(tag._POS_TAGGER)

        ''' sometimes the nltk tagger is misclassifying some part-of-speech
            such as The that should be a determiner. The duty tagger also helps
            to eliminate common words that are not so important
        '''
        duty = dict()
        [duty.update({w:'x'}) for w in self.common_words]

        enchaned_tagger = tag.UnigramTagger(model=duty, backoff=default_tagger)

        meaning_words = ' '.join([w for w, c in enchaned_tagger.tag(
                                 word_tokenize(text)) if c in
            meaning_tags and (len(w) > 2)])

        '''if no meaning words are found, using this approach then
            return the whole text
        '''
        if not meaning_words:
            return None
        else:
            return meaning_words
