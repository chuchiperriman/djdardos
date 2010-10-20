# -*- mode: python; tab-width: 4; indent-tabs-mode: nil -*-
# -*- coding: utf-8 -*-

from ..models import *

class GraficaJornadas:
    def __init__(self, liga=None):
        self.liga = liga
        self.equipo = None
        self.jugador = None
        self.tipo_partida = 0
        self.tipo_juego = 0
        self.valores = list()
        
    def set_jugador(self, jugador):
        self.jugador = jugador
        self.equipo = jugador.equipo
        
    def set_equipo(self, equipo):
        self.jugador = None
        self.equipo = equipo
        
    def apply_filtro_tipo_partida(self, partidas):
        if self.tipo_partida > 0:
            return partidas.filter(tipo=self.tipo_partida)
        return partidas
    
    def apply_filtro_tipo_juego(self, partidas):
        if self.tipo_juego > 0:
            return partidas.filter(tipo_juego=self.tipo_juego)
        return partidas
        
    def calcular_valor(self, partidas):
        ganadas = 0
        perdidas = 0
        porcentaje = 0
        for p in partidas:
            #TODO Aquí hay que filtrar por jugador o equipo según gráfica
            if self.jugador:
                if p.ganadores.filter(id=self.jugador.id).count() > 0:
                    ganadas = ganadas + 1
                else:
                    perdidas = perdidas + 1
            else:
                if p.ganadores.filter(equipo=self.equipo).count() > 0:
                    ganadas = ganadas + 1
                else:
                    perdidas = perdidas + 1

        if (ganadas + perdidas) > 0:
            porcentaje = ganadas * 100 / (ganadas + perdidas)
            
        return (ganadas, perdidas, porcentaje)
                
    def calcular(self):
        res = list()
        jornadas = None
        if self.liga:
            jornadas = self.liga.jornada_set.all()
        else:
            jornadas = Jornada.objects.all()
            
        for jor in jornadas:
            partidos = jor.partido_set.filter(
                Q(equipo_local=self.equipo) | Q(equipo_visitante=self.equipo))
            if len(partidos) == 0:
                continue
                
            if self.jugador:
                partidas = partidos[0].partida_set.filter(
                    Q(jugadores_local=self.jugador) | Q(jugadores_visitante=self.jugador))
            else:
                partidas = partidos[0].partida_set.all()

            partidas = self.apply_filtro_tipo_partida(partidas)
            partidas = self.apply_filtro_tipo_juego(partidas)
            
            ganadas, perdidas, porcentaje = self.calcular_valor(partidas.distinct())
            if ganadas != 0 or perdidas != 0:
                res.append({
                    "jornada" : jor,
                    "ganadas" : ganadas,
                    "perdidas" : perdidas,
                    "porcentaje" : porcentaje
                })
        self.valores = res
        return res
        
        
        
