# -*- mode: python; tab-width: 4; indent-tabs-mode: nil -*-

from datetime import datetime
from djdardos.dardos.models import *
from django.db.models import Q
from django.shortcuts import render_to_response, get_object_or_404
from estadisticas import EstadisticasEquipo

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
    print 'ini v', datetime.now()
    e = get_object_or_404(Equipo, pk=equipo_id)
    import logging
    logging.debug(e.ligas.all())
    liga_actual = e.ligas.all()[0]
    estadisticas = EstadisticasEquipo(e)
    jornadas = []
    for j in liga_actual.jornada_set.all():
        jornadas.append(JornadasPartidos(j, e))
    print 'fin v', datetime.now()    
    #TODO Esto es una cochinada temporal (lo de las ligas)
    return render_to_response('dardos/equipos/detail.html', 
    	{'equipo': e, 'jugadores': estadisticas.jugadores,
         'liga_actual': liga_actual, 'jornadas': jornadas,
         'estadisticas': estadisticas})

