# -*- mode: python; tab-width: 4; indent-tabs-mode: nil -*-
# -*- coding: utf-8 -*-

from djdardos.dardos.models import *

from django import template

register = template.Library()

class DatoLineaSimple:
    def __init__(self, x, y):
        self.x = x
        self.y = y

class DatosJornadaGP:
    def __init__(self, num_jornada, ganados, perdidos):
        self.num_jornada = num_jornada
        self.ganados = ganados
        self.perdidos = perdidos

class JornadasGrafico:
    def __init__(self,titulo, div_id="chartdiv", max_partidas = 16,
        max_jornadas = 15):
        self.titulo = titulo
        self.div_id = div_id
        self.max_partidas = max_partidas
        self.max_jornadas = max_jornadas
        self.datos = list()
    
    def get_max_x_range(self):
        return range(self.max_jornadas + 2)
        
    def get_max_y_range(self):
        if self.max_partidas <= 6:
            return range(self.max_partidas + 1)
        else:
            return range(0, self.max_partidas + 1, 2)
            
    def add_dato (self, num_jornada, ganados, perdidos):
        self.datos.append(DatosJornadaGP(num_jornada, ganados, perdidos))
        
class GraficoEvolucion:
    def __init__(self, titulo, div_id="chartdiv", label="Partidas"):
        self.titulo = titulo
        self.div_id = div_id
        self.datos = list()
        self.label = label
        
    def get_max_x_range(self):
        return range (0,17)
        
    def get_max_y_range(self):
        return range (0,7)
    
    def calcular(self, jugador):
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
            
            self.datos.append(DatoLineaSimple(partidos[0].jornada.numero,ganadas))

@register.inclusion_tag('dardos/includes/grafico_gp_jornadas.html')
def show_grafico_gp_jornadas(jornadas_grafico):
    return {'jornadas_grafico' : jornadas_grafico}
@register.inclusion_tag('dardos/includes/grafico_evolucion.html')

def show_grafico_evolucion(jugador, div_id="chartdiv"):
    grafico_evolucion = GraficoEvolucion("Gráfico de evolución",div_id)
    grafico_evolucion.calcular(jugador)
    return {'grafico_evolucion' : grafico_evolucion}
    
