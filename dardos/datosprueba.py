# -*- mode: python; tab-width: 4; indent-tabs-mode: nil -*-

from dardos.models import *
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
    
    p = Partido(pk=1, jornada=Jornada.objects.get(pk=1), 
            equipo_local=e2, equipo_visitante=e, ganador=e2, 
            fecha=datetime.now())
    p.save()
    
    pa = PartidaIndividual(pk=1, partido=p, tipo="1", 
            jugador_local=Jugador.objects.get(pk=4),
            jugador_visitante=Jugador.objects.get(pk=1),
            ganador=Jugador.objects.get(pk=4))
    pa.save()
    
    pa = PartidaIndividual(pk=2, partido=p, tipo="1", 
            jugador_local=Jugador.objects.get(pk=5),
            jugador_visitante=Jugador.objects.get(pk=2),
            ganador=Jugador.objects.get(pk=2))
    pa.save()
    
    pa = PartidaIndividual(pk=3, partido=p, tipo="1", 
            jugador_local=Jugador.objects.get(pk=4),
            jugador_visitante=Jugador.objects.get(pk=2),
            ganador=Jugador.objects.get(pk=2))
    pa.save()
    
    pa = PartidaParejas(pk=1, partido=p, tipo="1", 
            jugador_local1=Jugador.objects.get(pk=4),
            jugador_local2=Jugador.objects.get(pk=5),
            jugador_visitante1=Jugador.objects.get(pk=1),
            jugador_visitante2=Jugador.objects.get(pk=3),
            ganador1=Jugador.objects.get(pk=1),
            ganador2=Jugador.objects.get(pk=3))
    pa.save()
    
    