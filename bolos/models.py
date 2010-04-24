# -*- mode: python; tab-width: 4; indent-tabs-mode: nil -*-

from django.db import models

class Liga(models.Model):
    nombre = models.CharField(max_length=100)

class Equipo(models.Model):
    liga = models.ForeignKey(Liga)
    nombre = models.CharField(max_length=20)
    
    def __unicode__(self):
        return self.nombre


class Jugador(models.Model):
    equipo = models.ForeignKey(Equipo)
    nombre = models.CharField(max_length=100)
    fecha_alta = models.DateTimeField('Fecha de Alta')

    def __unicode__(self):
        return self.nombre

class Partido(models.Model):
    equipo_local = models.ForeignKey(Equipo, related_name="equipo_local")
    equipo_visitante = models.ForeignKey(Equipo, related_name="equipo_visitante")
    fecha = models.DateTimeField()

class TipoPartida(models.Model):
    nombre = models.CharField(max_length="20")
    def __unicode__(self):
        return self.nombre
    
class PartidaSimple(models.Model):
    partido = models.ForeignKey(Partido)
    tipo = models.ForeignKey(TipoPartida)
    jugador_local = models.ForeignKey(Jugador, related_name="jugador_local")
    jugador_visitante = models.ForeignKey(Jugador, related_name="jugador_visitante")
    ganador = models.ForeignKey(Jugador, related_name="ganador")
    
class PartidaDobles(models.Model):
    partido = models.ForeignKey(Partido)
    tipo = models.ForeignKey(TipoPartida)
    jugador_local1 = models.ForeignKey(Jugador, related_name="jugador_local1")
    jugador_local2 = models.ForeignKey(Jugador, related_name="jugador_local2")
    jugador_visitante1 = models.ForeignKey(Jugador, related_name="jugador_visitante1")
    jugador_visitante2 = models.ForeignKey(Jugador, related_name="jugador_visitante2")
    ganador1 = models.ForeignKey(Jugador, related_name="ganador1")
    ganador2 = models.ForeignKey(Jugador, related_name="ganador2")
    
    
    
    
