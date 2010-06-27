# -*- mode: python; tab-width: 4; indent-tabs-mode: nil -*-

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
        
    def save(self,partido):
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
        if cleaned_data["ganador"] == "l":
            p.ganadores.add(Jugador.objects.get(pk=cleaned_data["jugador_local"]))
            p.ganadores.add(Jugador.objects.get(pk=cleaned_data["jugador_local2"]))
        else:
            p.ganadores.add(Jugador.objects.get(pk=cleaned_data["jugador_visitante"]))
            p.ganadores.add(Jugador.objects.get(pk=cleaned_data["jugador_visitante2"]))
        p.save()
        print p.jugadores_local.all()
        
"""
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
        logging.debug("widgets:"+str(dir(self)))
        logging.debug("widgets:"+str(dir(self.instance)))
        self.cleaned_data = super(PartidoForm, self).clean()
        
        if ('jornada' in self.cleaned_data and
            'equipo_local' in self.cleaned_data and
            'equipo_visitante' in self.cleaned_data):
            
            if (self.han_jugado(self.cleaned_data['jornada'].liga, 
                self.cleaned_data['equipo_local'], self.cleaned_data['equipo_visitante'])):
                raise forms.ValidationError("Estos equipos ya han jugado")
            
            if (self.cleaned_data['equipo_local'].id == self.cleaned_data['equipo_visitante'].id):
                raise forms.ValidationError("No puedes seleccionar el mismo equipo")
            #TODO Validar que ninguno de los dos equipos hayan jugado ya la jornada indicada

        return self.cleaned_data

class PartidaIndividualForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(PartidaIndividualForm, self).__init__(*args, **kwargs)
        self.fields['numero'].widget = forms.widgets.HiddenInput()

    #TODO Mostrar solo jornadas que no tienen partido asignado
    class Meta:
        model = Partida
        exclude = ("partido", "tipo")
    
class PartidaParejasForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(PartidaParejasForm, self).__init__(*args, **kwargs)
        self.fields['numero'].widget = forms.widgets.HiddenInput()
        
    #TODO Mostrar solo jornadas que no tienen partido asignado
    class Meta:
        model = Partida
        exclude = ("partido", "tipo")

    def clean(self):
        cleaned_data = self.cleaned_data
        jugador_local1 = cleaned_data["jugador_local1"]
        jugador_local2 = cleaned_data["jugador_local2"]
        jugador_visitante1 = cleaned_data["jugador_visitante1"]
        jugador_visitante2 = cleaned_data["jugador_visitante2"]
        ganador1 = cleaned_data["ganador1"]
        ganador2 = cleaned_data["ganador2"]
        
        jugadores = [jugador_local1, jugador_local2, jugador_visitante1, jugador_visitante2]
        
        if jugador_local1 == jugador_local2:
            raise forms.ValidationError("El jugador local 1 no puede ser el mismo que el jugador local 2")
        if jugador_visitante1 == jugador_visitante2:
            raise forms.ValidationError("El jugador visitante 1 no puede ser el mismo que el jugador visitante 2")
        if ganador1 not in jugadores:
            raise forms.ValidationError("El ganador 1 ("+ganador1.nombre+") no ha jugado la partida")
        if ganador2 not in jugadores:
            raise forms.ValidationError("El ganador 2 ("+ganador2.nombre+") no ha jugado la partida")
        if ganador1 == ganador2:
            raise forms.ValidationError("El ganador 1 no puede ser el mismo que el ganador 2")
        if ganador1.equipo != ganador2.equipo:
            raise forms.ValidationError("No puede haber un ganador de cada equipo")
        return cleaned_data
"""
class JornadaForm(forms.ModelForm):
    
    def __init__(self, *args, **kwargs):
        super(JornadaForm, self).__init__(*args, **kwargs)
        self.fields['fecha_prevista'].input_formats = ('%d/%m/%Y','%d-%m-%Y')
        
    class Meta:
        model = Jornada
        
    def clean(self):
        cleaned_data = self.cleaned_data
        
        if Jornada.objects.filter(
            Q(numero=cleaned_data["numero"]) & Q(liga=cleaned_data["liga"])).count() > 0:
            raise forms.ValidationError("La fornada "+str(cleaned_data["numero"])+" de la liga "+
                str(cleaned_data["liga"])+" ya esta dada de alta "+str(cleaned_data["fecha_prevista"]))
            
        
        return cleaned_data
        
        
