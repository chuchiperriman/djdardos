# -*- mode: python; tab-width: 4; indent-tabs-mode: nil -*-
from djdardos.dardos.models import *
from django.shortcuts import render_to_response, get_object_or_404

from django.http import HttpResponse, Http404
from django.views.generic import date_based, list_detail
from django.conf import settings
from django.views.generic.simple import direct_to_template
from djdardos.basic.blog.models import *


def ligas_index(request, **kwargs):
    divisiones = Division.objects.all()
    return direct_to_template(request, 'dardos/divisiones/index.html',
        {'divisiones' : divisiones})
        
