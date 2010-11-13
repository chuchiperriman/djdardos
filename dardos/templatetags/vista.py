# -*- mode: python; tab-width: 4; indent-tabs-mode: nil -*-

from djdardos.dardos.models import *
from djdardos.dardos.general.sesiones import *

from django import template

register = template.Library()

@register.inclusion_tag('dardos/vista/display_divliga_actual.html', takes_context = True)
def display_divliga_actual(context):
    liga_actual = None
    request = context['request']
    if LIGA_ACTUAL in request.session:
        #TODO Igual mejor guardar el nombre para no ir a bbdd
        liga_actual = Liga.objects.get(pk=request.session["liga_actual"])
        
    return {'liga_actual': liga_actual,
        'current_path': request.path}

@register.inclusion_tag('dardos/vista/menu_superior.html', takes_context = True)
def display_menu_superior(context):
    menu_superior = {"general":Opcion("General", "/"), 
        "ligas" : Opcion("Ligas","/ligas")}
        
    request = context['request']
    if request.path.startswith("/ligas"):
        menu_superior["ligas"].seleccionado = True
    else:
        menu_superior["general"].seleccionado = True
        
    return {'menu_superior': menu_superior}
        
class Opcion:
    def __init__(self, nombre, url):
        self.nombre = nombre
        self.url = url
        self.seleccionado = False
        

