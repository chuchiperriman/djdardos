# -*- mode: python; tab-width: 4; indent-tabs-mode: nil -*-

from dardos.models import *
from datetime import datetime

from xml.dom.minidom import parse

def to_new_partidas():
    for pi in PartidaIndividual.objects.all():
        p = Partida()
        p.numero = pi.numero
        p.partido = pi.partido
        p.tipo = 1
        p.tipo_juego = pi.tipo
        p.save()
        p.jugadores_local.add(pi.jugador_local)
        p.jugadores_visitante.add(pi.jugador_visitante)
        p.ganadores.add(pi.ganador)
        p.save()
        print 'Saved: ', p
    for pi in PartidaParejas.objects.all():
        p = Partida()
        p.numero = pi.numero
        p.partido = pi.partido
        p.tipo = 2
        p.tipo_juego = pi.tipo
        p.save()
        p.jugadores_local.add(pi.jugador_local1)
        p.jugadores_local.add(pi.jugador_local2)
        p.jugadores_visitante.add(pi.jugador_visitante1)
        p.jugadores_visitante.add(pi.jugador_visitante2)
        p.ganadores.add(pi.ganador1)
        p.ganadores.add(pi.ganador2)
        p.save()
        print 'Saved: ', p
        
def cargar():
    dom = parse("/home/perriman/dev/djdardos/data/datos.xml")
    root = dom.childNodes[0]
    
    equipos = {}
    
    for en in root.getElementsByTagName("equipo"):
        equipos[en.attributes["id"].value] = en.attributes["nombre"].value
        e = Equipo(pk=en.attributes["id"].value, nombre=en.attributes["nombre"].value)
        e.save()
        Jugador.objects.filter(equipo=e).delete()
        print 'equipo',e.nombre
        for jn in en.getElementsByTagName("jugador"):
            j = Jugador(pk=jn.attributes["id"].value, nombre=jn.attributes["nombre"].value,
                fecha_alta=datetime.now(), equipo=e)
            j.save()
            print '\tjugador', j.nombre
    for dn in root.getElementsByTagName("division"):
        Division.objects.filter(nombre=dn.attributes["nombre"].value).delete()
        d = Division(nombre=dn.attributes["nombre"].value)
        d.save()
        print 'division',d.nombre
        for ln in dn.getElementsByTagName("liga"):
            l = Liga(nombre=ln.attributes["nombre"].value, division=d)
            l.save()
            print '\tliga', l.nombre
            for eln in ln.getElementsByTagName("equipo_liga"):
                e = Equipo.objects.get(pk=eln.attributes["id"].value)
                e.ligas.add(l)
                e.save()
            for jn in ln.getElementsByTagName("jornada"):
                j = Jornada(liga=l, numero=jn.attributes["numero"].value)
                j.save()
                Partido.objects.filter(jornada=j).delete()
                print '\t\tjornada', j.numero
                for pn in jn.getElementsByTagName("partido"):
                    p = Partido(equipo_local=Equipo.objects.get(pk=pn.attributes["equipo_local"].value),
                        equipo_visitante=Equipo.objects.get(pk=pn.attributes["equipo_visitante"].value),
                        ganador=Equipo.objects.get(pk=pn.attributes["ganador"].value),
                        fecha=datetime.strptime(pn.attributes["fecha"].value, "%d/%m/%Y"),
                        jugado=bool(pn.attributes["jugado"].value),
                        jornada=j)
                    p.save()
                    print '\t\t\tpartido',p.fecha,p.equipo_local,p.equipo_visitante
                    for ppn in pn.getElementsByTagName("partidapar"):
                        pp = PartidaParejas(partido=p, tipo=ppn.attributes["tipo"].value, 
                            jugador_local1=Jugador.objects.get(pk=ppn.attributes["jugador_local1"].value),
                            jugador_local2=Jugador.objects.get(pk=ppn.attributes["jugador_local2"].value),
                            jugador_visitante1=Jugador.objects.get(pk=ppn.attributes["jugador_visitante1"].value),
                            jugador_visitante2=Jugador.objects.get(pk=ppn.attributes["jugador_visitante2"].value),
                            ganador1=Jugador.objects.get(pk=ppn.attributes["ganador1"].value),
                            ganador2=Jugador.objects.get(pk=ppn.attributes["ganador2"].value))
                        pp.save()
                        print '\t\t\t\tpartida parejas',pp.pk
                    for pin in pn.getElementsByTagName("partidaind"):
                        pi = PartidaIndividual(partido=p, tipo=pin.attributes["tipo"].value, 
                            jugador_local=Jugador.objects.get(pk=pin.attributes["jugador_local"].value),
                            jugador_visitante=Jugador.objects.get(pk=pin.attributes["jugador_visitante"].value),
                            ganador=Jugador.objects.get(pk=pin.attributes["ganador"].value))
                        pi.save()
                        print '\t\t\t\tpartida individual',pi.pk
                    
    return
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
            fecha=datetime.now(),
            jugado = True)
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
    
    temp = Equipo(pk=3, nombre="Equipo Primero")
    temp.save()
    temp.ligas.add(l)
    e3 = Equipo(pk=4, nombre="Equipo Tercero")
    e3.save()
    e3.ligas.add(l)
    e4 = Equipo(pk=5, nombre="Equipo Cuarto")
    e4.save()
    e4.ligas.add(l)
    
    p = Partido(pk=3, jornada=Jornada.objects.get(pk=3), 
            equipo_local=e, equipo_visitante=e3, ganador=None, 
            fecha=datetime.now(),
            jugado = False)
    p.save()
    
    p = Partido(pk=4, jornada=Jornada.objects.get(pk=4), 
            equipo_local=e4, equipo_visitante=e, ganador=None, 
            fecha=datetime.now(),
            jugado = False)
    p.save()
    
    
