# -*- mode: python; tab-width: 4; indent-tabs-mode: nil -*-

from djdardos.dardos.models import *
from djdardos.mb.models import *
from django.contrib.contenttypes.models import ContentType

from django import template

register = template.Library()

@register.inclusion_tag('mb/tags/lista_tweets.html', takes_context = True)
def tweets_jugador(context):
    request = context['request']
    if request.user.get_profile() and request.user.get_profile().jugador:
        ct = ContentType.objects.get_for_model(request.user.get_profile().jugador)
        tweets = Tweet.objects.filter(sender_type=ct.id, sender_id=request.user.get_profile().jugador.id)
    else:
        tweets = []
    return {'tweets': tweets}

