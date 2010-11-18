# -*- mode: python; tab-width: 4; indent-tabs-mode: nil -*-

from djdardos.dardos.models import *
from djdardos.dardos.general.sesiones import *

from django import template
from django.contrib import messages

register = template.Library()

@register.inclusion_tag('dardos/vista/display_divliga_actual.html', takes_context = True)
def display_divliga_actual(context):
    request = context['request']
    liga_actual = get_liga_actual(request)
    ligas = None
    if liga_actual:
        ligas = Liga.objects.filter(division = liga_actual.division)
    return {'liga_actual': get_liga_actual(request),
        'ligas': ligas,
        'current_path': request.path}

@register.inclusion_tag('dardos/vista/cuadro_login.html', takes_context = True)
def cuadro_login(context):
    request = context['request']
    return {'current_path': get_current_path(request),
            'user' : request.user}

