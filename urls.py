# -*- mode: python; tab-width: 4; indent-tabs-mode: nil -*-

from django.conf.urls.defaults import *
from django.conf import settings


# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', 'djdardos.basic.blog.views.post_list'),
    (r'^ligas/$', 'djdardos.dardos.views.ligas_index'),
    (r'^login/$', 'djdardos.dardos.general.views.login'),
    (r'^logout/$', 'djdardos.dardos.general.views.logout'),
    (r'^equipos/$', 'djdardos.dardos.equipos.views.index'),
    (r'^equipos/estreport/(?P<equipo_id>\d+)/(?P<liga_id>\d+)$', 'djdardos.dardos.equipos.views.estreport'),
    (r'^equipos/estparejas/(?P<equipo_id>\d+)/(?P<liga_id>\d+)$', 'djdardos.dardos.equipos.views.ajax_estadistica_parejas'),
    (r'^equipos/(?P<equipo_id>\d+)/$', 'djdardos.dardos.equipos.views.detail'),
    (r'^jugadores/$', 'djdardos.dardos.jugadores.views.index'),
    (r'^jugadores/(?P<jugador_id>\d+)/$', 'djdardos.dardos.jugadores.views.detail'),
    (r'^partidos/$', 'djdardos.dardos.partidos.views.index'),
    (r'^partidos/(?P<partido_id>\d+)/$', 'djdardos.dardos.partidos.views.detail'),
    (r'^partidos/new/$', 'djdardos.dardos.partidos.views.new'),
    (r'^partidos/partidas/(?P<partido_id>\d+)/$', 'djdardos.dardos.partidos.views.setpartidas'),
    (r'^partidos/new_jornada/$', 'djdardos.dardos.partidos.views.new_jornada'),
    (r'^division/(?P<division_id>\d+)/$', 'djdardos.dardos.divisiones.views.detail'),
    (r'^ajax_jornada_detail/(?P<jornada_id>\d+)/$', 'djdardos.dardos.divisiones.views.ajax_jornada_detail'),
    (r'^ajax_grafica_evolucion/(?P<liga_id>\d+)/$', 'djdardos.dardos.graficas.views.ajax_grafica_evolucion'),
    (r'^liga/(?P<liga_id>\d+)/ajax_get_siguiente_jornada/$', 'djdardos.dardos.partidos.views.ajax_get_siguiente_jornada'),
    (r'^comments/', include('django.contrib.comments.urls')),
    (r'^blog/', include('basic.blog.urls')),
    url(r'^post/(?P<year>\d{4})/(?P<month>\w{3})/(?P<day>\d{1,2})/(?P<slug>[-\w]+)/$',
        view='djdardos.dardos.views.post_detail',
        name='blog_detail'
    ),
    (r'^pruebas/$', 'djdardos.dardos.pruebas.views.index'),
    (r'^cambiar_liga/$', 'djdardos.dardos.general.views.cambiar_liga'),
    # Uncomment the admin/doc line below and add 'django.contrib.admindocs' 
    # to INSTALLED_APPS to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    #Media files
    (r'^site_media/(?P<path>.*)$', 'django.views.static.serve',
                 {'document_root': settings.MEDIA_ROOT}),

    # Uncomment the next line to enable the admin:
    (r'^admin/', include(admin.site.urls))
)
