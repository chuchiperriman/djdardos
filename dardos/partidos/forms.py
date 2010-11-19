# -*- mode: python; tab-width: 4; indent-tabs-mode: nil -*-
# -*- coding: utf-8 -*-

from djdardos.dardos.models import *
from django import forms
import datetime
import logging

class PartidaIndividualForm(forms.Form):
    tipo_partida = "individual"
    numero = forms.IntegerField(widget=forms.HiddenInput())
    jugador_local = forms.IntegerField(widget=forms.Select())
    jugador_visitante = forms.IntegerField(widget=forms.Select())
    #l local y v visitante
    ganador = forms.CharField(
        widget=forms.RadioSelect(
            choices=(("l", "Local"), ("v", "Visitante"))
            ),
        initial = "l"
        )
        
    def load(self, partida):
        self.fields["jugador_local"].initial = partida.jugadores_local.all()[0].id
        self.fields["jugador_visitante"].initial = partida.jugadores_visitante.all()[0].id
        if partida.ganadores.all()[0].id == self.fields["jugador_local"].initial:
            self.fields["ganador"].initial = "l"
        else:
            self.fields["ganador"].initial = "v"
        
    def save(self, partido):
        cleaned_data = self.cleaned_data
        p = Partida()
        p.numero = cleaned_data["numero"]
        p.partido = partido
        p.tipo = TIPO_PARTIDA_INDIVIDUAL
        p.tipo_juego = TIPO_JUEGO_501
        p.save()
        p.jugadores_local.add(Jugador.objects.get(pk=cleaned_data["jugador_local"]))
        p.jugadores_visitante.add(Jugador.objects.get(pk=cleaned_data["jugador_visitante"]))
        if cleaned_data["ganador"] == "l":
            p.ganadores.add(Jugador.objects.get(pk=cleaned_data["jugador_local"]))
        else:
            p.ganadores.add(Jugador.objects.get(pk=cleaned_data["jugador_visitante"]))
        p.save()
        print p

class PartidaParejasForm(PartidaIndividualForm):
    tipo_partida = "parejas"
    jugador_local2 = forms.IntegerField(widget=forms.Select())
    jugador_visitante2 = forms.IntegerField(widget=forms.Select())
    tipo_juego = forms.IntegerField(widget=forms.HiddenInput())
    
    def load(self, partida):
        locales = partida.jugadores_local.all()
        visitantes = partida.jugadores_visitante.all()
        ganadores = partida.ganadores.all()
        self.fields["jugador_local"].initial = locales[0].id
        self.fields["jugador_local2"].initial = locales[1].id
        self.fields["jugador_visitante"].initial = visitantes[0].id
        self.fields["jugador_visitante2"].initial = visitantes[1].id
        local = False
        for l in locales:
            if l.id == ganadores[0].id:
                local = True
                break
        if local:
            self.fields["ganador"].initial = "l"
        else:
            self.fields["ganador"].initial = "v"
    
    def clean(self):
        cleaned_data = self.cleaned_data
        jugador_local1 = cleaned_data["jugador_local"]
        jugador_local2 = cleaned_data["jugador_local2"]
        jugador_visitante1 = cleaned_data["jugador_visitante"]
        jugador_visitante2 = cleaned_data["jugador_visitante2"]
        
        if jugador_local1 == jugador_local2:
            raise forms.ValidationError("El jugador local 1 no puede ser el mismo que el jugador local 2")
        if jugador_visitante1 == jugador_visitante2:
            raise forms.ValidationError("El jugador visitante 1 no puede ser el mismo que el jugador visitante 2")
        return cleaned_data
        
    def save(self,partido):
        cleaned_data = self.cleaned_data
        p = Partida()
        p.numero = cleaned_data["numero"]
        p.partido = partido
        p.tipo = TIPO_PARTIDA_PAREJAS
        p.tipo_juego = cleaned_data["tipo_juego"]
        p.save()
        print cleaned_data["jugador_local"]
        print cleaned_data["jugador_local2"]
        p.jugadores_local.add(Jugador.objects.get(pk=cleaned_data["jugador_local"]))
        p.jugadores_local.add(Jugador.objects.get(pk=cleaned_data["jugador_local2"]))
        p.jugadores_visitante.add(Jugador.objects.get(pk=cleaned_data["jugador_visitante"]))
        p.jugadores_visitante.add(Jugador.objects.get(pk=cleaned_data["jugador_visitante2"]))
        
        if cleaned_data["jugador_local"] == cleaned_data["jugador_local2"]:
            raise forms.ValidationError("El jugador local 1 no puede ser el mismo que el jugador local 2")
        if cleaned_data["jugador_visitante"] == cleaned_data["jugador_visitante2"]:
            raise forms.ValidationError("El jugador visitante 1 no puede ser el mismo que el jugador visitante 2")
            
        if cleaned_data["ganador"] == "l":
            p.ganadores.add(Jugador.objects.get(pk=cleaned_data["jugador_local"]))
            p.ganadores.add(Jugador.objects.get(pk=cleaned_data["jugador_local2"]))
        else:
            p.ganadores.add(Jugador.objects.get(pk=cleaned_data["jugador_visitante"]))
            p.ganadores.add(Jugador.objects.get(pk=cleaned_data["jugador_visitante2"]))
        
        p.save()
        print p.jugadores_local.all()
        
class PartidoForm(forms.ModelForm):
    #TODO Mostrar solo jornadas que no tienen partido asignado
    class Meta:
        model = Partido

    def han_jugado(self,liga, equipo_local, equipo_visitante):
        num = Partido.objects.filter(Q(jornada__in=liga.jornada_set.all()) &
            Q(equipo_local=equipo_local) & 
            Q(equipo_visitante=equipo_visitante)).count()
        return num > 0
    
    def clean(self):
        self.cleaned_data = super(PartidoForm, self).clean()
        
        if ('jornada' in self.cleaned_data and
            'equipo_local' in self.cleaned_data and
            'equipo_visitante' in self.cleaned_data):
            
            if (self.cleaned_data['equipo_local'].id == self.cleaned_data['equipo_visitante'].id):
                raise forms.ValidationError("No puedes seleccionar el mismo equipo")
            #TODO Validar que ninguno de los dos equipos hayan jugado ya la jornada indicada

        return self.cleaned_data

class JornadaForm(forms.ModelForm):
    
    def __init__(self, *args, **kwargs):
        super(JornadaForm, self).__init__(*args, **kwargs)
        self.fields['fecha_prevista'].input_formats = ('%d/%m/%Y','%d-%m-%Y')
        
    class Meta:
        model = Jornada
        
    def clean(self):
        cleaned_data = self.cleaned_data
        if self.is_valid():
            if cleaned_data["numero"] < 1:
                raise forms.ValidationError("El número de jornada tiene que ser mayor de cero")
            if Jornada.objects.filter(
                Q(numero=cleaned_data["numero"]) & Q(liga=cleaned_data["liga"])).count() > 0:
                raise forms.ValidationError("La fornada "+str(cleaned_data["numero"])+" de la liga "+
                    str(cleaned_data["liga"])+" ya esta dada de alta")
            
        
        return cleaned_data
        
        
