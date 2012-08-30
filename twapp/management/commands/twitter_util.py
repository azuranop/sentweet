# -*- coding: utf-8 -*-

import sys
import locale
import twitter
import redis
import json
import time
from random import shuffle
from urllib2 import URLError
from twitter_login import login

def makeTwitterRequest(t, twitterFunction, max_errors=3, *args, **kwArgs): 
    wait_period = 2
    error_count = 0
    while True:
        try:
            return twitterFunction(*args, **kwArgs)
        except twitter.api.TwitterHTTPError, e:
            error_count = 0
            wait_period = handleTwitterHTTPError(e, t, wait_period)
            if wait_period is None:
                return
        except URLError, e:
            error_count += 1
            print >> sys.stderr, "URLError encountered. Continuing."
            if error_count > max_errors:
                print >> sys.stderr, "Too many consecutive errors...bailing out."
                raise

if __name__ == '__main__': # For ad-hoc testing

    def makeTwitterRequest(t, twitterFunction, *args, **kwArgs): 
        wait_period = 2
        while True:
            try:
                e = Exception()
                e.code = 401
                #e.code = 502
                #e.code = 503
                raise twitter.api.TwitterHTTPError(e, "http://foo.com", "FOO", "BAR")
                return twitterFunction(*args, **kwArgs)
            except twitter.api.TwitterHTTPError, e:
                wait_period = handleTwitterHTTPError(e, t, wait_period)
                if wait_period is None:
                    return

    t = login()
    makeTwitterRequest(t, t.friends.ids, screen_names=['ladygaga'])
