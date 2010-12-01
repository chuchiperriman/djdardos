# -*- mode: python; tab-width: 4; indent-tabs-mode: nil -*-
# -*- coding: utf-8 -*-

import procesos

from djdardos.dardos.models import *
from django.db.models import Max
from djdardos.dardos.partidos.forms import *
from ..general.sesiones import *
from ..equipos.estadisticas import DatosEstadisticaJugadores, AnalisisJugadores
from django.shortcuts import render_to_response, get_object_or_404
from django.views.generic.simple import direct_to_template
from django.views.generic.create_update import create_object
from django.contrib import messages
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.contrib.auth.decorators import login_required, permission_required

def index(request):
    partidos = Partido.objects.all()
    liga_actual = get_liga_actual(request)
    if liga_actual:
        partidos = partidos.filter(jornada__in=Jornada.objects.filter(liga = liga_actual))
        
    partidos = partidos.order_by('jornada')
    return direct_to_template(request, 'dardos/partidos/index.html', {'partidos': partidos})

def detail(request, partido_id, reporting=None):
    p = get_object_or_404(Partido, pk=partido_id)
    partidoq = Partido.objects.filter(pk=partido_id)
    partidas = p.partida_set.order_by('numero')
    
    jugadores = Jugador.objects.filter(Q(jugadores_local__in= partidas) | Q(jugadores_visitante__in= partidas)).distinct()
    estadisticas_jugadores = list()
    estadisticas_jugadores = DatosEstadisticaJugadores(jugadores, partidoq)
    analisis_jugadores = AnalisisJugadores(estadisticas_jugadores)
    
    #local
    jugadores_local = Jugador.objects.filter(Q(jugadores_local__in=partidas)).distinct()
    ej_local = DatosEstadisticaJugadores(jugadores_local, partidoq)
    aj_local = AnalisisJugadores(ej_local)
    
    #visitante
    jugadores_visitante = Jugador.objects.filter(Q(jugadores_visitante__in=partidas)).distinct()
    ej_visitante = DatosEstadisticaJugadores(jugadores_visitante, partidoq)
    aj_visitante = AnalisisJugadores(ej_visitante)
    
    partidas = list(partidas)
    if len(partidas) > 0:
        if reporting == 'reporting':
            template = 'dardos/partidos/detailreporting.html'
        else:
            template = 'dardos/partidos/detail.html'
            
        return direct_to_template(request, template, 
        	{'partido' : p,
             'partidas_par_1' : partidas[0:2],
             'partidas_par_2' : partidas[2:4],
             'partidas_ind_1' : partidas[4:8],
             'partidas_par_3' : partidas[8:10],
             'partidas_par_4' : partidas[10:12],
             'partidas_ind_2' : partidas[12:16],
             'estadisticas_jugadores': estadisticas_jugadores,
             'analisis_jugadores': analisis_jugadores,
             'analisis_local': aj_local,
             'analisis_visitante': aj_visitante})
    else:
        return direct_to_template(request, 'dardos/partidos/detail_sin_acta.html', 
        	{'partido' : p})

@login_required
def new(request):
    #TODO hacer funcion global para usar en muchos sitios
    if not request.user.has_perm("dardos.can_add_todo") and not request.user.has_perm("dardos.can_add_equipo"):
        return HttpResponseRedirect("/errores_permisos")
        
    ligas = Liga.objects.all()
    jornadas = None
    liga = None
    equipos = None
    liga_sesion = get_liga_actual(request)
    if request.user.has_perm("dardos.can_add_todo"):
        if "liga" in request.REQUEST and request.REQUEST["liga"] != '':
            liga = request.REQUEST["liga"]
            jornadas = Jornada.objects.filter(liga=liga)
        elif liga_sesion:
            liga = str(liga_sesion.id)
            jornadas = liga_sesion.jornada_set.all()
        else:
            jornadas = ligas[0].jornada_set.all()
    elif request.user.has_perm("dardos.can_add_equipo"):
        #TODO Comprobar que en la liga esté el equipo del usuario
        #sino hay que poner la liga de su equipo
        return HttpResponse("De momento sin hacer")
    else:
        return HttpResponseRedirect("/error_permisos")
        
    
    if liga:
        liga_obj = Liga.objects.get(pk=liga)
        equipos = liga_obj.equipo_set.all()
        
    return create_object(
        request,
        form_class=PartidoForm,
        post_save_redirect='/partidos/new',
        extra_context={
            'ligas': ligas,
            'jornadas': jornadas,
            'liga': liga,
            'equipos' : equipos
        })

