# -*- mode: python; tab-width: 4; indent-tabs-mode: nil -*-

from djbolos.bolos.models import *
from djbolos.bolos.partidos.forms import *
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
        
def prenew(request):
    if request.method == 'POST':
        form = PartidoPreForm(request.POST) # A form bound to the POST data
        if form.is_valid():
            form2 = PartidoForm(equipo_local=form.cleaned_data["equipo_local"],
                                equipo_visitante=form.cleaned_data["equipo_visitante"])
            return render_to_response('bolos/partidos/new2.html',
                {"form": form2})
    else:
        form = PartidoPreForm()
        
    equipos = Equipo.objects.all().order_by("nombre")
    return render_to_response('bolos/partidos/new1.html',
        {"equipos": equipos,
        "form": form})

def new(request):
    if request.method == 'POST':
        form = PartidoPreForm(request.POST)
        form = PartidoForm (request.POST, equipo_local=form.cleaned_data["equipo_local"],
                           equipo_visitante=form.cleaned_data["equipo_visitante"])
        if form.is_valid():
            return detail(request)
        
        return render_to_response('bolos/partidos/new2.html',
                {"form": form})
        
    return prenew(request)
    
    
    
