# -*- mode: python; tab-width: 4; indent-tabs-mode: nil -*-

from djdardos.dardos.models import *
from djdardos.dardos.general.sesiones import *

from django import template

register = template.Library()

@register.inclusion_tag('dardos/vista/display_divliga_actual.html', takes_context = True)
def display_divliga_actual(context):
    request = context['request']
    return {'liga_actual': get_liga_actual(request),
        'current_path': request.path}

