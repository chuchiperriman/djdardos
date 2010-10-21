# -*- mode: python; tab-width: 4; indent-tabs-mode: nil -*-
# -*- coding: utf-8 -*-

from djdardos.dardos.models import *
from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponse, Http404

from ..templatetags.graficos import *
from ..equipos.estadisticas import DatosEstadisticaJugador
from ..graficas import graficas
from ..graficas.forms import GraficasForm

# Create your views here.
def index(request):
    if 'q' in request.GET:
        jugadores_list = Jugador.objects.filter(
            nombre__contains=request.GET["q"]).order_by('equipo', 'nombre')
    else:
        jugadores_list = Jugador.objects.all().order_by('equipo', 'nombre')
    return render_to_response('dardos/jugadores/index.html', {'jugadores_list': jugadores_list})

def detail(request, jugador_id):
    jugador = get_object_or_404(Jugador, pk=jugador_id)
    jugador_datos = DatosEstadisticaJugador(jugador)
    ordenado = {}
    
    for p in jugador.partidas_ganadas():
        if not p.partido.jornada.numero in ordenado:
            ordenado[p.partido.jornada.numero] = DatosJornadaGP(
                p.partido.jornada.numero, 1, 0)
        else:
            ordenado[p.partido.jornada.numero].ganados += 1

    for p in jugador.partidas_perdidas():
        if not p.partido.jornada.numero in ordenado:
            ordenado[p.partido.jornada.numero] = DatosJornadaGP(
                p.partido.jornada.numero, 0, 1)
        else:
            ordenado[p.partido.jornada.numero].perdidos += 1
    
    graficas_form = GraficasForm()
    graficas_form.fields["equipo"].initial = jugador.equipo.id
    graficas_form.fields["jugador"].initial = jugador.id
    graficas_form.fields["liga"].initial = jugador.equipo.get_liga_actual().id
    return render_to_response('dardos/jugadores/detail.html', {
        'jugador': jugador,
        'jugador_datos': jugador_datos,
        'graficas_form' : graficas_form})
        
