from djbolos.bolos.models import *
from django import forms

class PartidoPreForm(forms.Form):
    equipo_local = forms.ModelChoiceField(queryset=Equipo.objects.all().order_by("nombre"))
    equipo_visitante = forms.ModelChoiceField(queryset=Equipo.objects.all().order_by("nombre"))

class PartidoForm(forms.Form):
    equipo_local = forms.ModelChoiceField(queryset=Equipo.objects.all().order_by("nombre"))
    equipo_visitante = forms.ModelChoiceField(queryset=Equipo.objects.all().order_by("nombre"))
