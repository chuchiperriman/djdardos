# -*- mode: python; tab-width: 4; indent-tabs-mode: nil -*-
from django.db import models
from django.db.models import Q
from djdardos.dardos.models import *
from djdardos.dardos.equipos.estadisticas import *

class DatosEquipo:
    
    def __init__(self, equipo, liga):
        self.equipo = equipo
        self.liga = liga
        self.estadisticas = EstadisticasEquipo(equipo, liga)
    

class Clasificacion:
    def __init__(self, liga):
        self.liga = liga
        self.equipos = []
        for equipo in liga.equipo_set.all():
            self.equipos.append(DatosEquipo(equipo, liga))
        
        self.equipos.sort(key=lambda datos: datos.estadisticas.puntos(), reverse=True)
                
