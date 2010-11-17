# -*- mode: python; tab-width: 4; indent-tabs-mode: nil -*-
# -*- coding: utf-8 -*-

from djdardos.dardos.models import *
from django.db.models import Q
from django.shortcuts import render_to_response, get_object_or_404
from djdardos.dardos.liga.clasificacion import *
from django.core import serializers
from django.contrib import auth
from django.contrib import messages

from django.http import HttpResponse, Http404, HttpResponseRedirect

def cambiar_liga(request):
    request.session["liga_actual"] = request.REQUEST["liga"]
    return HttpResponseRedirect(request.REQUEST["current_path"])
    
def login (request):
    """
    Guardamos los errores en messages para que el tag de login lo muestre
    """
    username = request.POST['username']
    password = request.POST['password']
    user = auth.authenticate(username=username, password=password)
    if user is not None:
        if user.is_active:
            auth.login(request, user)
        else:
            messages.add_message(request, messages.ERROR, 'El usuario está deshabilitado',
                extra_tags="login")
    else:
        messages.add_message(request, messages.ERROR, 'Usuario y contraseña no válidos',
            extra_tags="login")
    return HttpResponseRedirect(request.REQUEST["current_path"])
