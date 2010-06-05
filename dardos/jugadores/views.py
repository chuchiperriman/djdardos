# -*- mode: python; tab-width: 4; indent-tabs-mode: nil -*-

from djdardos.dardos.models import *
from django.shortcuts import render_to_response, get_object_or_404

from django.http import HttpResponse, Http404



# Create your views here.
def index(request):
    if 'q' in request.GET:
        jugadores_list = Jugador.objects.filter(
            nombre__contains=request.GET["q"]).order_by('equipo', 'nombre')
    else:
        jugadores_list = Jugador.objects.all().order_by('equipo', 'nombre')
    return render_to_response('dardos/jugadores/index.html', {'jugadores_list': jugadores_list})

def detail(request, jugador_id):
    p = get_object_or_404(Jugador, pk=jugador_id)
    return render_to_response('dardos/jugadores/detail.html', {'jugador': p})
    
