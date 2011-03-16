from django.conf.urls.defaults import *

urlpatterns = patterns('djdardos.dardos.views.jornadas',
    url(r'^ajax_jornada_detail/$', 
        'ajax_jornada_detail', 
        name='dardos-jornadas-ajax_jornada_detail'),
    url(r'^ajax_jornadas_from_liga/$',
        'ajax_jornadas_from_liga',
        name='dardos-maestros-ajax_jornadas_from_liga'),
)
