# -*- mode: python; tab-width: 4; indent-tabs-mode: nil -*-
# -*- coding: utf-8 -*-

from djdardos.dardos.models import *
from django.db.models import Max
from djdardos.dardos.partidos.forms import *
from ..general.sesiones import *
from django.shortcuts import render_to_response, get_object_or_404

from django.http import HttpResponse, Http404


