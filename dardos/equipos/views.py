# -*- mode: python; tab-width: 4; indent-tabs-mode: nil -*-
# -*- coding: utf-8 -*-

from datetime import datetime
from djdardos.dardos.models import *
from django.db.models import Q
from django.shortcuts import render_to_response, get_object_or_404
from django.views.generic.simple import direct_to_template
from estadisticas import *
from ..graficas.forms import GraficasForm
from ..general.sesiones import *
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
            nombre__contains=request.GET["q"])
    else:
        equipos = Equipo.objects.all()
        
    liga_actual = get_liga_actual(request)
    if liga_actual:
        equipos = equipos.filter(ligas = liga_actual)
    
    equipos = equipos.order_by('nombre')
    return direct_to_template(request, 'dardos/equipos/index.html', {'equipos': equipos})

def detail(request, equipo_id):
    e = get_object_or_404(Equipo, pk=equipo_id)
    if "liga_actual" in request.session:
        liga_actual = Liga.objects.get(pk=request.session["liga_actual"])
    else:
        liga_actual = e.get_liga_actual()
    
    estadisticas = EstadisticasEquipo(e, liga_actual)
    jugadores = e.jugador_set.all()
    partidos = Partido.objects.filter(jornada__liga__exact = liga_actual).distinct()
    estjugadores = DatosEstadisticaJugadores(jugadores, partidos)
    analisis_jugadores = AnalisisJugadores(estjugadores)
    jornadas = []
    for j in liga_actual.jornada_set.all():
        jornadas.append(JornadasPartidos(j, e))
        
    graficas_form = GraficasForm()
    graficas_form.fields["equipo"].initial = equipo_id
    graficas_form.fields["liga"].initial = liga_actual.id
    
    return render_to_response('dardos/equipos/detail.html', 
    	{'equipo': e, 'estjugadores': estjugadores,
         'liga_actual': liga_actual, 'jornadas': jornadas,
         'estadisticas': estadisticas,
         'analisis_jugadores': analisis_jugadores,
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
         
