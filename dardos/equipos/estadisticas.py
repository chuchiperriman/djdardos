# -*- mode: python; tab-width: 4; indent-tabs-mode: nil -*-

from djdardos.dardos.models import *
from django.db import models
from django.db.models import Q

class EstadisticasEquipo:
    def __init__(self, equipo):
        self.equipo = equipo
    
    def partidos_jugados(self):
        return Partido.objects.filter(Q(jugado=True) & (Q(equipo_local=self.equipo) | Q(equipo_visitante=self.equipo))).count()
        
    def partidos_ganados(self):
        return Partido.objects.filter(Q(jugado=True) & Q(ganador=self.equipo)).count()

    def partidos_perdidos(self):
        return Partido.objects.filter(Q(jugado=True) & (Q(equipo_local=self.equipo) | 
            Q(equipo_visitante=self.equipo))).exclude(
                Q(ganador=self.equipo) | Q(ganador=None)).count()
    
    def partidos_empatados(self):
        return Partido.objects.filter(Q(jugado=True) & Q(ganador=None) & 
            (Q(equipo_local=self.equipo) | Q(equipo_visitante=self.equipo))).count()
        
    def partidos_jugados_local(self):
        return Partido.objects.filter(Q(jugado=True) & Q(equipo_local=self.equipo)).count()
        
    def partidos_ganados_local(self):
        return Partido.objects.filter(Q(jugado=True) & Q(equipo_local=self.equipo) & Q(ganador=self.equipo)).count()

    def partidos_perdidos_local(self):
        return Partido.objects.filter(Q(jugado=True) & Q(equipo_local=self.equipo)).exclude(
            Q(ganador=self.equipo) | Q(ganador=None)).count()

    def partidos_empatados_local(self):
        return Partido.objects.filter(Q(jugado=True) & Q(equipo_local=self.equipo) & Q(ganador=None)).count()
        
    def partidos_jugados_visitante(self):
        return Partido.objects.filter(Q(jugado=True) & Q(equipo_visitante=self.equipo)).count()
        
    def partidos_ganados_visitante(self):
        return Partido.objects.filter(Q(jugado=True) & Q(equipo_visitante=self.equipo) & Q(ganador=self.equipo)).count()

    def partidos_perdidos_visitante(self):
        return Partido.objects.filter(Q(jugado=True) & Q(equipo_visitante=self.equipo)).exclude(
            Q(ganador=self.equipo) | Q(ganador=None)).count()
    
    def partidos_empatados_visitante(self):
        return Partido.objects.filter(Q(jugado=True) & Q(equipo_visitante=self.equipo) & Q(ganador=None)).count()
            
    def puntos(self):
        return self.partidos_ganados() * 2 + self.partidos_empatados()
        
