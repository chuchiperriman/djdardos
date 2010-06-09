from djdardos.dardos.models import *

from django import template

register = template.Library()

class DatosJornadaGP:
    def __init__(self, num_jornada, ganados, perdidos):
        self.num_jornada = num_jornada
        self.ganados = ganados
        self.perdidos = perdidos

class JornadasGrafico:
    def __init__(self,titulo, div_id="chartdiv", max_partidas = 16,
        max_jornadas = 15):
        self.titulo = titulo
        self.div_id = div_id
        self.max_partidas = max_partidas
        self.max_jornadas = max_jornadas
        self.datos = list()
    
    def get_max_x_range(self):
        return range(self.max_jornadas + 2)
        
    def get_max_y_range(self):
        if self.max_partidas <= 6:
            return range(self.max_partidas + 1)
        else:
            return range(0, self.max_partidas + 1, 2)
            
    def add_dato (self, num_jornada, ganados, perdidos):
        self.datos.append(DatosJornadaGP(num_jornada, ganados, perdidos))
        
        
@register.inclusion_tag('dardos/includes/grafico_gp_jornadas.html')
def show_grafico_gp_jornadas(jornadas_grafico):
    return {'jornadas_grafico' : jornadas_grafico}
