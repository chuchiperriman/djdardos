# -*- mode: python; tab-width: 4; indent-tabs-mode: nil -*-

from djdardos.dardos.models import *
from djdardos.dardos.partidos.forms import *
from django.shortcuts import render_to_response, get_object_or_404

from django.http import HttpResponse, Http404
import logging


# Create your views here.
def index(request):
    partidos = Partido.objects.all().order_by('-fecha')
    return render_to_response('dardos/partidos/index.html', {'partidos': partidos})

def detail(request, partido_id):
    p = get_object_or_404(Partido, pk=partido_id)
    return render_to_response('dardos/partidos/detail.html', 
    	{'partido': p, 'partidas': p.partida_set.all()})
        
def prenew(request):
    if request.method == 'POST':
        form = PartidoPreForm(request.POST) # A form bound to the POST data
        if form.is_valid():
            form2 = PartidoForm()
            form2.cargar_datos(form.cleaned_data["equipo_local"],
                               form.cleaned_data["equipo_visitante"])
            return render_to_response('dardos/partidos/new2.html',
                {"form": form2})
    else:
        form = PartidoPreForm()
        
    equipos = Equipo.objects.all().order_by("nombre")
    return render_to_response('dardos/partidos/new1.html',
        {"equipos": equipos,
        "form": form})

def new(request):
    if request.method == 'POST':
        form = PartidoForm (request.POST)
        form.cargar_datos_por_id (form.data['equipo_local'],
            form.data['equipo_visitante'])
        if form.is_valid():
            logging.debug("Si es valido: "+str(form.cleaned_data))
            return render_to_response('dardos/partidos/new2.html',
                {"form": form})
        
        logging.debug("No es valido: "+str(form.data['equipo_local']))
        logging.debug("Errores: "+str(form.errors))
        return render_to_response('dardos/partidos/new2.html',
                {"form": form})
        
    return prenew(request)
    
    
    
