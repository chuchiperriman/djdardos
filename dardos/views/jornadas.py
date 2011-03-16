# -*- mode: python; tab-width: 4; indent-tabs-mode: nil -*-

from djdardos.dardos.models import *
from django.shortcuts import render_to_response
from django.http import HttpResponse

def ajax_jornada_detail(request):
    partidos = Partido.objects.filter(jornada = request.GET["id"])
    return render_to_response('dardos/partidos/partidos_jornada_block.html', 
    	{'partidos': partidos})
    	
def ajax_jornadas_from_liga (request):
    if request.is_ajax():
        jornadas = Jornada.objects.filter(liga=request.GET["id"])
        texto = ""
        for j in jornadas:
            texto = texto + "<option value='"+str(j.id)+"'>"+str(j.numero)+ \
                " - " + str(j.fecha_prevista) + "</option>"
        return HttpResponse(texto)
    else:
        return HttpResponse(status=400)
