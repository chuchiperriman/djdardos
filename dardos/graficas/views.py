# -*- mode: python; tab-width: 4; indent-tabs-mode: nil -*-
# -*- coding: utf-8 -*-

from djdardos.dardos.models import *
from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponse, Http404

from ..templatetags.graficos import *
from ..equipos.estadisticas import DatosEstadisticaJugador
from ..graficas import graficas
from .forms import GraficasForm

def ajax_grafica_evolucion(request):
    #TODO ver cómo cogemos la liga
    form = GraficasForm(request.GET)
    graf = None
    if form.is_valid():
        g = graficas.GraficaJornadas(Liga.objects.get(pk=1))
        if form.cleaned_data["jugador"]:
            g.set_jugador(Jugador.objects.get(pk=form.cleaned_data["jugador"]))
        else:
            g.set_equipo(Equipo.objects.get(pk=form.cleaned_data["equipo"]))
        g.tipo_partida = int(form.cleaned_data["tipo_partida"])
        g.tipo_juego = int(form.cleaned_data["tipo_juego"])
        g.calcular()
        graf = GraficoEvolucion("Evolución por jornadas",
            form.cleaned_data["chart_div"])
        tipo_valores = int(form.cleaned_data["tipo_valores"])
        if tipo_valores == 1:
            if form.cleaned_data["jugador"]:
                graf.range_y=range(0,7)
            else:
                #Si es gráfica de equipo, pueden ganar hasta 16
                graf.range_y=range(0,17)
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

        
        
        
