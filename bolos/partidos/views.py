# -*- mode: python; tab-width: 4; indent-tabs-mode: nil -*-

from djbolos.bolos.models import *
from django.shortcuts import render_to_response, get_object_or_404

from django.http import HttpResponse, Http404



# Create your views here.
def index(request):
    partidos = Partido.objects.all().order_by('-fecha')
    return render_to_response('bolos/partidos/index.html', {'partidos': partidos})

def detail(request, partido_id):
    p = get_object_or_404(Partido, pk=partido_id)
    return render_to_response('bolos/partidos/detail.html', 
    	{'partido': p, 'partidas': p.partida_set.all()})
        
def new(request):
    return render_to_response('bolos/partidos/new.html')
    
