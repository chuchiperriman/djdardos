# -*- mode: python; tab-width: 4; indent-tabs-mode: nil -*-
# -*- coding: utf-8 -*-

from djdardos.dardos.models import *
from django.db.models import Max
from djdardos.dardos.partidos.forms import *
from ..general.sesiones import *
from django.shortcuts import render_to_response, get_object_or_404

from django.http import HttpResponse, Http404

def ajax_jornadas_from_liga (request, liga_id):
    if request.is_ajax():
        jornadas = Jornada.objects.filter(liga=liga_id)
        texto = ""
        for j in jornadas:
            texto = texto + "<option value='"+str(j.id)+"'>"+str(j.numero)+ \
                " - " + str(j.fecha_prevista) + "</option>"
        return HttpResponse(texto)
    else:
        return HttpResponse(status=400)
        
