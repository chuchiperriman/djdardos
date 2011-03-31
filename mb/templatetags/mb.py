# -*- mode: python; tab-width: 4; indent-tabs-mode: nil -*-

from djdardos.dardos.models import *
from djdardos.mb.models import *
from django.contrib.contenttypes.models import ContentType

from django import template

register = template.Library()

@register.inclusion_tag('mb/tags/lista_tweets.html', takes_context = True)
def tweets_jugador(context, jugador):
    request = context['request']
    if jugador:
        ct = ContentType.objects.get_for_model(jugador)
        tweets = Tweet.objects.filter(sender_type=ct.id, sender_id=jugador.id)
    else:
        tweets = []
    return {'tweets': tweets}

