# -*- mode: python; tab-width: 4; indent-tabs-mode: nil -*-
# -*- coding: utf-8 -*-

from django import forms
from ..models import *

class GraficasForm(forms.Form):
    equipo = forms.IntegerField(widget=forms.HiddenInput)
    jugador = forms.IntegerField(required=False, widget=forms.HiddenInput)
    liga = forms.IntegerField(required=False, widget=forms.HiddenInput)
    
    chart_div = forms.CharField(required=False, initial="chartdivevo",
        widget=forms.HiddenInput)
    tipo_grafico = forms.ChoiceField(choices = [
        ['1','Evolución por jornadas']
        ])
    tipo_partida = forms.ChoiceField(required=False, 
        choices = ((0,"Cualquiera"),) + TIPOS_PARTIDA)
    tipo_juego = forms.ChoiceField(required=False,
        choices = ((0,"Cualquiera"),) + TIPOS_JUEGO)
    tipo_valores = forms.ChoiceField(required=False,
        choices = ((1,"Ganadas y perdidas"), (2, "Porcentaje de ganadas")) )
