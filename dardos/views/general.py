# -*- mode: python; tab-width: 4; indent-tabs-mode: nil -*-
# -*- coding: utf-8 -*-

from djdardos.dardos.models import *
from djdardos.dardos.general.sesiones import *
from django.db.models import Q
from django.views.generic.simple import direct_to_template
from djdardos.dardos.liga.clasificacion import *
from djdardos.dardos.general.sesiones import *
from django.core import serializers
from django.contrib import auth
from django.contrib import messages

from django.http import HttpResponse, Http404, HttpResponseRedirect


def index (request):
    current_path = "/"
    return direct_to_template(request, 'dardos/index.html')
        
def login (request):
    current_path = "/"
    if request.method == 'POST':
        """
        Guardamos los errores en messages para que el tag de login lo muestre
        """
        username = request.POST['username']
        password = request.POST['password']
        current_path = get_current_path(request)
        user = auth.authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                auth.login(request, user)
                return HttpResponseRedirect(current_path)
            else:
                messages.error(request, 'El usuario está deshabilitado',
                    extra_tags="login")
        else:
            messages.error(request, 'Usuario y contraseña no válidos',
                extra_tags="login")
    return direct_to_template(request, 'dardos/general/login.html', 
        {'current_path': current_path})
    
def logout (request):
    auth.logout(request)
    return HttpResponseRedirect('/')



