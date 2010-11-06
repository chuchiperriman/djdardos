# -*- mode: python; tab-width: 4; indent-tabs-mode: nil -*-

from djdardos.dardos.models import *
from django.db.models import Q
from django.shortcuts import render_to_response, get_object_or_404
from djdardos.dardos.liga.clasificacion import *
from django.core import serializers

from django.http import HttpResponse, Http404, HttpResponseRedirect

def cambiar_liga(request):
    print request.session.get("liga_actual", "nada")
    request.session["liga_actual"] = request.REQUEST["liga"]
    return HttpResponseRedirect(request.REQUEST["current_path"])
    
