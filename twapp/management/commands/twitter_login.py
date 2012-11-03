# -*- coding: utf-8 -*-

import os
import twitter
import config 

from twitter.oauth import write_token_file, read_token_file
from twitter.oauth_dance import oauth_dance


def login():

    c = config.Config()
    d = c.cfg
    
    app_name = d.get('twitter', 'app_name')
    consumer_key = d.get('twitter', 'consumer_key')
    consumer_secret = d.get('twitter', 'consumer_secret')
    token_file = d.get('twitter', 'token_file')

    try:
        (oauth_token, oauth_token_secret) = read_token_file(token_file)
    except IOError, e:
        (oauth_token, oauth_token_secret) = oauth_dance(app_name, consumer_key,
                consumer_secret)

        if not os.path.isdir('out'):
            os.mkdir('out')

        write_token_file(token_file, oauth_token, oauth_token_secret)
         
    return twitter.Twitter(domain='api.twitter.com', api_version='1',
                        auth=twitter.oauth.OAuth(oauth_token, oauth_token_secret, consumer_key, consumer_secret))

if __name__ == '__main__':
    login()
