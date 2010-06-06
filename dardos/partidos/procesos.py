# -*- mode: python; tab-width: 4; indent-tabs-mode: nil -*-

from djdardos.dardos.models import *


def calcular_puntos_partidos():
    for p in Partido.objects.all():
        if p.puntos_local != 0 or p.puntos_visitante != 0:
            continue
        jugadores = p.equipo_local.jugador_set.all()
        puntos_local = p.partidaindividual_set.filter(ganador__in=jugadores).count()
        puntos_local += p.partidaparejas_set.filter(Q(ganador1__in=jugadores) | Q(ganador2__in=jugadores)).count()
        
        jugadores = p.equipo_visitante.jugador_set.all()
        puntos_visitante = p.partidaindividual_set.filter(ganador__in=jugadores).count()
        puntos_visitante += p.partidaparejas_set.filter(Q(ganador1__in=jugadores) | Q(ganador2__in=jugadores)).count()
        print p,': ',puntos_local,'-',puntos_visitante
        
        puntos_total = puntos_local + puntos_visitante
        
        if puntos_total > 0 and puntos_total != 16:
            raise Exception("Las partidas de '%s' no son 16!!" % (p))
        p.puntos_local = puntos_local
        p.puntos_visitante = puntos_visitante
        p.save()
        
