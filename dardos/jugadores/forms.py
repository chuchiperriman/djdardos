# -*- mode: python; tab-width: 4; indent-tabs-mode: nil -*-
# -*- coding: utf-8 -*-

from django import forms
from ..models import *

class GraficasForm(forms.Form):
    jugador = forms.IntegerField(widget=forms.HiddenInput)
    tipo_grafico = forms.ChoiceField(choices = [
        ['1','Evolución']
        ])
    tipo_partida = forms.ChoiceField(choices = TIPOS_PARTIDA)
    tipo_valor = forms.ChoiceField(choices = TIPOS_JUEGO)
