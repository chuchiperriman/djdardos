# -*- mode: python; tab-width: 4; indent-tabs-mode: nil -*-
# -*- coding: utf-8 -*-

from datetime import datetime
from djdardos.dardos.models import *
from django.db.models import Q
from django.shortcuts import render_to_response, get_object_or_404
from estadisticas import EstadisticasEquipo
from ..graficas.forms import GraficasForm
from estparejas import *
from django.template import RequestContext

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
    if "liga_actual" in request.session:
        liga_actual = Liga.objects.get(pk=request.session["liga_actual"])
    else:
        liga_actual = e.get_liga_actual()
    
    estadisticas = EstadisticasEquipo(e, liga_actual)
    jornadas = []
    for j in liga_actual.jornada_set.all():
        jornadas.append(JornadasPartidos(j, e))
        
    graficas_form = GraficasForm()
    graficas_form.fields["equipo"].initial = equipo_id
    graficas_form.fields["liga"].initial = liga_actual.id
    
    return render_to_response('dardos/equipos/detail.html', 
    	{'equipo': e, 'jugadores': estadisticas.jugadores,
         'liga_actual': liga_actual, 'jornadas': jornadas,
         'estadisticas': estadisticas,
         'graficas_form' : graficas_form},
         context_instance = RequestContext(request))

def ajax_estadistica_parejas(request, equipo_id, liga_id):
    try:
        equipo = Equipo.objects.get(pk=equipo_id)
        liga = Liga.objects.get(pk=liga_id)
        estparejas = get_estadistica_parejas (equipo, liga)
    except:
        import traceback
        import sys
        traceback.print_exc(file=sys.stdout)
    return render_to_response('dardos/equipos/estparejas.html',
        {'estadistica' : estparejas})
         
def estreport(request, equipo_id, liga_id):
    e = get_object_or_404(Equipo, pk=equipo_id)
    liga_actual = Liga.objects.get(pk=liga_id)
    estadisticas = EstadisticasEquipo(e, liga_actual)
    estparejas = get_estadistica_parejas (e, liga_actual)
    return render_to_response('dardos/equipos/estreport.html',
        {'jugadores': estadisticas.jugadores,
         'estadisticas': estadisticas,
         'estadistica_parejas': estparejas})
         
