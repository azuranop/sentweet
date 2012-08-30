# -*- coding: utf-8 -*-

import sys
import time
import twitter
import MySQLdb
import json

from training import classifier, extract_features
from extractwords import extractwords
from django.core.management.base import BaseCommand
from web.twapp.models import Tweet
from database import login_db
from twitter_login import login
from twitter_util import makeTwitterRequest
from mysql_date import mysql_date

class Command(BaseCommand):
    help = 'Retrieve the tweets'

    def handle(self, *args, **options):

        Q = ''.join(sys.argv[1])

        MAX_PAGES = 15
        RESULTS_PER_PAGE = 100
        LANGUAGE = "en"
        twitter_search = twitter.Twitter(domain="search.twitter.com")

        search_results = []
        for page in range(1,MAX_PAGES+1):
            search_results += \
            twitter_search.search(q=Q, rpp=RESULTS_PER_PAGE, lang=LANGUAGE, page=page)['results']

        try:

           conn = MySQLdb.connect(**login_db)
           cursor = conn.cursor()


           api_call = getattr(t.statuses, 'user_timeline')
           tweets = makeTwitterRequest(t, api_call, **KW)

           print 'Fetched %i tweets' % len(tweets)

           a = len(tweets)           

           for i in range(a):

              txt = tweets[i]['text']

              b = extractwords(txt)

              outc = int(bool(classifier.classify(extract_features(b))))

              ref = tweets[i]['id']
              src = tweets[i]['source']
              created = mysql_date(tweets[i]['created_at'])

              try:

              # Insert into database 

                cursor.execute ("INSERT INTO  twapp_tweet(user,content,source,tweet_id,datetime,prop) VALUES (%s,%s,%s,%s,%s,%s) ", (user,txt,src,ref,created,outc))
              except MySQLdb.Error, e:
                  print "Error %d: %s" % (e.args[0], e.args[1])

           cursor.close()
           conn.commit()
           conn.close()
           sys.exit(0)

        except MySQLdb.Error, e:
           print "Error %d: %s" % (e.args[0], e.args[1])
           print "While handling %s" % (user)
           sys.exit (1)
