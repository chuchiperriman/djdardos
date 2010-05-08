# -*- mode: python; tab-width: 4; indent-tabs-mode: nil -*-

from djdardos.dardos.models import *
from django.db import models
from django.db.models import Q

class DatosEstadisticaJugadores:
    def __init__(self):
        self.jugadores = []
        self.valor = 0
        
    def __unicode__(self):
        val=""
        primero = True
        for j in self.jugadores:
            if not primero:
                val += ", "
            else:
                primero = False
                
            val += j.nombre
        return str(self.valor) + " -> " + val

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
    
    def __controlar_jugador_mejor(self, datos, jugador, valor):
        if valor > datos.valor:
            datos.jugadores = [jugador]
            datos.valor = valor
        elif valor == datos.valor:
            datos.jugadores.append(jugador)
            
    def __controlar_jugador_peor(self, datos, jugador, valor):
        if valor < datos.valor:
            datos.jugadores = [jugador]
            datos.valor = valor
        elif valor == datos.valor:
            datos.jugadores.append(jugador)
            
    def datos_mas_ganadas(self):
        datos = DatosEstadisticaJugadores()
        for j in Jugador.objects.filter(equipo=self.equipo):
            self.__controlar_jugador_mejor(datos, j, j.partidas_ganadas())
        return datos
        
    def datos_mas_ganadas_ind(self):
        datos = DatosEstadisticaJugadores()
        for j in Jugador.objects.filter(equipo=self.equipo):
            self.__controlar_jugador_mejor(datos, j, j.partidas_ind_ganadas())
        return datos
    
    def datos_mas_ganadas_par(self):
        datos = DatosEstadisticaJugadores()
        for j in Jugador.objects.filter(equipo=self.equipo):
            self.__controlar_jugador_mejor(datos, j, j.partidas_par_ganadas())
        return datos
        
    def datos_mas_perdidas(self):
        datos = DatosEstadisticaJugadores()
        for j in Jugador.objects.filter(equipo=self.equipo):
            self.__controlar_jugador_mejor(datos, j, j.partidas_perdidas())
        return datos
        
    def datos_mas_perdidas_ind(self):
        datos = DatosEstadisticaJugadores()
        for j in Jugador.objects.filter(equipo=self.equipo):
            self.__controlar_jugador_mejor(datos, j, j.partidas_ind_perdidas())
        return datos
    
    def datos_mas_perdidas_par(self):
        datos = DatosEstadisticaJugadores()
        for j in Jugador.objects.filter(equipo=self.equipo):
            self.__controlar_jugador_mejor(datos, j, j.partidas_par_perdidas())
        return datos
    
    def datos_mejor_media_ind(self):
        datos = DatosEstadisticaJugadores()
        for j in Jugador.objects.filter(equipo=self.equipo):
            self.__controlar_jugador_mejor(datos, j, 
                    j.partidas_ind_ganadas () - j.partidas_ind_perdidas())
        return datos
        
    def datos_mejor_media_par(self):
        datos = DatosEstadisticaJugadores()
        for j in Jugador.objects.filter(equipo=self.equipo):
            self.__controlar_jugador_mejor(datos, j, 
                    j.partidas_par_ganadas () - j.partidas_par_perdidas())
        return datos
        
    def datos_mejor_media(self):
        datos = DatosEstadisticaJugadores()
        for j in Jugador.objects.filter(equipo=self.equipo):
            self.__controlar_jugador_mejor(datos, j, 
                    j.partidas_ganadas () - j.partidas_perdidas())
        return datos
        
    def datos_peor_media_ind(self):
        datos = DatosEstadisticaJugadores()
        for j in Jugador.objects.filter(equipo=self.equipo):
            self.__controlar_jugador_peor(datos, j, 
                    j.partidas_ind_ganadas () - j.partidas_ind_perdidas())
        return datos
        
    def datos_peor_media_par(self):
        datos = DatosEstadisticaJugadores()
        for j in Jugador.objects.filter(equipo=self.equipo):
            self.__controlar_jugador_peor(datos, j, 
                    j.partidas_par_ganadas () - j.partidas_par_perdidas())
        return datos
        
    def datos_peor_media(self):
        datos = DatosEstadisticaJugadores()
        for j in Jugador.objects.filter(equipo=self.equipo):
            self.__controlar_jugador_peor(datos, j, 
                    j.partidas_ganadas () - j.partidas_perdidas())
        return datos
        
