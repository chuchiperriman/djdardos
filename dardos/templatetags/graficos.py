# -*- mode: python; tab-width: 4; indent-tabs-mode: nil -*-
# -*- coding: utf-8 -*-

from djdardos.dardos.models import *

from django import template

register = template.Library()

class DatoGrafico:
    def __init__(self, x, y):
        self.x = x
        self.y = y

class LineaGrafico:
    def __init__(self, label=""):
        self.label = label
        self.datos = list()

class DatosJornadaGP:
    def __init__(self, num_jornada, ganados, perdidos):
        self.num_jornada = num_jornada
        self.ganados = ganados
        self.perdidos = perdidos

class GraficoEvolucion:
    def __init__(self, titulo, div_id="chartdiv", 
        range_x=range (0,17), range_y=range (0,100,10)):
        self.titulo = titulo
        self.div_id = div_id
        self.__lineas = list()
        self.count = 1
        self.range_x = range_x
        self.range_y = range_y
        
    def range_x(self):
        return range_x
        
    def range_y(self):
        return range_y
        
    def add_linea(self, linea):
        linea.id = self.count
        self.count += 1
        self.__lineas.append(linea)
        
    def get_lineas(self):
        return self.__lineas

class GraficoEvolucionGanadas (GraficoEvolucion):
    def __init__(self, div_id="chartdiv"):
        GraficoEvolucion.__init__(self,"Porcentaje ganadas", div_id)
        
    def calcular(self, jugador):
        linea = LineaGrafico("Partidas ganadas")
        #TODO Filtrar por temporada o liga etc.
        jornadas = Jornada.objects.all()
        for jor in jornadas:
            partidos = jor.partido_set.filter(
                Q(equipo_local=jugador.equipo) | Q(equipo_visitante=jugador.equipo))
            if len(partidos) == 0:
                continue
            partidas = partidos[0].partida_set.filter(
                Q(jugadores_local=jugador) | Q(jugadores_visitante=jugador)).distinct()
            ganadas = 0
            perdidas = 0
            for p in partidas:
                if p.ganadores.filter(id=jugador.id).count() > 0:
                    ganadas = ganadas +1
                else:
                    perdidas = perdidas +1
            if (ganadas + perdidas) > 0:
                linea.datos.append(DatoGrafico(partidos[0].jornada.numero,
                    ganadas * 100 / (ganadas + perdidas) ))
        self.add_linea(linea)
            
@register.inclusion_tag('dardos/includes/grafico_evolucion.html')
def show_grafico_evolucion(jugador, div_id="chartdiv"):
    grafico_evolucion = GraficoEvolucionGanadas(div_id)
    grafico_evolucion.calcular(jugador)
    return {'grafico_evolucion' : grafico_evolucion}
    
    
