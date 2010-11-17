# -*- mode: python; tab-width: 4; indent-tabs-mode: nil -*-

from djdardos.dardos.models import *

DIVISION_ACTUAL = "division_actual"
LIGA_ACTUAL = "liga_actual"

def get_liga_actual(request):
    liga_actual = None
    if LIGA_ACTUAL in request.session:
        liga_actual = Liga.objects.get(pk=request.session[LIGA_ACTUAL])
    elif DIVISION_ACTUAL in request.session:
        liga_actual = Division.objects.get(pk=request.session[DIVISION_ACTUAL]).get_liga_actual()
    return liga_actual
    
def get_current_path(request):
    if "current_path" in request.REQUEST:
        current_path = request.REQUEST["current_path"]
    else:
        current_path = request.path
    return current_path
