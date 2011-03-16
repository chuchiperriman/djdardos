from django.conf.urls.defaults import *

urlpatterns = patterns('djdardos.dardos.views.equipos',
    url(r'^$', 'index', name='dardos-equipos-index'),
    url(r'^estreport/(?P<equipo_id>\d+)/(?P<liga_id>\d+)$',
        'estreport', name='dardos-equipos-estreport'),
    url(r'^estparejas/(?P<equipo_id>\d+)/(?P<liga_id>\d+)$',
        'ajax_estadistica_parejas', name='dardos-equipos-estparejas'),
    url(r'^(?P<equipo_id>\d+)/$', 'detail', 
        name='dardos-equipos-detail'),
    url(r'^ajax_equipos_from_liga/$',
        'ajax_equipos_from_liga',
        name='dardos-equipos-ajax_equipos_from_liga'),
)
