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
    
@register.inclusion_tag('dardos/includes/estadisticas_jugadores.html')
def show_estadisticas_jugadores(jugadores):
    return {'show_details' : True,
        'jugadores' : jugadores}
    
@register.inclusion_tag('dardos/includes/estadisticas_jugadores.html')
def show_estadisticas_jugador(jugador):
    return {'show_details' : False,
        'jugadores' : (jugador,)}
    
@register.inclusion_tag('dardos/equipos/estequipo.html')
def show_estadisticas_equipo(estadisticas):
    return {'estadisticas' : estadisticas}
    
@register.inclusion_tag('dardos/equipos/estparejasgeneral.html')
def show_estadisticas_parejas_general(estadistica):
    return {'estadistica' : estadistica}
    
@register.inclusion_tag('dardos/equipos/estparejasanalisis.html')
def show_estadisticas_parejas_analisis(estadistica):
    return {'estadistica' : estadistica}
    
