# -*- coding: utf-8 -*-

import twitter
import config 
import pickle

from django.core.management.base import BaseCommand
from webgit.twapp.models import Tweet
from django.db.models import Max

from extractwords import extractwords, word_feats

from twitter_login import login
from twitter_util import makeTwitterRequest

class Command(BaseCommand):

    help = 'Retrieve the tweets and classify them with the Bayesian classifier'

    def handle(self, *args, **options):
 
        # Get the configuration parameters

        c = config.Config()
        d = c.cfg

        # Load the classifier

        f = open('bayesclass.pickle')
        classifier = pickle.load(f)
    
        t = login()


        KW = {'user' : d.get('api', 'user'), 
              'count' : d.get('api', 'count'), 
              'skip_users' : d.get('api', 'skip_users'), 
              'include_entities' : 'true',
              'since_id' : 1, 
              'id' : 2} 

        p = Tweet.objects.aggregate(Max('tweet_id'))
#        print(p)
        latestId = p['tweet_id__max']
        if latestId == None:
           latestId = 1

        KW['since_id'] = int(latestId)
        print(KW['since_id'])

        api_call = getattr(t.statuses, 'user_timeline')
        tweets = makeTwitterRequest(t, api_call, **KW)

        print 'Fetched %i tweets' % len(tweets)

        a = len(tweets)           

        for i in range(a):

            txt = tweets[i]['text']
            ref = tweets[i]['id']
            src = tweets[i]['source']
            outc = int(classifier.classify(word_feats(txt)))
            created = mysql_date(tweets[i]['created_at'])

            q = Tweet( datetime = created, 
                       user = K['user'],
                       content = txt, 
                       source = src,
                       tweet_id = ref,
                       prop = outc )

            q.save()
        f.close()
