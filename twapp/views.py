
from django.template import Context, loader
from twapp.models import Tweet
from django.http import HttpResponse

def index(request):
    latest_tweets_list = Tweet.objects.all().order_by('-datetime')[:10]
    t = loader.get_template('twapp/index.html')
    c = Context({
        'latest_tweets_list': latest_tweets_list,
    })
    return HttpResponse(t.render(c))
