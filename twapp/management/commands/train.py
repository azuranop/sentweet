# Collect positive tweets (emoticon :)) and train the Bayes classifier

# -*- coding: utf-8 -*-

import twitter
import nltk.classify.util
import pickle
from nltk.classify import NaiveBayesClassifier

from extractwords import extractwords, word_feats
from django.core.management.base import BaseCommand
from web.twapp.models import Tweet
from twitter_login import login
from twitter_util import makeTwitterRequest

class Command(BaseCommand):
    help = 'Retrieve the tweets'

    def handle(self, *args, **options):

        n = 10   # Number of training tweets
        SEARCH_TERM = ':)'
        
        MAX_PAGES = 1
        RESULTS_PER_PAGE = 1
        LANGUAGE = "en"
        INCLUDE_ENTITIES = "true"

        KW = {
            'domain': 'search.twitter.com',
            'count': 1000,
            'rpp': 100,
            'q': SEARCH_TERM,
            'lang': LANGUAGE,
            'include_entities': INCLUDE_ENTITIES 
            }

        t = twitter.Twitter(domain='search.twitter.com')

        posfeats = []

        for i in range(n):

               tweets = makeTwitterRequest(t, t.search, **KW)

               txt = tweets['results'][0]['text']
               itemb = extractwords(txt)
               posfeats.append((word_feats(itemb), '1'))

        classifier = NaiveBayesClassifier.train(posfeats)

        f = open('bayesclass.pickle', 'wb')
        pickle.dump(classifier, f)
        f.close()

