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
    if LIGA_ACTUAL in request.session:
        l = Liga.objects.get(pk=request.session[LIGA_ACTUAL])
    else:
        l = d.get_liga_actual()
        
    request.session[LIGA_ACTUAL] = l.id
    request.session[DIVISION_ACTUAL] = d.id
        
    return render_to_response('dardos/divisiones/detail.html', 
    	{'division': d,
         'liga': l,
         'current_path': request.path},
         context_instance = RequestContext(request))

         
def ajax_jornada_detail(request, jornada_id):
    """
    if request.is_ajax():
        mimetype = 'application/javascript'
        jornada = Jornada.objects.get(pk=jornada_id)
        data = serializers.serialize('json', jornada.partido_set.all())
        return HttpResponse(data,mimetype)
    else:
        return HttpResponse(status=400)
    """
    partidos = Partido.objects.filter(jornada = jornada_id)
    return render_to_response('dardos/partidos/partidos_jornada_block.html', 
    	{'partidos': partidos})

