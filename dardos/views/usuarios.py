# -*- mode: python; tab-width: 4; indent-tabs-mode: nil -*-
# -*- coding: utf-8 -*-

from djdardos.dardos.models import *
from djdardos.mb.models import *
from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponse, Http404
from django.views.generic.simple import direct_to_template
from django.contrib.auth.decorators import login_required
from django.contrib.contenttypes.models import ContentType

def home(request):
    ct = ContentType.objects.get_for_model(request.user)
    following = Following.objects.filter(follower_content_type=ct, follower_object_id=request.user.id)

    return direct_to_template(request, 'dardos/usuarios/home.html', {
            'following': following})

home = login_required(home)
