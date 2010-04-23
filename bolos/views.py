from djbolos.bolos.models import *
from django.shortcuts import render_to_response, get_object_or_404

from django.http import HttpResponse, Http404



# Create your views here.
def index(request):
    jugadores_list = Jugador.objects.all().order_by('nombre')[:5]
    return render_to_response('bolos/jugadores/index.html', {'jugadores_list': jugadores_list})

def detail(request, jugador_id):
    p = get_object_or_404(Jugador, pk=jugador_id)
    return render_to_response('bolos/jugadores/detail.html', {'jugador': p})
    
