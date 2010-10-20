# -*- mode: python; tab-width: 4; indent-tabs-mode: nil -*-
# -*- coding: utf-8 -*-

from datetime import datetime
from djdardos.dardos.models import *
from django.db.models import Q
from django.shortcuts import render_to_response, get_object_or_404
from estadisticas import EstadisticasEquipo
from ..templatetags.graficos import JornadasGrafico
from ..graficas.forms import GraficasForm

from django.http import HttpResponse, Http404

class JornadasPartidos:
    jornada = None
    partido = None
    def __init__(self, jornada, equipo):
        self.jornada = jornada
        partidos = jornada.partido_set.filter(Q(equipo_local=equipo) | Q(equipo_visitante=equipo))
        if partidos:
            self.partido = partidos[0]

# Create your views here.
def index(request):
    if 'q' in request.GET:
        equipos = Equipo.objects.filter(
            nombre__contains=request.GET["q"]).order_by('nombre')
    else:
        equipos = Equipo.objects.all().order_by('nombre')
    return render_to_response('dardos/equipos/index.html', {'equipos': equipos})

def detail(request, equipo_id):
    e = get_object_or_404(Equipo, pk=equipo_id)
    liga_actual = e.get_liga_actual()
    estadisticas = EstadisticasEquipo(e, liga_actual)
    jornadas = []
    for j in liga_actual.jornada_set.all():
        jornadas.append(JornadasPartidos(j, e))
        
    graficas_form = GraficasForm()
    graficas_form.fields["equipo"].initial = equipo_id
    
    return render_to_response('dardos/equipos/detail.html', 
    	{'equipo': e, 'jugadores': estadisticas.jugadores,
         'liga_actual': liga_actual, 'jornadas': jornadas,
         'estadisticas': estadisticas,
         'graficas_form' : graficas_form})

