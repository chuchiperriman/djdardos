# -*- mode: python; tab-width: 4; indent-tabs-mode: nil -*-

from djdardos.dardos.models import *
from django import forms
import datetime
import logging

class PartidoPreForm(forms.Form):
    
    #TODO Hacerlo con un formulario de modelo: http://docs.djangoproject.com/en/dev/topics/forms/modelforms/
    
    fecha = forms.DateField(input_formats=('%d-%m-%Y', '%d/%m/%Y'))
    jornada = forms.ModelChoiceField(queryset=Jornada.objects.filter(partido=None))
    equipo_local = forms.ModelChoiceField(queryset=Equipo.objects.all().order_by("nombre"))
    equipo_visitante = forms.ModelChoiceField(queryset=Equipo.objects.all().order_by("nombre"))
    
    def han_jugado(self,liga, equipo_local, equipo_visitante):
        num = Partido.objects.filter(Q(jornada__in=liga.jornada_set.all()) &
            Q(equipo_local=equipo_local) & 
            Q(equipo_visitante=equipo_visitante)).count()
        return num > 0
        
    def clean(self):
        cleaned_data = self.cleaned_data

        if (self.han_jugado(cleaned_data['jornada'].liga, 
            cleaned_data['equipo_local'], cleaned_data['equipo_visitante'])):
            raise forms.ValidationError("Estos equipos ya han jugado")
        
        if (cleaned_data['equipo_local'].id == cleaned_data['equipo_visitante'].id):
            raise forms.ValidationError("No puedes seleccionar el mismo equipo")
        return cleaned_data


