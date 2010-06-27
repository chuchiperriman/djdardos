# -*- mode: python; tab-width: 4; indent-tabs-mode: nil -*-

from djdardos.dardos.models import *


def actualizar_puntos_partido(p):

    jugadores = p.equipo_local.jugador_set.all()
    puntos_local = p.partida_set.filter(ganadores__in=jugadores).distinct().count()
    
    jugadores = p.equipo_visitante.jugador_set.all()
    puntos_visitante = p.partida_set.filter(ganadores__in=jugadores).distinct().count()
    print p,': ',puntos_local,'-',puntos_visitante
    
    puntos_total = puntos_local + puntos_visitante
    
    if puntos_total > 0 and puntos_total != 16:
        raise Exception("Las partidas de '%s' no son 16!!" % (p))
        
    p.puntos_local = puntos_local
    p.puntos_visitante = puntos_visitante
    p.jugado = True
    p.save()
    return True
    
def actualizar_puntos_partidos():
    for p in Partido.objects.all():
        actualizar_puntos_partido(p)
        
