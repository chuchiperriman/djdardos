# -*- mode: python; tab-width: 4; indent-tabs-mode: nil -*-
# -*- coding: utf-8 -*-

from djdardos.dardos.models import *
from djdardos.mb.models import *
from django.contrib.contenttypes.models import ContentType

from django import template

register = template.Library()

@register.inclusion_tag('mb/tags/lista_tweets.html', takes_context = True)
def tweets_object(context, objeto):
    request = context['request']
    if objeto:
        ct = ContentType.objects.get_for_model(objeto)
        tweets = Tweet.objects.filter(sender_type=ct.id, sender_id=objeto.id)
    else:
        tweets = []
    return {'tweets': tweets}

@register.inclusion_tag('mb/tags/lista_tweets.html', takes_context = True)
def tweets_public(context):
    """
    Muestra tweets en el timeline público 
    """
    request = context['request']
    ct = ContentType.objects.get_for_model(Equipo)
    #tweets = Tweet.objects.filter(sender_type=ct.id)
    tweets = Tweet.objects.all()
    return {'tweets': tweets}

