
import re
from string import punctuation

# Takes a tweet and extract meaningful words

def extractwords(tweet):

  splitter = re.compile('\\W*')
  items = [s.lower() for s in splitter.split(tweet) if s!='']

  ignorewords = set([ 'the', 'of', 'to', 'and', 'a', 'in', 'is', 'it', 'from', 'for', 'by', 's', 'on', 'about', 'you', 'we', 'are', 'has', 'have', 'that', 'eu', 'at', 'as', 'which', 'they', 'or', 'says', 'say', 'all', 'an', 'with', 'one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine', 'ten', 'into', 'us'])

  words_filtered = [e for e in items if ((e in ignorewords) | (len(e) >= 3))]

  return(words_filtered)

