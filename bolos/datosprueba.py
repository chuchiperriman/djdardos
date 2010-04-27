# -*- mode: python; tab-width: 4; indent-tabs-mode: nil -*-

from bolos.models import *
from datetime import datetime

def cargar():
    d = Division(pk=1, nombre="Primera")
    d.save()
    d = Division(pk=2, nombre="Segunda")
    d.save()
    d = Division(pk=3, nombre="Tercera")
    d.save()
    l = Liga(pk=1, nombre="2010", division=d)
    l.save()
    for i in range(20):
        j = Jornada(pk=i+1, numero=i+1, liga=l)
        j.save()
    
    e = Equipo(pk=1, nombre="Paris XX")
    e.save()
    e.ligas.add(l)
    j = Jugador(pk=1, nombre="Chuchi", fecha_alta=datetime.now(), equipo=e)
    j.save()
    j = Jugador(pk=2, nombre="Rego", fecha_alta=datetime.now(), equipo=e)
    j.save()
    j = Jugador(pk=3, nombre="Jose", fecha_alta=datetime.now(), equipo=e)
    j.save()
    e2 = Equipo(pk=2, nombre="Coffebeer")
    e2.save()
    e2.ligas.add(l)
    j = Jugador(pk=4, nombre="Pablo", fecha_alta=datetime.now(), equipo=e2)
    j.save()
    j = Jugador(pk=5, nombre="Marcos", fecha_alta=datetime.now(), equipo=e2)
    j.save()
    j = Jugador(pk=6, nombre="Marta", fecha_alta=datetime.now(), equipo=e2)
    j.save()
