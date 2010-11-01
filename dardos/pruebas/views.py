# -*- mode: python; tab-width: 4; indent-tabs-mode: nil -*-
# -*- coding: utf-8 -*-

from djdardos.dardos.models import *
from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponse, Http404
from django.conf import settings
import os
from django.core import serializers

# Create your views here.
def index(request):
    d = settings.MEDIA_ROOT + '/data/'
    ficheros = [Division,
        Liga,
        Jornada,
        Equipo,
        Jugador,
        Partido,
        Partida]

    for tipo in ficheros:
        print tipo.__name__ + ".xml"
        texto = open(d + tipo.__name__ + ".xml", "r").read()
        for obj in serializers.deserialize("xml", texto):
            obj.save()

    return render_to_response('dardos/pruebas/index.html', {})
