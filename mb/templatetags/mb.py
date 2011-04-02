# -*- mode: python; tab-width: 4; indent-tabs-mode: nil -*-
# -*- coding: utf-8 -*-

from djdardos.dardos.models import *
from djdardos.mb.models import *
from django.contrib.contenttypes.models import ContentType
from django.core.paginator import Paginator, InvalidPage, EmptyPage

from django import template

register = template.Library()

def get_tweet_pagination (request, tweet_list):
    #TODO cambiar 5 por algo configurable o más real
    paginator = Paginator(tweet_list, 5)
    try:
        page = int(request.GET.get('page', '1'))
    except ValueError:
        page = 1

    try:
        tweets = paginator.page(page)
    except (EmptyPage, InvalidPage):
        tweets = paginator.page(paginator.num_pages)
    
    return tweets

@register.inclusion_tag('mb/tags/lista_tweets.html', takes_context = True)
def tweets_object(context, objeto):
    request = context['request']
    if objeto:
        ct = ContentType.objects.get_for_model(objeto)
        tweet_list = Tweet.objects.filter(sender_type=ct.id, sender_id=objeto.id)
    else:
        tweets_list = []
        
    return {'tweets': get_tweet_pagination(request, tweet_list)}

@register.inclusion_tag('mb/tags/lista_tweets.html', takes_context = True)
def tweets_public(context):
    """
    Muestra tweets en el timeline público 
    """
    request = context['request']

    ct = ContentType.objects.get_for_model(Equipo)
    #tweets = Tweet.objects.filter(sender_type=ct.id)
    tweet_list = Tweet.objects.all()

    return {'tweets': get_tweet_pagination(request, tweet_list)}

