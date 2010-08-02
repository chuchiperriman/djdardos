# -*- mode: python; tab-width: 4; indent-tabs-mode: nil -*-
# -*- coding: utf-8 -*-

from ..models import *

TIPO_CALCULO_GANADAS = 1
TIPO_CALCULO_PERDIDAS = 2
TIPO_CALCULO_POR_GANADAS = 3

class GraficaJornadas:
    def __init__(self, liga):
        self.liga = liga
        self.equipo = None
        self.jugador = None
        self.tipo_partida = 0
        self.tipo_juego = 0
        self.tipo_valor = TIPO_CALCULO_GANADAS
        
    def set_jugador(self, jugador):
        self.jugador = jugador
        self.equipo = jugador.equipo
        
    def set_equipo(self, equipo):
        self.jugador = None
        self.equipo = jugador.equipo
        
    def apply_filtro_tipo_partida(self, partidas):
        if self.tipo_partida > 0:
            return partidas.filter(tipo=self.tipo_partida)
    
    def apply_filtro_tipo_juego(self, partidas):
        if self.tipo_juego > 0:
            return partidas.filter(tipo_juego=self.tipo_juego)

    def calcular_valor(self, partidas):
        ganadas = 0
        perdidas = 0
        valor = 0
        for p in partidas:
            #TODO Aquí hay que filtrar por jugador o equipo según gráfica
            if p.ganadores.filter(id=self.jugador.id).count() > 0:
                ganadas = ganadas + 1
            else:
                perdidas = perdidas + 1

        if self.tipo_valor == TIPO_CALCULO_GANADAS:
            valor = ganadas
        elif self.tipo_valor == TIPO_CALCULO_PERDIDAS:
            valor = perdidas
        elif self.tipo_valor == TIPO_CALCULO_POR_GANADAS:
            if (ganadas + perdidas) > 0:
                valor = ganadas * 100 / (ganadas + perdidas)
        return valor        
                
    def calcular(self):
        res = list()
        jornadas = self.liga.jornada_set.all()
        for jor in jornadas:
            partidos = jor.partido_set.filter(
                Q(equipo_local=self.equipo) | Q(equipo_visitante=self.equipo))
            if len(partidos) == 0:
                continue
                
            if self.jugador:
                partidas = partidos[0].partida_set.filter(
                    Q(jugadores_local=self.jugador) | Q(jugadores_visitante=self.jugador))
            if self.tipo_partida > 0:
                partidas = self.apply_filtro_tipo_partida(partidas)
            if self.tipo_juego > 0:
                partidas = self.apply_filtro_tipo_juego(partidas)
            
            valor = self.calcular_valor(partidas.distinct())
            res.append([jor, valor])
        return res
