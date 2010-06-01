# -*- mode: python; tab-width: 4; indent-tabs-mode: nil -*-

from django.db import models
from django.db.models import Q

TIPOS_PARTIDA = (
    ("1" , "501"),
    ("2" , "Cricket")
)

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
    fecha_prevista = models.DateField('Fecha prevista')
    
    def __unicode__(self):
        return str(self.numero)

class Equipo(models.Model):
    ligas = models.ManyToManyField(Liga)
    nombre = models.CharField(max_length=20)
    campo = models.CharField(max_length=100)
    email = models.EmailField(null=True, blank=True)
    direccion = models.CharField(max_length=255,null=True, blank=True)
    path_foto = models.CharField(max_length=255,null=True, blank=True)
    telefono = models.CharField(max_length=20, null=True, blank=True)
    google_maps = models.TextField(null=True, blank=True)

    def __unicode__(self):
        return self.nombre
    

class Jugador(models.Model):
    equipo = models.ForeignKey(Equipo)
    nombre = models.CharField(max_length=100)
    fecha_alta = models.DateTimeField('Fecha de Alta')
    path_foto = models.CharField(max_length=255,null=True, blank=True)
    email = models.EmailField(null=True, blank=True)

    def __unicode__(self):
        return self.nombre

    def partidas(self):
        return self.partidas_ind() + self.partidas_par()
            
    def partidas_ind(self):
        return PartidaIndividual.objects \
            .filter(Q(jugador_local=self) | Q(jugador_visitante=self)) \
            .count()
            
    def partidas_par(self):
        return PartidaParejas.objects \
            .filter(Q(jugador_local1=self) | Q(jugador_local2=self) \
                | Q(jugador_visitante1=self) | Q(jugador_visitante2=self)) \
            .count()

    def partidas_ganadas(self):
        return self.partidas_ind_ganadas() + self.partidas_par_ganadas()
    
    def partidas_perdidas(self):
        return self.partidas_ind_perdidas() + self.partidas_par_perdidas()
        
    def partidas_ind_ganadas(self):
        return PartidaIndividual.objects.filter(ganador=self).count()
        
    def partidas_par_ganadas(self):
        return PartidaParejas.objects.filter(Q(ganador1=self) | Q(ganador2=self)).count()
        
    def partidas_ind_perdidas(self):
        return PartidaIndividual.objects \
            .filter(Q(jugador_local=self) | Q(jugador_visitante=self)) \
            .exclude(ganador=self) \
            .count()
            
    def partidas_par_perdidas(self):
        return PartidaParejas.objects \
            .filter(Q(jugador_local1=self) | Q(jugador_local2=self) \
                | Q(jugador_visitante1=self) | Q(jugador_visitante2=self)) \
            .exclude(Q(ganador1=self) | Q(ganador2=self)) \
            .count()
            
    def partidas_diferencia(self):
        return self.partidas_ganadas() - self.partidas_perdidas()
    def partidas_ind_diferencia(self):
        return self.partidas_ind_ganadas() - self.partidas_ind_perdidas()
    def partidas_par_diferencia(self):
        return self.partidas_par_ganadas() - self.partidas_par_perdidas()
        
class Partido(models.Model):
    jornada = models.ForeignKey(Jornada)
    equipo_local = models.ForeignKey(Equipo, related_name="equipo_local")
    equipo_visitante = models.ForeignKey(Equipo, related_name="equipo_visitante")
    ganador = models.ForeignKey(Equipo, related_name="ganador", null=True, blank=True)
    fecha = models.DateTimeField()
    jugado = models.BooleanField()
    
    def puntos_local(self):
        jugadores = self.equipo_local.jugador_set.all()
        puntos = self.partidaindividual_set.filter(ganador__in=jugadores).count()
        puntos += self.partidaparejas_set.filter(Q(ganador1__in=jugadores) | Q(ganador2__in=jugadores)).count()
        return puntos
    
    def puntos_visitante(self):
        jugadores = self.equipo_visitante.jugador_set.all()
        puntos = self.partidaindividual_set.filter(ganador__in=jugadores).count()
        puntos += self.partidaparejas_set.filter(Q(ganador1__in=jugadores) | Q(ganador2__in=jugadores)).count()
        return puntos
    
    def __unicode__(self):
        return self.equipo_local.nombre + "-" + self.equipo_visitante.nombre + " " + str(self.fecha)

class PartidaIndividual(models.Model):
    numero = models.IntegerField()
    partido = models.ForeignKey(Partido)
    tipo = models.CharField(max_length=1, choices=TIPOS_PARTIDA)
    jugador_local = models.ForeignKey(Jugador, related_name="jugador_local")
    jugador_visitante = models.ForeignKey(Jugador, related_name="jugador_visitante")
    ganador = models.ForeignKey(Jugador, related_name="ganador")
    
    def __unicode__(self):
        return str(self.partido) + " - " + str(self.numero)
    
class PartidaParejas(models.Model):
    numero = models.IntegerField()
    partido = models.ForeignKey(Partido)
    tipo = models.CharField(max_length=1, choices=TIPOS_PARTIDA)
    jugador_local1 = models.ForeignKey(Jugador, related_name="jugador_local1")
    jugador_local2 = models.ForeignKey(Jugador, related_name="jugador_local2")
    jugador_visitante1 = models.ForeignKey(Jugador, related_name="jugador_visitante1")
    jugador_visitante2 = models.ForeignKey(Jugador, related_name="jugador_visitante2")
    ganador1 = models.ForeignKey(Jugador, related_name="ganador1")
    ganador2 = models.ForeignKey(Jugador, related_name="ganador2")
    
    def __unicode__(self):
        return str(self.partido) + " - " + str(self.numero)
    
    
    
