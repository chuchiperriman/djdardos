# -*- mode: python; tab-width: 4; indent-tabs-mode: nil -*-
from djdardos.dardos.models import *
from djdardos.dardos.liga.clasificacion import *

from django import template

register = template.Library()

@register.inclusion_tag('dardos/includes/menu_divisiones.html')
def show_divisiones():
    return {'divisiones' : Division.objects.all()}


@register.inclusion_tag('dardos/includes/clasificacion.html')
def show_clasificacion(liga, equipo = None):
    clasificacion = Clasificacion(liga)
    return {'clasificacion' : clasificacion,
        'equipo' : equipo}
    
@register.inclusion_tag('dardos/includes/partida_parejas.html')
def show_partida_parejas(partidas):
    return {'partidas' : partidas}
    
@register.inclusion_tag('dardos/includes/partida_individuales.html')
def show_partida_individuales(partidas):
    return {'partidas' : partidas}
