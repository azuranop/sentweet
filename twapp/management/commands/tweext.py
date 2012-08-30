# -*- coding: utf-8 -*-

import sys
import time
import twitter
import MySQLdb

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


        # User screen name whose tweets we want to mine

        user = 'ladygaga'

        # For the Twitter API call

        KW = { 'count': 200,
                'skip_users': 'true',
                'include_entities': 'true',
                'since_id': 1,
                'id': user }

        t = login()

        try:

           conn = MySQLdb.connect(**login_db)
           cursor = conn.cursor()

           # Select id of latest tweet in database

           # Database must has been created  
  
           cursor.execute("SELECT max(tweet_id) FROM twapp_tweet WHERE user=%s",(user))
           latestId = cursor.fetchone()
           latestId = latestId[0]

           if latestId == None:
              latestId = 1

           KW['since_id'] = int(latestId)
           print(KW['since_id'])

           print KW

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
              print(created)
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
