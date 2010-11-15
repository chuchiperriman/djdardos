# -*- mode: python; tab-width: 4; indent-tabs-mode: nil -*-

from djdardos.dardos.models import *
from djdardos.dardos.general.sesiones import *

from django import template

register = template.Library()

@register.inclusion_tag('dardos/vista/display_divliga_actual.html', takes_context = True)
def display_divliga_actual(context):
    liga_actual = None
    request = context['request']
    if LIGA_ACTUAL in request.session:
        #TODO Igual mejor guardar el nombre para no ir a bbdd
        liga_actual = Liga.objects.get(pk=request.session[LIGA_ACTUAL])
    elif DIVISION_ACTUAL in request.session:
        #TODO Igual mejor guardar el nombre para no ir a bbdd
        division_actual = Division.objects.get(pk=request.session[DIVISION_ACTUAL])
        liga_actual = division_actual.get_liga_actual()
        
    return {'liga_actual': liga_actual,
        'current_path': request.path}

