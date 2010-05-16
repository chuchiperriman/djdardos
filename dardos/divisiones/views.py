# -*- mode: python; tab-width: 4; indent-tabs-mode: nil -*-

from djdardos.dardos.models import *
from django.db.models import Q
from django.shortcuts import render_to_response, get_object_or_404
from djdardos.dardos.liga.clasificacion import *

from django.http import HttpResponse, Http404

def detail(request, division_id):
    d = Division.objects.get(pk=division_id)
    l = d.liga_set.get(nombre="2010")
    return render_to_response('dardos/divisiones/detail.html', 
    	{'division': d,
         'liga': l})
