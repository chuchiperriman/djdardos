from django.conf.urls.defaults import *

urlpatterns = patterns('djdardos.dardos.views.jugadores',
    url(r'^$', 'index', name='dardos-jugadores-index'),
    url(r'^(?P<jugador_id>\d+)/$', 'detail',
        name='dardos-jugadores-detail'),
)
