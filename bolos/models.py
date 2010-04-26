# -*- mode: python; tab-width: 4; indent-tabs-mode: nil -*-

from django.db import models

class Division(models.Model):
    nombre = models.CharField(max_length=100)
    
    def __unicode__(self):
        return self.nombre
    
class Liga(models.Model):
    division = models.ForeignKey(Division)
    nombre = models.CharField(max_length=100)

    def __unicode__(self):
        return self.nombre

class Jornada(models.Model):
    liga = models.ForeignKey(Liga)
    numero = models.IntegerField()

class Equipo(models.Model):
    ligas = models.ManyToManyField(Liga)
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
    jornada = models.ForeignKey(Jornada)
    equipo_local = models.ForeignKey(Equipo, related_name="equipo_local")
    equipo_visitante = models.ForeignKey(Equipo, related_name="equipo_visitante")
    ganador = models.ForeignKey(Equipo, related_name="ganador")
    fecha = models.DateTimeField()

class PartidaIndividual(models.Model):
    partido = models.ForeignKey(Partido)
    tipo = models.IntegerField()
    jugador_local = models.ForeignKey(Jugador, related_name="jugador_local")
    jugador_visitante = models.ForeignKey(Jugador, related_name="jugador_visitante")
    ganador = models.ForeignKey(Jugador, related_name="ganador")
    
class PartidaParejas(models.Model):
    partido = models.ForeignKey(Partido)
    tipo = models.IntegerField()
    jugador_local1 = models.ForeignKey(Jugador, related_name="jugador_local1")
    jugador_local2 = models.ForeignKey(Jugador, related_name="jugador_local2")
    jugador_visitante1 = models.ForeignKey(Jugador, related_name="jugador_visitante1")
    jugador_visitante2 = models.ForeignKey(Jugador, related_name="jugador_visitante2")
    ganador1 = models.ForeignKey(Jugador, related_name="ganador1")
    ganador2 = models.ForeignKey(Jugador, related_name="ganador2")
    
    
    
    
