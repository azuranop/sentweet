
# Add to use bigint

from django.db.models.fields import IntegerField
from django.conf import settings

class BigIntegerField(IntegerField):
    empty_strings_allowed=False
    def get_internal_type(self):
        return "BigIntegerField"
    def db_type(self):
        return 'bigint' # Note this won't work with Oracle.

from django.db import models

class Tweet(models.Model):
      datetime = models.DateTimeField('date published')
      user = models.CharField(max_length=20)
      content = models.CharField(max_length=150)
      source = models.CharField(max_length=100)
      tweet_id = BigIntegerField()
      prop = models.IntegerField()

