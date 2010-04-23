# -*- mode: python; tab-width: 4; indent-tabs-mode: nil -*-

from django.db import models

class Equipo(models.Model):
    nombre = models.CharField(max_length=20)
    
    def __unicode__(self):
        return self.nombre


class Jugador(models.Model):
    equipo = models.ForeignKey(Equipo)
    nombre = models.CharField(max_length=100)
    fecha_alta = models.DateTimeField('Fecha de Alta')

    def __unicode__(self):
        return self.nombre

