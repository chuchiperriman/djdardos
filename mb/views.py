# Create your views here.
from djdardos.mb.models import *
from django.shortcuts import get_object_or_404
from django.views.generic.simple import direct_to_template
from django.http import HttpResponseRedirect
from django.forms import ModelForm
from django.shortcuts import render_to_response
from django.contrib.auth.decorators import login_required
from django.contrib.contenttypes.models import ContentType

class TweetForm(ModelForm):
    class Meta:
        model = Tweet
        exclude = ['sender_type', 'sender_id', 'sent']

def list(request):
    ct = ContentType.objects.get_for_model(request.user)
    tweets = Tweet.objects.filter(sender_type=ct.id, sender_id=request.user.id)
    return direct_to_template(request, 'mb/list.html',
                              {'tweets': tweets})

def new_tweet(request):
    if request.method == 'POST':
        print 'post'
        form = TweetForm(data=request.POST)
                                           
        if form.is_valid():
            new_tweet = form.save(commit=False)
            new_tweet.sender = request.user
            new_tweet.save()
            return HttpResponseRedirect('/mb/list')
            #return HttpResponseRedirect(new_snippet.get_absolute_url())
    else:
        form = TweetForm()

    return direct_to_template(request, 'mb/list.html', {'form': form})

new_tweet = login_required(new_tweet)


