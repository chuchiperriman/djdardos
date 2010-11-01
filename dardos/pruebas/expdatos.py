from dardos.models import *
from django.core import serializers

def serialize (objeto):
    out = open("/tmp/" + objeto.__name__ + ".xml" , "w")
    data = serializers.serialize("xml", objeto.objects.all(), stream=out)
    
serialize (Division)
serialize(Liga)
serialize(Jornada)
serialize(Equipo)
serialize(Jugador)
serialize(Partido)
serialize(Partida)
