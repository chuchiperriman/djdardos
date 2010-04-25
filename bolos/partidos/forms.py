# -*- mode: python; tab-width: 4; indent-tabs-mode: nil -*-

from djbolos.bolos.models import *
from django import forms

class PartidoPreForm(forms.Form):
    equipo_local = forms.ModelChoiceField(queryset=Equipo.objects.all().order_by("nombre"))
    equipo_visitante = forms.ModelChoiceField(queryset=Equipo.objects.all().order_by("nombre"))

class PartidoForm(forms.Form):
    """def __init__(self, equipo_local, equipo_visitante):
        self.equipo_local = equipo_local
        self.equipo_visitante = equipo_visitante
        self.jugadores_local = self.equipo_local.jugador_set.all()
        self.jugadores_visitantes = self.equipo_visitante.jugador_set.all()
        
        self.jugador_local = forms.ModelChoiceField(queryset=self.jugadores_local)
        self.jugador_visitante = forms.ModelChoiceField(queryset=self.jugadores_visitantes)
    """    
    jugador_local = forms.ModelChoiceField(queryset=Jugador.objects.none())
    jugador_visitante = forms.ModelChoiceField(queryset=Jugador.objects.none())
    
    def __init__(self, equipo_local, equipo_visitante, *args, **kwargs):
        super(PartidoForm, self).__init__(*args, **kwargs)
        
        self.fields['jugador_local'].queryset = equipo_local.jugador_set.all()
        self.fields['jugador_visitante'].queryset = equipo_visitante.jugador_set.all()
