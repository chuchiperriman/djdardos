# -*- mode: python; tab-width: 4; indent-tabs-mode: nil -*-

from itertools import chain

from django.db import models
from django.db.models import Q

TIPO_PARTIDA_INDIVIDUAL = 1
TIPO_PARTIDA_PAREJAS = 2

TIPO_JUEGO_501 = 1
TIPO_JUEGO_CRICKET = 2

TIPOS_PARTIDA = (
    (TIPO_PARTIDA_INDIVIDUAL , "Individual"),
    (TIPO_PARTIDA_PAREJAS , "Parejas")
)

TIPOS_JUEGO = (
    (TIPO_JUEGO_501 , "501"),
    (TIPO_JUEGO_CRICKET , "Cricket")
)

class Division(models.Model):
    nombre = models.CharField(max_length=100)
    
    def get_liga_actual(self):
        return self.liga_set.get(actual=True)
        
    def __unicode__(self):
        return self.nombre
    
class Liga(models.Model):
    division = models.ForeignKey(Division)
    nombre = models.CharField(max_length=100)
    actual = models.BooleanField(default=False)

    def __unicode__(self):
        return self.nombre

class Jornada(models.Model):
    liga = models.ForeignKey(Liga)
    numero = models.IntegerField()
    fecha_prevista = models.DateField('Fecha prevista')
    
    def __unicode__(self):
        return self.liga.nombre + ": " + str(self.numero)

class Equipo(models.Model):
    ligas = models.ManyToManyField(Liga)
    nombre = models.CharField(max_length=20)
    campo = models.CharField(max_length=100)
    email = models.EmailField(null=True, blank=True)
    direccion = models.CharField(max_length=255,null=True, blank=True)
    path_foto = models.CharField(max_length=255,null=True, blank=True)
    telefono = models.CharField(max_length=20, null=True, blank=True)
    google_maps = models.TextField(null=True, blank=True)

    def get_liga_actual(self):
        for l in self.ligas.all():
            if l.actual:
                return l
        return None
    
    def __unicode__(self):
        return self.nombre
    

class Jugador(models.Model):
    equipo = models.ForeignKey(Equipo)
    nombre = models.CharField(max_length=100)
    fecha_alta = models.DateTimeField('Fecha de Alta')
    path_foto = models.CharField(max_length=255,null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    
    filters = None
    
    def partidas(self):
        #partidos = Partido.objects.filter(jornada__liga__exact = self.equipo.get_liga_actual()).distinct()
        if self.filters:
            return Partida.objects.filter(self.filters).filter(Q(jugadores_local = self) | Q(jugadores_visitante = self)).distinct()
        else:
            return Partida.objects.filter(Q(jugadores_local = self) | Q(jugadores_visitante = self)).distinct()
    
    def partidas_ind(self):
        return self.partidas().filter(tipo=TIPO_PARTIDA_INDIVIDUAL)
        
    def partidas_par(self):
        return self.partidas().filter(tipo=TIPO_PARTIDA_PAREJAS)
    
    def partidas_ganadas(self):
        return self.partidas().filter(ganadores=self)
    
    def partidas_ind_ganadas(self):
        return self.partidas_ind().filter(ganadores=self)
        
    def partidas_par_ganadas(self):
        return self.partidas_par().filter(ganadores=self)
    
    def partidas_perdidas(self):
        return self.partidas().exclude(ganadores=self)
    
    def partidas_ind_perdidas(self):
        return self.partidas_ind().exclude(ganadores=self)
        
    def partidas_par_perdidas(self):
        return self.partidas_par().exclude(ganadores=self)
        
    def __unicode__(self):
        return self.nombre

class Partido(models.Model):
    jornada = models.ForeignKey(Jornada)
    equipo_local = models.ForeignKey(Equipo, related_name="equipo_local")
    equipo_visitante = models.ForeignKey(Equipo, related_name="equipo_visitante")
    ganador = models.ForeignKey(Equipo, related_name="ganador", null=True, blank=True)
    fecha = models.DateTimeField()
    jugado = models.BooleanField()
    puntos_local = models.PositiveSmallIntegerField(default = 0)
    puntos_visitante = models.PositiveSmallIntegerField(default = 0)
    
    def __unicode__(self):
        return "Jornada " + str(self.jornada.numero) + ": " + self.equipo_local.nombre + "-" + self.equipo_visitante.nombre + " " + str(self.fecha)

class Partida(models.Model):
    numero = models.IntegerField()
    partido = models.ForeignKey(Partido)
    tipo = models.CharField(max_length=1, choices=TIPOS_PARTIDA)
    tipo_juego = models.CharField(max_length=1, choices=TIPOS_JUEGO)
    jugadores_local = models.ManyToManyField(Jugador, related_name="jugadores_local")
    jugadores_visitante = models.ManyToManyField(Jugador, related_name="jugadores_visitante")
    ganadores = models.ManyToManyField(Jugador, related_name="ganadores")
    
    #Funciones de utilidad para partidas individuales
    def jugador_local(self):
        return self.jugadores_local.all()[0]
        
    def jugador_visitante(self):
        return self.jugadores_visitante.all()[0]
    
    def ganador(self):
        return self.ganadores.all()[0]
        
    #Funciones de utilidad para partidas de parejas
    def jugador_local1(self):
        return self.jugadores_local.all()[0]
        
    def jugador_visitante1(self):
        return self.jugadores_visitante.all()[0]
    
    def ganador1(self):
        return self.ganadores.all()[0]
        
    def jugador_local2(self):
        return self.jugadores_local.all()[1]
        
    def jugador_visitante2(self):
        return self.jugadores_visitante.all()[1]
    
    def ganador2(self):
        return self.ganadores.all()[1]
        
    def __unicode__(self):
        return str(self.partido) + " - " + str(self.numero)
    
    
