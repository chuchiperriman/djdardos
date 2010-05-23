# -*- mode: python; tab-width: 4; indent-tabs-mode: nil -*-

from djdardos.dardos.models import *
from django.db import models
from django.db.models import Q

class DatosEstadisticaJugadores:
    def __init__(self, equipo = None, peor = False, porcentaje = False):
        self.equipo = equipo
        self.jugadores = []
        self.valor = 0
        self.peor = peor
        self.porcentaje = porcentaje
    
    def calcular_mejor(self, get_valor):
        self.jugadores = []
        self.valor = 0
        for j in Jugador.objects.filter(equipo=self.equipo):
            valor = get_valor(j)
            if (not self.peor and valor > self.valor) or (self.peor and valor < self.valor):
                self.jugadores = [j]
                self.valor = valor
            elif valor == self.valor:
                self.jugadores.append(j)
        return self
        
    def __unicode__(self):
        val=""
        primero = True
        for j in self.jugadores:
            if not primero:
                val += ", "
            else:
                primero = False
                
            val += j.nombre
        if self.porcentaje:
            return str(self.valor) + "% -> " + val
        else:
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

    def partidos_diferencia(self):
        return self.partidos_ganados() - self.partidos_perdidos()
        
    def partidos_jugados_local(self):
        return Partido.objects.filter(Q(jugado=True) & Q(equipo_local=self.equipo)).count()
        
    def partidos_ganados_local(self):
        return Partido.objects.filter(Q(jugado=True) & Q(equipo_local=self.equipo) & Q(ganador=self.equipo)).count()

    def partidos_perdidos_local(self):
        return Partido.objects.filter(Q(jugado=True) & Q(equipo_local=self.equipo)).exclude(
            Q(ganador=self.equipo) | Q(ganador=None)).count()

    def partidos_empatados_local(self):
        return Partido.objects.filter(Q(jugado=True) & Q(equipo_local=self.equipo) & Q(ganador=None)).count()
        
    def partidos_diferencia_local(self):
        return self.partidos_ganados_local() - self.partidos_perdidos_local()
        
    def partidos_jugados_visitante(self):
        return Partido.objects.filter(Q(jugado=True) & Q(equipo_visitante=self.equipo)).count()
        
    def partidos_ganados_visitante(self):
        return Partido.objects.filter(Q(jugado=True) & Q(equipo_visitante=self.equipo) & Q(ganador=self.equipo)).count()

    def partidos_perdidos_visitante(self):
        return Partido.objects.filter(Q(jugado=True) & Q(equipo_visitante=self.equipo)).exclude(
            Q(ganador=self.equipo) | Q(ganador=None)).count()
    
    def partidos_empatados_visitante(self):
        return Partido.objects.filter(Q(jugado=True) & Q(equipo_visitante=self.equipo) & Q(ganador=None)).count()

    def partidos_diferencia_visitante(self):
        return self.partidos_ganados_visitante() - self.partidos_perdidos_visitante()
    
    def puntos_local(self):
        return self.partidos_ganados_local() * 3 + self.partidos_empatados_local()
        
    def puntos_visitante(self):
        return self.partidos_ganados_visitante() * 3 + self.partidos_empatados_visitante()
        
    def puntos(self):
        return self.partidos_ganados() * 3 + self.partidos_empatados()
    
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
        datos = DatosEstadisticaJugadores(self.equipo)
        return datos.calcular_mejor(lambda j: j.partidas_ganadas())
        
    def datos_mas_ganadas_ind(self):
        datos = DatosEstadisticaJugadores(self.equipo)
        return datos.calcular_mejor(lambda j: j.partidas_ind_ganadas())
    
    def datos_mas_ganadas_par(self):
        datos = DatosEstadisticaJugadores(self.equipo)
        return datos.calcular_mejor(lambda j: j.partidas_par_ganadas())
        
    def datos_mas_perdidas(self):
        datos = DatosEstadisticaJugadores(self.equipo)
        return datos.calcular_mejor(lambda j: j.partidas_perdidas())
        
    def datos_mas_perdidas_ind(self):
        datos = DatosEstadisticaJugadores(self.equipo)
        return datos.calcular_mejor(lambda j: j.partidas_ind_perdidas())
    
    def datos_mas_perdidas_par(self):
        datos = DatosEstadisticaJugadores(self.equipo)
        return datos.calcular_mejor(lambda j: j.partidas_par_perdidas())
    
    def datos_mejor_diferencia_ind(self):
        datos = DatosEstadisticaJugadores(self.equipo)
        return datos.calcular_mejor(lambda j: j.partidas_ind_ganadas () - j.partidas_ind_perdidas())
        
    def datos_mejor_diferencia_par(self):
        datos = DatosEstadisticaJugadores(self.equipo)
        return datos.calcular_mejor(lambda j: j.partidas_par_ganadas () - j.partidas_par_perdidas())
        
    def datos_mejor_diferencia(self):
        datos = DatosEstadisticaJugadores(self.equipo)
        return datos.calcular_mejor(lambda j: j.partidas_ganadas () - j.partidas_perdidas())
        
    def datos_peor_diferencia_ind(self):
        datos = DatosEstadisticaJugadores(self.equipo, True)
        return datos.calcular_mejor(lambda j: j.partidas_ind_ganadas () - j.partidas_ind_perdidas())
        
    def datos_peor_diferencia_par(self):
        datos = DatosEstadisticaJugadores(self.equipo, True)
        return datos.calcular_mejor(lambda j: j.partidas_par_ganadas () - j.partidas_par_perdidas())
        
    def datos_peor_diferencia(self):
        datos = DatosEstadisticaJugadores(self.equipo, True)
        return datos.calcular_mejor(lambda j: j.partidas_ganadas () - j.partidas_perdidas())
        
    def datos_mejor_porcentaje_ind(self):
        def calc(j):
            if j.partidas_ind() == 0:
                return 0
            return j.partidas_ind_ganadas () * 100 / j.partidas_ind()
            
        datos = DatosEstadisticaJugadores(self.equipo, porcentaje=True)
        return datos.calcular_mejor(calc)
    
    def datos_mejor_porcentaje_par(self):
        def calc(j):
            if j.partidas_par() == 0:
                return 0
            return j.partidas_par_ganadas () * 100 / j.partidas_par()
            
        datos = DatosEstadisticaJugadores(self.equipo, porcentaje=True)
        return datos.calcular_mejor(calc)
        
    def datos_mejor_porcentaje(self):
        def calc(j):
            if j.partidas() == 0:
                return 0
            return j.partidas_ganadas () * 100 / j.partidas()
            
        datos = DatosEstadisticaJugadores(self.equipo, porcentaje=True)
        return datos.calcular_mejor(calc)
        
    def datos_mayor_porcentaje_perdidas_ind(self):
        def calc(j):
            if j.partidas_ind() == 0:
                return 0
            return j.partidas_ind_perdidas () * 100 / j.partidas_ind()
            
        datos = DatosEstadisticaJugadores(self.equipo, porcentaje=True)
        return datos.calcular_mejor(calc)
    
    def datos_mayor_porcentaje_perdidas_par(self):
        def calc(j):
            if j.partidas_par() == 0:
                return 0
            return j.partidas_par_perdidas () * 100 / j.partidas_par()
            
        datos = DatosEstadisticaJugadores(self.equipo, porcentaje=True)
        return datos.calcular_mejor(calc)
        
    def datos_mayor_porcentaje_perdidas(self):
        def calc(j):
            if j.partidas() == 0:
                return 0
            return j.partidas_perdidas () * 100 / j.partidas()
            
        datos = DatosEstadisticaJugadores(self.equipo, porcentaje=True)
        return datos.calcular_mejor(calc)
    
