# -*- mode: python; tab-width: 4; indent-tabs-mode: nil -*-
from datetime import datetime
from djdardos.dardos.models import *
from django.db import models
from django.db.models import Q

class DatosEstadisticaJugador:
    def __init__(self, jugador, partidos = None):
        self.jugador = jugador
        self.nombre = jugador.nombre
        self.id = jugador.id
        j = jugador
        if partidos:
            j.filters = Q(partido__in=partidos)
        self.partidas_ind = j.partidas_ind().count()
        self.partidas_par = j.partidas_par().count()
        self.partidas = self.partidas_ind + self.partidas_par
        self.partidas_ind_ganadas = j.partidas_ind_ganadas().count()
        self.partidas_par_ganadas = j.partidas_par_ganadas().count()
        self.partidas_ganadas = self.partidas_ind_ganadas + self.partidas_par_ganadas
        self.partidas_ind_perdidas = j.partidas_ind_perdidas().count()
        self.partidas_par_perdidas = j.partidas_par_perdidas().count()
        self.partidas_perdidas = self.partidas_ind_perdidas + self.partidas_par_perdidas
        self.partidas_ind_diferencia = self.partidas_ind_ganadas - self.partidas_ind_perdidas
        self.partidas_par_diferencia = self.partidas_par_ganadas - self.partidas_par_perdidas
        self.partidas_diferencia = self.partidas_ganadas - self.partidas_perdidas
        if self.partidas_ind > 0:
            self.partidas_ind_ganadas_por = self.partidas_ind_ganadas * 100 / self.partidas_ind
        else:
            self.partidas_ind_ganadas_por = 0
        if self.partidas_par > 0:
            self.partidas_par_ganadas_por = self.partidas_par_ganadas * 100 / self.partidas_par
        else:
            self.partidas_par_ganadas_por = 0
        if self.partidas > 0:
            self.partidas_ganadas_por = self.partidas_ganadas * 100 / self.partidas
        else:
            self.partidas_ganadas_por = 0
            
        self.partidas_par_cricket = j.partidas_par()\
            .filter(tipo_juego=TIPO_JUEGO_CRICKET).count()
        self.partidas_par_ganadas_cricket = j.partidas_par_ganadas()\
            .filter(tipo_juego=TIPO_JUEGO_CRICKET).count()
        self.partidas_par_perdidas_cricket = j.partidas_par_perdidas()\
            .filter(tipo_juego=TIPO_JUEGO_CRICKET).count()
        if self.partidas_par_cricket > 0:
            self.partidas_par_ganadas_cricket_por = \
                self.partidas_par_ganadas_cricket * 100 / self.partidas_par_cricket
        self.partidas_par_cricket_dif = self.partidas_par_ganadas_cricket - self.partidas_par_perdidas_cricket
        
