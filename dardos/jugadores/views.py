# -*- mode: python; tab-width: 4; indent-tabs-mode: nil -*-
# -*- coding: utf-8 -*-

from djdardos.dardos.models import *
from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponse, Http404

from ..templatetags.graficos import *
from ..equipos.estadisticas import DatosEstadisticaJugador
from ..graficas import graficas
from .forms import GraficasForm

# Create your views here.
def index(request):
    if 'q' in request.GET:
        jugadores_list = Jugador.objects.filter(
            nombre__contains=request.GET["q"]).order_by('equipo', 'nombre')
    else:
        jugadores_list = Jugador.objects.all().order_by('equipo', 'nombre')
    return render_to_response('dardos/jugadores/index.html', {'jugadores_list': jugadores_list})

def detail(request, jugador_id):
    jugador = get_object_or_404(Jugador, pk=jugador_id)
    jugador_datos = DatosEstadisticaJugador(jugador)
    ordenado = {}
    
    for p in jugador.partidas_ganadas():
        if not p.partido.jornada.numero in ordenado:
            ordenado[p.partido.jornada.numero] = DatosJornadaGP(
                p.partido.jornada.numero, 1, 0)
        else:
            ordenado[p.partido.jornada.numero].ganados += 1

    for p in jugador.partidas_perdidas():
        if not p.partido.jornada.numero in ordenado:
            ordenado[p.partido.jornada.numero] = DatosJornadaGP(
                p.partido.jornada.numero, 0, 1)
        else:
            ordenado[p.partido.jornada.numero].perdidos += 1
    
    jornadas_grafico = JornadasGrafico(u'Evolución de partidas ganadas/perdidas')
    jornadas_grafico.max_partidas = 6
    jornadas_grafico.max_jornadas = 15

    for k in ordenado:
        jornadas_grafico.datos.append(ordenado[k])

    graficas_form = GraficasForm()
    graficas_form.fields["jugador"].initial = jugador.id
    return render_to_response('dardos/jugadores/detail.html', {
        'jugador': jugador,
        'jugador_datos': jugador_datos,
        'jornadas_grafico' : jornadas_grafico,
        'graficas_form' : graficas_form})
        
def ajax_grafica_evolucion(request):
    #TODO ver cómo cogemos la liga
    form = GraficasForm(request.GET)
    graf = None
    if form.is_valid():
        g = graficas.GraficaJornadas(Liga.objects.get(pk=1))
        g.set_jugador(Jugador.objects.get(pk=form.cleaned_data["jugador"]))
        g.tipo_partida = int(form.cleaned_data["tipo_partida"])
        g.tipo_juego = int(form.cleaned_data["tipo_juego"])
        g.calcular()
        graf = GraficoEvolucion("Evolución por jornadas",
            form.cleaned_data["chart_div"])
        tipo_valores = int(form.cleaned_data["tipo_valores"])
        if tipo_valores == 1:
            graf.range_y=range(0,7)
            l = LineaGrafico("Ganadas")
            l2 = LineaGrafico("Perdidas")
            for v in g.valores:
                l.datos.append(DatoGrafico(v["jornada"].numero, v["ganadas"]))
                l2.datos.append(DatoGrafico(v["jornada"].numero, v["perdidas"]))
            graf.add_linea(l)
            graf.add_linea(l2)
        elif tipo_valores == 2:
            graf.range_y=range(0,110,10)
            l = LineaGrafico("Porcentaje ganadas")
            for v in g.valores:
                l.datos.append(DatoGrafico(v["jornada"].numero, v["porcentaje"]))
            graf.add_linea(l)
    return render_to_response('dardos/includes/grafico_evolucion.html', 
    	{'grafico_evolucion': graf})

        
        
        
