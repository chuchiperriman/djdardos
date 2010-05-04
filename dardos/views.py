from djdardos.dardos.models import *
from django.shortcuts import render_to_response, get_object_or_404

from django.http import HttpResponse, Http404



# Create your views here.
def index(request):
    return render_to_response('dardos/index.html')
    