class DatosEstadisticaJugadores:
    def __init__(self, equipo, liga = None):
        self.equipo = equipo
        self.jugadores = []
        self.valor = 0
        self.peor = False
        self.porcentaje = False
        #Preload the query
        self.jugadores_list = list()
        if liga:
            partidos = Partido.objects.filter(jornada__liga__exact = liga).distinct()
        for j in Jugador.objects.filter(equipo=self.equipo):
            self.jugadores_list.append(DatosEstadisticaJugador(j, partidos))
    
    def calcular_mejor(self, get_valor):
        self.jugadores = []
        primero = True
        self.valor = -26082004
        
        for j in self.jugadores_list:
            valor = get_valor(j)
            if primero:
                primero = False
                self.jugadores = [j]
                self.valor = valor
            elif (not self.peor and valor > self.valor) or (self.peor and valor < self.valor):
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
    def __init__(self, equipo, liga, cargar_jugadores = True):
        print 'ini', datetime.now()
        self.liga = liga
        self.equipo = equipo
        if cargar_jugadores:
            self.dej = DatosEstadisticaJugadores(self.equipo, self.liga)
            self.jugadores = self.dej.jugadores_list
        
        jornadas_liga = Jornada.objects.filter(liga=liga)
        self.partidos_jugados_count = Partido.objects.filter(
            Q(jornada__in=jornadas_liga) & Q(jugado=True) & (Q(equipo_local=self.equipo) | Q(equipo_visitante=self.equipo))).count()
        self.partidos_ganados_count = Partido.objects.filter(
            Q(jornada__in=jornadas_liga) & Q(jugado=True) & Q(ganador=self.equipo)).count()
        self.partidos_perdidos_count = Partido.objects.filter(
            Q(jornada__in=jornadas_liga) & Q(jugado=True) & (Q(equipo_local=self.equipo) | 
            Q(equipo_visitante=self.equipo))).exclude(
                Q(ganador=self.equipo) | Q(ganador=None)).count()
        self.partidos_empatados_count = Partido.objects.filter(Q(jugado=True) & Q(ganador=None) & 
            Q(jornada__in=jornadas_liga) & (Q(equipo_local=self.equipo) | Q(equipo_visitante=self.equipo))).count() 
        self.partidos_ganados_local_count = Partido.objects.filter(
            Q(jornada__in=jornadas_liga) & Q(jugado=True) & Q(equipo_local=self.equipo) & Q(ganador=self.equipo)).count()
        self.partidos_perdidos_local_count = Partido.objects.filter(
            Q(jornada__in=jornadas_liga) & Q(jugado=True) & Q(equipo_local=self.equipo)).exclude(
            Q(ganador=self.equipo) | Q(ganador=None)).count()
        self.partidos_empatados_local_count = Partido.objects.filter(
            Q(jornada__in=jornadas_liga) & Q(jugado=True) & Q(equipo_local=self.equipo) & Q(ganador=None)).count()
        self.partidos_ganados_visitante_count = Partido.objects.filter(
            Q(jornada__in=jornadas_liga) & Q(jugado=True) & Q(equipo_visitante=self.equipo) & Q(ganador=self.equipo)).count()
        self.partidos_perdidos_visitante_count= Partido.objects.filter(
            Q(jornada__in=jornadas_liga) & Q(jugado=True) & Q(equipo_visitante=self.equipo)).exclude(
            Q(ganador=self.equipo) | Q(ganador=None)).count()
        self.partidos_empatados_visitante_count = Partido.objects.filter(
            Q(jornada__in=jornadas_liga) & Q(jugado=True) & Q(equipo_visitante=self.equipo) & Q(ganador=None)).count()
        
        print 'fin', datetime.now()

    def partidos_jugados(self):
        return self.partidos_jugados_count
        
    def partidos_ganados(self):
        return self.partidos_ganados_count

    def partidos_perdidos(self):
        return self.partidos_perdidos_count
    
    def partidos_empatados(self):
        return self.partidos_empatados_count

    def partidos_diferencia(self):
        return self.partidos_ganados() - self.partidos_perdidos()
        
    def partidos_ganados_local(self):
        return self.partidos_ganados_local_count

    def partidos_perdidos_local(self):
        return self.partidos_perdidos_local_count

    def partidos_empatados_local(self):
        return self.partidos_empatados_local_count
    
    def partidos_jugados_local(self):
        return self.partidos_ganados_local_count + \
            self.partidos_perdidos_local_count + self.partidos_empatados_local_count
        
    def partidos_diferencia_local(self):
        return self.partidos_ganados_local() - self.partidos_perdidos_local()
        
    def partidos_ganados_visitante(self):
        return self.partidos_ganados_visitante_count

    def partidos_perdidos_visitante(self):
        return self.partidos_perdidos_visitante_count
    
    def partidos_empatados_visitante(self):
        return self.partidos_empatados_visitante_count
        
    def partidos_jugados_visitante(self):
        return self.partidos_ganados_visitante_count + \
            self.partidos_perdidos_visitante_count + \
            self.partidos_empatados_visitante_count

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
        self.dej.peor = False
        self.dej.porcentaje = False
        return self.dej.calcular_mejor(lambda j: j.partidas_ganadas)
        
    def datos_mas_ganadas_ind(self):
        self.dej.peor = False
        self.dej.porcentaje = False
        return self.dej.calcular_mejor(lambda j: j.partidas_ind_ganadas)
    
    def datos_mas_ganadas_par(self):
        self.dej.peor = False
        self.dej.porcentaje = False
        return self.dej.calcular_mejor(lambda j: j.partidas_par_ganadas)
        
    def datos_mas_perdidas(self):
        self.dej.peor = False
        self.dej.porcentaje = False
        return self.dej.calcular_mejor(lambda j: j.partidas_perdidas)
        
    def datos_mas_perdidas_ind(self):
        self.dej.peor = False
        self.dej.porcentaje = False
        return self.dej.calcular_mejor(lambda j: j.partidas_ind_perdidas)
    
    def datos_mas_perdidas_par(self):
        self.dej.peor = False
        self.dej.porcentaje = False
        return self.dej.calcular_mejor(lambda j: j.partidas_par_perdidas)
    
    def datos_mejor_diferencia_ind(self):
        self.dej.peor = False
        self.dej.porcentaje = False
        return self.dej.calcular_mejor(lambda j: j.partidas_ind_ganadas - j.partidas_ind_perdidas)
        
    def datos_mejor_diferencia_par(self):
        self.dej.peor = False
        self.dej.porcentaje = False
        res = self.dej.calcular_mejor(lambda j: j.partidas_par_ganadas - j.partidas_par_perdidas)
        return res
        
    def datos_mejor_diferencia(self):
        self.dej.peor = False
        self.dej.porcentaje = False
        return self.dej.calcular_mejor(lambda j: j.partidas_ganadas - j.partidas_perdidas)
        
    def datos_peor_diferencia_ind(self):
        self.dej.peor = True
        self.dej.porcentaje = False
        return self.dej.calcular_mejor(lambda j: j.partidas_ind_ganadas - j.partidas_ind_perdidas)
        
    def datos_peor_diferencia_par(self):
        self.dej.peor = True
        self.dej.porcentaje = False
        return self.dej.calcular_mejor(lambda j: j.partidas_par_ganadas - j.partidas_par_perdidas)
        
    def datos_peor_diferencia(self):
        self.dej.peor = True
        self.dej.porcentaje = False
        return self.dej.calcular_mejor(lambda j: j.partidas_ganadas - j.partidas_perdidas)
        
    def datos_mejor_porcentaje_ind(self):
        def calc(j):
            if j.partidas_ind == 0:
                return 0
            return j.partidas_ind_ganadas * 100 / j.partidas_ind
            
        self.dej.peor = False
        self.dej.porcentaje = True
        return self.dej.calcular_mejor(calc)
    
    def datos_mejor_porcentaje_par(self):
        def calc(j):
            if j.partidas_par == 0:
                return 0
            return j.partidas_par_ganadas * 100 / j.partidas_par
            
        self.dej.peor = False
        self.dej.porcentaje = True
        return self.dej.calcular_mejor(calc)
        
    def datos_mejor_porcentaje(self):
        def calc(j):
            if j.partidas == 0:
                return 0
            return j.partidas_ganadas * 100 / j.partidas
            
        self.dej.peor = False
        self.dej.porcentaje = True
        return self.dej.calcular_mejor(calc)
        
    def datos_mayor_porcentaje_perdidas_ind(self):
        def calc(j):
            if j.partidas_ind == 0:
                return 0
            return j.partidas_ind_perdidas * 100 / j.partidas_ind
            
        self.dej.peor = False
        self.dej.porcentaje = True
        return self.dej.calcular_mejor(calc)
    
    def datos_mayor_porcentaje_perdidas_par(self):
        def calc(j):
            if j.partidas_par == 0:
                return 0
            return j.partidas_par_perdidas * 100 / j.partidas_par
            
        self.dej.peor = False
        self.dej.porcentaje = True
        return self.dej.calcular_mejor(calc)
        
    def datos_mayor_porcentaje_perdidas(self):
        def calc(j):
            if j.partidas == 0:
                return 0
            return j.partidas_perdidas * 100 / j.partidas
            
        self.dej.peor = False
        self.dej.porcentaje = True
        return self.dej.calcular_mejor(calc)
    
