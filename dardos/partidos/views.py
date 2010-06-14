# -*- mode: python; tab-width: 4; indent-tabs-mode: nil -*-

import procesos

from djdardos.dardos.models import *
#from djdardos.dardos.partidos.forms import *
from django.shortcuts import render_to_response, get_object_or_404
from django.views.generic.create_update import create_object

from django.http import HttpResponse, Http404
import logging


# Create your views here.
def index(request):
    partidos = Partido.objects.all().order_by('jornada')
    return render_to_response('dardos/partidos/index.html', {'partidos': partidos})

def detail(request, partido_id):
    p = get_object_or_404(Partido, pk=partido_id)
    partidas = p.partida_set.order_by('numero')
    partidas = list(partidas)
    print partidas
    return render_to_response('dardos/partidos/detail.html', 
    	{'partido' : p,
         'partidas_par_1' : partidas[0:2],
         'partidas_par_2' : partidas[2:4],
         'partidas_ind_1' : partidas[4:8],
         'partidas_par_3' : partidas[8:10],
         'partidas_par_4' : partidas[10:12],
         'partidas_ind_2' : partidas[12:16]})

"""
def new(request):
    
    form = PartidoForm()
    
    if request.method == 'POST':
        form = PartidoForm(request.POST) # A form bound to the POST data
        if form.is_valid():
            form.save()
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
        p.numero = int(prefix) + 1
        print p.numero,'paaaar'
        if post:
            f = PartidaParejasForm(post,prefix=prefix, instance = p)
        else:
            f = PartidaParejasForm(prefix=prefix, instance = p)
        f.fields["jugador_local1"].queryset = Jugador.objects.filter(equipo=p.partido.equipo_local)
        f.fields["jugador_local2"].queryset = Jugador.objects.filter(equipo=p.partido.equipo_local)
        f.fields["jugador_visitante1"].queryset = Jugador.objects.filter(equipo=p.partido.equipo_visitante)
        f.fields["jugador_visitante2"].queryset = Jugador.objects.filter(equipo=p.partido.equipo_visitante)
        f.fields["ganador1"].queryset = Jugador.objects.filter(Q(equipo=p.partido.equipo_local) |
                                            Q(equipo=p.partido.equipo_visitante))
        f.fields["ganador2"].queryset = Jugador.objects.filter(Q(equipo=p.partido.equipo_local) |
                                            Q(equipo=p.partido.equipo_visitante))
        return f
    
    def crear_partida_individual(prefix, post=None):
        p = PartidaIndividual()
        p.partido = Partido.objects.get(pk=partido_id)
        p.numero = int(prefix) + 1
        print p.numero,'---'
        if post:
            f = PartidaIndividualForm(post,prefix=prefix, instance = p)
        else:
            f = PartidaIndividualForm(prefix=prefix, instance = p)
        f.fields["jugador_local"].queryset = Jugador.objects.filter(equipo=p.partido.equipo_local)
        f.fields["jugador_visitante"].queryset = Jugador.objects.filter(equipo=p.partido.equipo_visitante)
        f.fields["ganador"].queryset = Jugador.objects.filter(Q(equipo=p.partido.equipo_local) |
                                            Q(equipo=p.partido.equipo_visitante))
        return f
        
    if request.method == 'POST':
        forms_parejas_1 = [crear_partida_parejas(str(x),request.POST) for x in range(0,2)]
        forms_parejas_2 = [crear_partida_parejas(str(x),request.POST) for x in range(2,4)]
        forms_individual_1 = [crear_partida_individual(str(x), request.POST) for x in range(4,8)]
        forms_parejas_3 = [crear_partida_parejas(str(x),request.POST) for x in range(8,10)]
        forms_parejas_4 = [crear_partida_parejas(str(x),request.POST) for x in range(10,12)]
        forms_individual_2 = [crear_partida_individual(str(x), request.POST) for x in range(12,16)]
        todos = []
        todos.extend(forms_parejas_1)
        todos.extend(forms_parejas_2)
        todos.extend(forms_parejas_3)
        todos.extend(forms_parejas_4)
        todos.extend(forms_individual_1)
        todos.extend(forms_individual_2)
        
        if all([f.is_valid() for f in todos]):
            #TODO Comprobar que una pareja del grupo 1 no puede jugar en el grupo 2
            #TODO Comprobar que una un jugador no puede jugar mas de una individual de cada grupo
            for f in todos:
                f.save()
        
            partido = Partido.objects.get(pk=partido_id)
            partido.jugado = True
            #Este metodo guarda el partido
            procesos.actualizar_puntos_partido(partido)
        else:
            logging.debug('NOOOO Valido !!')
    else:
        forms_parejas_1 = [crear_partida_parejas(str(x)) for x in range(0,2)]
        forms_parejas_2 = [crear_partida_parejas(str(x)) for x in range(2,4)]
        forms_individual_1 = [crear_partida_individual(str(x)) for x in range(4,8)]
        forms_parejas_3 = [crear_partida_parejas(str(x)) for x in range(8,10)]
        forms_parejas_4 = [crear_partida_parejas(str(x)) for x in range(10,12)]
        forms_individual_2 = [crear_partida_individual(str(x)) for x in range(12,16)]
        todos = []

    return render_to_response('dardos/partidos/setpartidas.html',
        {"forms_parejas_1": forms_parejas_1,
         "forms_parejas_2": forms_parejas_2,
         "forms_individual_1": forms_individual_1,
         "forms_parejas_3": forms_parejas_3,
         "forms_parejas_4": forms_parejas_4,
         "forms_individual_2": forms_individual_2,
         "todos": todos})

def new_jornada (request):
    return create_object(
        request,
        form_class=JornadaForm,
        post_save_redirect='new')
"""
        
        
