# -*- mode: python; tab-width: 4; indent-tabs-mode: nil -*-

from djbolos.bolos.models import *
from django.shortcuts import render_to_response, get_object_or_404

from django.http import HttpResponse, Http404



# Create your views here.
def index(request):
    equipos = Equipo.objects.all().order_by('nombre')
    return render_to_response('bolos/equipos/index.html', {'equipos': equipos})

def detail(request, equipo_id):
    e = get_object_or_404(Equipo, pk=equipo_id)
    return render_to_response('bolos/equipos/detail.html', 
    	{'equipo': e, 'jugadores': e.jugador_set.all()})
    
