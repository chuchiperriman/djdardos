# -*- mode: python; tab-width: 4; indent-tabs-mode: nil -*-

from djdardos.dardos.models import *
from django.db import models
from django.db.models import Q

class EstadisticasEquipo:
    def __init__(self, equipo):
        self.equipo = equipo
        
    def partidos_jugados(self):
        return Partido.objects.filter(Q(equipo_local=self.equipo) | Q(equipo_visitante=self.equipo)).count()
        
    def partidos_ganados(self):
        return Partido.objects.filter(ganador=self.equipo).count()

    def partidos_perdidos(self):
        return Partido.objects.exclude(ganador=self.equipo).count()
        
    def partidos_jugados_local(self):
        return Partido.objects.filter(Q(equipo_local=self.equipo)).count()
        
    def partidos_ganados_local(self):
        return Partido.objects.filter(Q(equipo_local=self.equipo) & Q(ganador=self.equipo)).count()

    def partidos_perdidos_local(self):
        return Partido.objects.filter(Q(equipo_local=self.equipo)).exclude(ganador=self.equipo).count()

    def partidos_jugados_visitante(self):
        return Partido.objects.filter(Q(equipo_visitante=self.equipo)).count()
        
    def partidos_ganados_visitante(self):
        return Partido.objects.filter(Q(equipo_visitante=self.equipo) & Q(ganador=self.equipo)).count()

    def partidos_perdidos_visitante(self):
        return Partido.objects.filter(Q(equipo_visitante=self.equipo)).exclude(ganador=self.equipo).count()
        
