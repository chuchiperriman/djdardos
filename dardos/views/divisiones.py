# -*- mode: python; tab-width: 4; indent-tabs-mode: nil -*-

from djdardos.dardos.models import *
from django.db.models import Q
from django.shortcuts import render_to_response, get_object_or_404
from djdardos.dardos.liga.clasificacion import *
from djdardos.dardos.general.sesiones import *
from django.core import serializers
from django.template import RequestContext


from django.http import HttpResponse, Http404

def detail(request, division_id):
    d = Division.objects.get(pk=division_id)
    liga_actual = get_liga_actual(request)
    l = None
    if liga_actual in d.liga_set.all():
        l = Liga.objects.get(pk=request.session[LIGA_ACTUAL])
    if not l:
        l = d.get_liga_actual()
        
    request.session[LIGA_ACTUAL] = l.id
    request.session[DIVISION_ACTUAL] = d.id
    
    equipos = list()
    for e in l.equipo_set.all():
        equipos.append(e)
    
    cuadro = []
    for e in equipos:
        linea = []
        for e2 in equipos:
            partido = Partido.objects.filter(jornada__liga__exact=liga_actual, equipo_local=e, equipo_visitante=e2)
            if partido:
                partido = partido[0]
                print e,e2, partido
        
    return render_to_response('dardos/divisiones/detail.html', 
    	{'division': d,
         'liga': l,
         'current_path': request.path},
         context_instance = RequestContext(request))
         