class PartidasForm(forms.Form):
    
    #TODO Usar model forms: http://collingrady.wordpress.com/2008/02/18/editing-multiple-objects-in-django-with-newforms/
    
    par501jl1_1 = forms.ModelChoiceField(queryset=Jugador.objects.none())
    par501jl2_1 = forms.ModelChoiceField(queryset=Jugador.objects.none())
    par501jv1_1 = forms.ModelChoiceField(queryset=Jugador.objects.none())
    par501jv2_1 = forms.ModelChoiceField(queryset=Jugador.objects.none())
    par501g_1 = forms.ModelChoiceField(queryset=Equipo.objects.none())
    par501jl1_2 = forms.ModelChoiceField(queryset=Jugador.objects.none())
    par501jl2_2 = forms.ModelChoiceField(queryset=Jugador.objects.none())
    par501jv1_2 = forms.ModelChoiceField(queryset=Jugador.objects.none())
    par501jv2_2 = forms.ModelChoiceField(queryset=Jugador.objects.none())
    par501g_2 = forms.ModelChoiceField(queryset=Equipo.objects.none())
    par501jl1_3 = forms.ModelChoiceField(queryset=Jugador.objects.none())
    par501jl2_3 = forms.ModelChoiceField(queryset=Jugador.objects.none())
    par501jv1_3 = forms.ModelChoiceField(queryset=Jugador.objects.none())
    par501jv2_3 = forms.ModelChoiceField(queryset=Jugador.objects.none())
    par501g_3 = forms.ModelChoiceField(queryset=Equipo.objects.none())
    par501jl1_4 = forms.ModelChoiceField(queryset=Jugador.objects.none())
    par501jl2_4 = forms.ModelChoiceField(queryset=Jugador.objects.none())
    par501jv1_4 = forms.ModelChoiceField(queryset=Jugador.objects.none())
    par501jv2_4 = forms.ModelChoiceField(queryset=Jugador.objects.none())
    par501g_4 = forms.ModelChoiceField(queryset=Equipo.objects.none())
    
    ind501jl1_1 = forms.ModelChoiceField(queryset=Jugador.objects.none())
    ind501jv1_1 = forms.ModelChoiceField(queryset=Jugador.objects.none())
    ind501g_1 = forms.ModelChoiceField(queryset=Equipo.objects.none())
    ind501jl1_2 = forms.ModelChoiceField(queryset=Jugador.objects.none())
    ind501jv1_2 = forms.ModelChoiceField(queryset=Jugador.objects.none())
    ind501g_2 = forms.ModelChoiceField(queryset=Equipo.objects.none())
    ind501jl1_3 = forms.ModelChoiceField(queryset=Jugador.objects.none())
    ind501jv1_3 = forms.ModelChoiceField(queryset=Jugador.objects.none())
    ind501g_3 = forms.ModelChoiceField(queryset=Equipo.objects.none())
    ind501jl1_4 = forms.ModelChoiceField(queryset=Jugador.objects.none())
    ind501jv1_4 = forms.ModelChoiceField(queryset=Jugador.objects.none())
    ind501g_4 = forms.ModelChoiceField(queryset=Equipo.objects.none())
    
    parcrijl1_1 = forms.ModelChoiceField(queryset=Jugador.objects.none())
    parcrijl2_1 = forms.ModelChoiceField(queryset=Jugador.objects.none())
    parcrijv1_1 = forms.ModelChoiceField(queryset=Jugador.objects.none())
    parcrijv2_1 = forms.ModelChoiceField(queryset=Jugador.objects.none())
    parcrig_1 = forms.ModelChoiceField(queryset=Equipo.objects.none())
    parcrijl1_2 = forms.ModelChoiceField(queryset=Jugador.objects.none())
    parcrijl2_2 = forms.ModelChoiceField(queryset=Jugador.objects.none())
    parcrijv1_2 = forms.ModelChoiceField(queryset=Jugador.objects.none())
    parcrijv2_2 = forms.ModelChoiceField(queryset=Jugador.objects.none())
    parcrig_2 = forms.ModelChoiceField(queryset=Equipo.objects.none())
    parcrijl1_3 = forms.ModelChoiceField(queryset=Jugador.objects.none())
    parcrijl2_3 = forms.ModelChoiceField(queryset=Jugador.objects.none())
    parcrijv1_3 = forms.ModelChoiceField(queryset=Jugador.objects.none())
    parcrijv2_3 = forms.ModelChoiceField(queryset=Jugador.objects.none())
    parcrig_3 = forms.ModelChoiceField(queryset=Equipo.objects.none())
    parcrijl1_4 = forms.ModelChoiceField(queryset=Jugador.objects.none())
    parcrijl2_4 = forms.ModelChoiceField(queryset=Jugador.objects.none())
    parcrijv1_4 = forms.ModelChoiceField(queryset=Jugador.objects.none())
    parcrijv2_4 = forms.ModelChoiceField(queryset=Jugador.objects.none())
    parcrig_4 = forms.ModelChoiceField(queryset=Equipo.objects.none())
    
    ind501jl1_5 = forms.ModelChoiceField(queryset=Jugador.objects.none())
    ind501jv1_5 = forms.ModelChoiceField(queryset=Jugador.objects.none())
    ind501g_5 = forms.ModelChoiceField(queryset=Equipo.objects.none())
    ind501jl1_6 = forms.ModelChoiceField(queryset=Jugador.objects.none())
    ind501jv1_6 = forms.ModelChoiceField(queryset=Jugador.objects.none())
    ind501g_6 = forms.ModelChoiceField(queryset=Equipo.objects.none())
    ind501jl1_7 = forms.ModelChoiceField(queryset=Jugador.objects.none())
    ind501jv1_7 = forms.ModelChoiceField(queryset=Jugador.objects.none())
    ind501g_7 = forms.ModelChoiceField(queryset=Equipo.objects.none())
    ind501jl1_8 = forms.ModelChoiceField(queryset=Jugador.objects.none())
    ind501jv1_8 = forms.ModelChoiceField(queryset=Jugador.objects.none())
    ind501g_8 = forms.ModelChoiceField(queryset=Equipo.objects.none())
    
    def __init__(self, partido_id, *args, **kwargs):
        partido = Partido.objects.get(pk=partido_id)
        equipo_local = partido.equipo_local
        equipo_visitante = partido.equipo_visitante
        
        super(PartidasForm, self).__init__(*args, **kwargs)
        
        self.fields['par501jl1_1'].queryset = equipo_local.jugador_set.all()
        self.fields['par501jl2_1'].queryset = equipo_local.jugador_set.all()
        self.fields['par501jv1_1'].queryset = equipo_visitante.jugador_set.all()
        self.fields['par501jv2_1'].queryset = equipo_visitante.jugador_set.all()
        self.fields['par501g_1'].queryset = Equipo.objects.filter(pk__in=[equipo_local.id, equipo_visitante.id])
        self.fields['par501jl1_2'].queryset = equipo_local.jugador_set.all()
        self.fields['par501jl2_2'].queryset = equipo_local.jugador_set.all()
        self.fields['par501jv1_2'].queryset = equipo_visitante.jugador_set.all()
        self.fields['par501jv2_2'].queryset = equipo_visitante.jugador_set.all()
        self.fields['par501g_2'].queryset = Equipo.objects.filter(pk__in=[equipo_local.id, equipo_visitante.id])
        self.fields['par501jl1_3'].queryset = equipo_local.jugador_set.all()
        self.fields['par501jl2_3'].queryset = equipo_local.jugador_set.all()
        self.fields['par501jv1_3'].queryset = equipo_visitante.jugador_set.all()
        self.fields['par501jv2_3'].queryset = equipo_visitante.jugador_set.all()
        self.fields['par501g_3'].queryset = Equipo.objects.filter(pk__in=[equipo_local.id, equipo_visitante.id])
        self.fields['par501jl1_4'].queryset = equipo_local.jugador_set.all()
        self.fields['par501jl2_4'].queryset = equipo_local.jugador_set.all()
        self.fields['par501jv1_4'].queryset = equipo_visitante.jugador_set.all()
        self.fields['par501jv2_4'].queryset = equipo_visitante.jugador_set.all()
        self.fields['par501g_4'].queryset = Equipo.objects.filter(pk__in=[equipo_local.id, equipo_visitante.id])
        
        self.fields['ind501jl1_1'].queryset = equipo_local.jugador_set.all()
        self.fields['ind501jv1_1'].queryset = equipo_visitante.jugador_set.all()
        self.fields['ind501g_1'].queryset = Equipo.objects.filter(pk__in=[equipo_local.id, equipo_visitante.id])
        self.fields['ind501jl1_2'].queryset = equipo_local.jugador_set.all()
        self.fields['ind501jv1_2'].queryset = equipo_visitante.jugador_set.all()
        self.fields['ind501g_2'].queryset = Equipo.objects.filter(pk__in=[equipo_local.id, equipo_visitante.id])
        self.fields['ind501jl1_3'].queryset = equipo_local.jugador_set.all()
        self.fields['ind501jv1_3'].queryset = equipo_visitante.jugador_set.all()
        self.fields['ind501g_3'].queryset = Equipo.objects.filter(pk__in=[equipo_local.id, equipo_visitante.id])
        self.fields['ind501jl1_4'].queryset = equipo_local.jugador_set.all()
        self.fields['ind501jv1_4'].queryset = equipo_visitante.jugador_set.all()
        self.fields['ind501g_4'].queryset = Equipo.objects.filter(pk__in=[equipo_local.id, equipo_visitante.id])
        
        self.fields['parcrijl1_1'].queryset = equipo_local.jugador_set.all()
        self.fields['parcrijl2_1'].queryset = equipo_local.jugador_set.all()
        self.fields['parcrijv1_1'].queryset = equipo_visitante.jugador_set.all()
        self.fields['parcrijv2_1'].queryset = equipo_visitante.jugador_set.all()
        self.fields['parcrig_1'].queryset = Equipo.objects.filter(pk__in=[equipo_local.id, equipo_visitante.id])
        self.fields['parcrijl1_2'].queryset = equipo_local.jugador_set.all()
        self.fields['parcrijl2_2'].queryset = equipo_local.jugador_set.all()
        self.fields['parcrijv1_2'].queryset = equipo_visitante.jugador_set.all()
        self.fields['parcrijv2_2'].queryset = equipo_visitante.jugador_set.all()
        self.fields['parcrig_2'].queryset = Equipo.objects.filter(pk__in=[equipo_local.id, equipo_visitante.id])
        self.fields['parcrijl1_3'].queryset = equipo_local.jugador_set.all()
        self.fields['parcrijl2_3'].queryset = equipo_local.jugador_set.all()
        self.fields['parcrijv1_3'].queryset = equipo_visitante.jugador_set.all()
        self.fields['parcrijv2_3'].queryset = equipo_visitante.jugador_set.all()
        self.fields['parcrig_3'].queryset = Equipo.objects.filter(pk__in=[equipo_local.id, equipo_visitante.id])
        self.fields['parcrijl1_4'].queryset = equipo_local.jugador_set.all()
        self.fields['parcrijl2_4'].queryset = equipo_local.jugador_set.all()
        self.fields['parcrijv1_4'].queryset = equipo_visitante.jugador_set.all()
        self.fields['parcrijv2_4'].queryset = equipo_visitante.jugador_set.all()
        self.fields['parcrig_4'].queryset = Equipo.objects.filter(pk__in=[equipo_local.id, equipo_visitante.id])
        
        self.fields['ind501jl1_5'].queryset = equipo_local.jugador_set.all()
        self.fields['ind501jv1_5'].queryset = equipo_visitante.jugador_set.all()
        self.fields['ind501g_5'].queryset = Equipo.objects.filter(pk__in=[equipo_local.id, equipo_visitante.id])
        self.fields['ind501jl1_6'].queryset = equipo_local.jugador_set.all()
        self.fields['ind501jv1_6'].queryset = equipo_visitante.jugador_set.all()
        self.fields['ind501g_6'].queryset = Equipo.objects.filter(pk__in=[equipo_local.id, equipo_visitante.id])
        self.fields['ind501jl1_7'].queryset = equipo_local.jugador_set.all()
        self.fields['ind501jv1_7'].queryset = equipo_visitante.jugador_set.all()
        self.fields['ind501g_7'].queryset = Equipo.objects.filter(pk__in=[equipo_local.id, equipo_visitante.id])
        self.fields['ind501jl1_8'].queryset = equipo_local.jugador_set.all()
        self.fields['ind501jv1_8'].queryset = equipo_visitante.jugador_set.all()
        self.fields['ind501g_8'].queryset = Equipo.objects.filter(pk__in=[equipo_local.id, equipo_visitante.id])
        
    def clean(self):
        cleaned_data = self.cleaned_data

        #TODO Comprobar que la pareja no sea la misma
        #TODO Comprobar que una pareja del grupo 1 no puede jugar en el grupo 2
        return cleaned_data
