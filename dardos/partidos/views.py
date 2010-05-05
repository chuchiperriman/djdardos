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
"""    
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
"""

def new(request):
    
    form = PartidoForm()
    
    if request.method == 'POST':
        form = PartidoForm(request.POST) # A form bound to the POST data
        if form.is_valid():
            form.save()
            """
            p = Partido(jornada=form.cleaned_data['jornada'],
                equipo_local = form.cleaned_data['equipo_local'],
                equipo_visitante = form.cleaned_data['equipo_visitante'],
                fecha = form.cleaned_data['fecha'],
                jugado = False,
                ganador = None)
            p.save()
            """
            return index(request)
    
    
    equipos = Equipo.objects.all().order_by("nombre")
    return render_to_response('dardos/partidos/new.html',
        {"equipos": equipos,
        "form": form})

def setpartidas(request, partido_id):
    if request.method == 'POST':
        form = PartidasForm(data=request.POST, partido_id=partido_id)
        if form.is_valid():
            logging.debug('Valido !!')
            
    else:
        form = PartidasForm(partido_id=partido_id)

    #form.cargar_datos (partido_id)
        
    return render_to_response('dardos/partidos/setpartidas.html',
        {"form": form})