@permission_required('dardos.add_partido')
@login_required
def setpartidas(request, partido_id):
    
    partido = Partido.objects.get(pk=partido_id)
    jugadores_local_choices = list()
    for j in partido.equipo_local.jugador_set.all():
        jugadores_local_choices.append((j.id, j.nombre))
    jugadores_visitante_choices = list()
    for j in partido.equipo_visitante.jugador_set.all():
        jugadores_visitante_choices.append((j.id, j.nombre))
    
    def crear_partida_parejas(prefix, post=None, tipo_juego=1):
        numero = int(prefix) + 1
        if post:
            f = PartidaParejasForm(post,prefix=prefix)
        else:
            f = PartidaParejasForm(prefix=prefix)
            p = partido.partida_set.filter(numero=numero)
            if p and len(p) == 1:
                f.load(p[0])
                
        f.fields["numero"].initial = numero
        f.fields["tipo_juego"].initial = tipo_juego
        f.fields["jugador_local"].widget.choices = jugadores_local_choices
        f.fields["jugador_local2"].widget.choices = jugadores_local_choices
        f.fields["jugador_visitante"].widget.choices = jugadores_visitante_choices
        f.fields["jugador_visitante2"].widget.choices = jugadores_visitante_choices
        return f
        
    def crear_partida_individual(prefix, post=None):
        numero = int(prefix) + 1
        if post:
            f = PartidaIndividualForm(post,prefix=prefix)
        else:
            f = PartidaIndividualForm(prefix=prefix)
            p = partido.partida_set.filter(numero=numero)
            if p and len(p) == 1:
                f.load(p[0])
            
        f.fields["numero"].initial = numero
        f.fields["jugador_local"].widget.choices = jugadores_local_choices
        f.fields["jugador_visitante"].widget.choices = jugadores_visitante_choices
        return f
        
    partido = Partido.objects.get(pk=partido_id)
    
    if request.method == 'POST':
        forms_parejas_1 = [crear_partida_parejas(str(x),request.POST) for x in range(0,2)]
        forms_parejas_2 = [crear_partida_parejas(str(x),request.POST) for x in range(2,4)]
        forms_individual_1 = [crear_partida_individual(str(x), request.POST) for x in range(4,8)]
        forms_parejas_3 = [crear_partida_parejas(str(x),request.POST,2) for x in range(8,10)]
        forms_parejas_4 = [crear_partida_parejas(str(x),request.POST,2) for x in range(10,12)]
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
            #TODO Comprobar que un jugador no puede jugar mas de una individual de cada grupo
            partido.partida_set.all().delete()
            partido.save()
            partido = Partido.objects.get(pk=partido_id)
            for f in todos:
                f.save(partido)
        
            #Este metodo guarda el partido
            procesos.actualizar_puntos_partido(partido)
            messages.success (request, 'Partido dado de alta correctamente')
            
            return HttpResponseRedirect('/partidos/%d/' % (partido.id))
            
        else:
            messages.error (request, 'Revise los datos del acta porque se han producido errores')
    else:
        todos = []
        forms_parejas_1 = [crear_partida_parejas(str(x)) for x in range(0,2)]
        forms_parejas_2 = [crear_partida_parejas(str(x)) for x in range(2,4)]
        forms_individual_1 = [crear_partida_individual(str(x)) for x in range(4,8)]
        forms_parejas_3 = [crear_partida_parejas(str(x), None, 2) for x in range(8,10)]
        forms_parejas_4 = [crear_partida_parejas(str(x), None, 2) for x in range(10,12)]
        forms_individual_2 = [crear_partida_individual(str(x)) for x in range(12,16)]
    
    return direct_to_template(request, 'dardos/partidos/setpartidas.html',
        {"partido": partido,
         "jugadores_local": partido.equipo_local.jugador_set.all(),
         "jugadores_visitante": partido.equipo_visitante.jugador_set.all(),
         "forms_parejas_1": forms_parejas_1,
         "forms_parejas_2": forms_parejas_2,
         "forms_parejas_3": forms_parejas_3,
         "forms_parejas_4": forms_parejas_4,
         "forms_individual_1": forms_individual_1,
         "forms_individual_2": forms_individual_2,
         "todos": todos})

@permission_required('dardos.add_jornada')
def new_jornada (request):
    liga_actual = get_liga_actual(request)
    if liga_actual:
        liga_actual = liga_actual.id
    else:
        liga_actual = ''
    return create_object(
        request,
        form_class=JornadaForm,
        post_save_redirect='/partidos/new',
        extra_context={'liga_sesion': liga_actual})

def ajax_get_siguiente_jornada (request, liga_id):
    if request.is_ajax():
        numero = Jornada.objects.filter(liga=liga_id).aggregate(Max("numero"))["numero__max"]
        jornada = Jornada.objects.get(liga=liga_id, numero=numero)
        texto = "<b>Información:</b> La última jornada de la liga '" + str(jornada.liga.nombre) + \
            "' es la " + str(numero) + " el día " + str(jornada.fecha_prevista)
        return HttpResponse(texto)
    else:
        return HttpResponse(status=400)
        
