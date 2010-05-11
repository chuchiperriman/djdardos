# -*- mode: python; tab-width: 4; indent-tabs-mode: nil -*-

from djdardos.dardos.models import *
from djdardos.dardos.partidos.forms import *
from django.shortcuts import render_to_response, get_object_or_404

from django.http import HttpResponse, Http404
import logging


# Create your views here.
def index(request):
    partidos = Partido.objects.all().order_by('jornada')
    return render_to_response('dardos/partidos/index.html', {'partidos': partidos})

def detail(request, partido_id):
    p = get_object_or_404(Partido, pk=partido_id)
    return render_to_response('dardos/partidos/detail.html', 
    	{'partido': p, 'partidas': p.partida.all()})
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
            
    #q = Partido.objects.all().values('jornada').query
    #form.fields["jornada"].queryset = Jornada.objects.exclude(pk__in=q)
    equipos = Equipo.objects.all().order_by("nombre")
    return render_to_response('dardos/partidos/new.html',
        {"equipos": equipos,
        "form": form})

def setpartidas(request, partido_id):

    def crear_partida_parejas(prefix, post=None):
        p = PartidaParejas()
        p.partido = Partido.objects.get(pk=partido_id)
        if post:
            f = PartidaParejasForm(post,prefix=prefix, instance=p)
        else:
            f = PartidaParejasForm(prefix=prefix, instance=p)
        f.fields["jugador_local1"].queryset = Jugador.objects.filter(equipo=p.partido.equipo_local)
        f.fields["jugador_local2"].queryset = Jugador.objects.filter(equipo=p.partido.equipo_local)
        f.fields["jugador_visitante1"].queryset = Jugador.objects.filter(equipo=p.partido.equipo_visitante)
        f.fields["jugador_visitante2"].queryset = Jugador.objects.filter(equipo=p.partido.equipo_visitante)
        f.fields["ganador1"].queryset = Jugador.objects.filter(Q(equipo=p.partido.equipo_local) |
                                            Q(equipo=p.partido.equipo_visitante))
        return f
    
    if request.method == 'POST':
        forms_parejas_1 = [crear_partida_parejas(x,request.POST) for x in range(0,2)]
        if all([f.is_valid() for f in forms_parejas_1]):
            logging.debug('Valido !!')
        else:
            logging.debug('NOOOO Valido !!')
    else:
        forms_parejas_1 = [crear_partida_parejas(x) for x in range(0,2)]
        
    forms_parejas_2 = [crear_partida_parejas(x) for x in range(2,4)]
    forms_individual_1 = [PartidaIndividualForm(prefix=str(x), instance=PartidaIndividual()) for x in range(4,8)]
    forms_parejas_3 = [crear_partida_parejas(x) for x in range(8,10)]
    forms_parejas_4 = [crear_partida_parejas(x) for x in range(10,12)]
    forms_individual_2 = [PartidaIndividualForm(prefix=str(x), instance=PartidaIndividual()) for x in range(12,16)]

    return render_to_response('dardos/partidos/setpartidas.html',
        {"forms_parejas_1": forms_parejas_1,
         "forms_parejas_2": forms_parejas_2,
         "forms_individual_1": forms_individual_1,
         "forms_parejas_3": forms_parejas_1,
         "forms_parejas_4": forms_parejas_2,
         "forms_individual_2": forms_individual_1})

