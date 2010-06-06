from djdardos.dardos.models import *

from django import template

register = template.Library()

class DatosJornadaGP:
    def __init__(self, num_jornada, ganados, perdidos):
        self.num_jornada = num_jornada
        self.ganados = ganados
        self.perdidos = perdidos

class JornadasGrafico:
    def __init__(self,titulo, div_id="chartdiv"):
        self.titulo = titulo
        self.div_id = div_id
        self.datos = list()
        
    def add_dato (self, num_jornada, ganados, perdidos):
        self.datos.append(DatosJornadaGP(num_jornada, ganados, perdidos))
        
        
@register.inclusion_tag('dardos/includes/grafico_gp_jornadas.html')
def show_grafico_gp_jornadas(jornadas_grafico):
    return {'jornadas_grafico' : jornadas_grafico}
