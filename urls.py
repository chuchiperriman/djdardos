# -*- mode: python; tab-width: 4; indent-tabs-mode: nil -*-

from django.conf.urls.defaults import *
from django.conf import settings


# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    (r'^equipos$', 'djbolos.bolos.equipos.views.index'),
    (r'^equipos/(?P<equipo_id>\d+)/$', 'djbolos.bolos.equipos.views.detail'),
    (r'^jugadores$', 'djbolos.bolos.jugadores.views.index'),
    (r'^jugadores/(?P<jugador_id>\d+)/$', 'djbolos.bolos.jugadores.views.detail'),
    (r'^partidos$', 'djbolos.bolos.partidos.views.index'),
    (r'^partidos/new$', 'djbolos.bolos.partidos.views.new'),
    (r'^partidos/prenew$', 'djbolos.bolos.partidos.views.prenew'),
    (r'^partidos/(?P<partido_id>\d+)/$', 'djbolos.bolos.partidos.views.detail'),
    # Example:
    # (r'^djbolos/', include('djbolos.foo.urls')),

    # Uncomment the admin/doc line below and add 'django.contrib.admindocs' 
    # to INSTALLED_APPS to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    #Media files
    (r'^site_media/(?P<path>.*)$', 'django.views.static.serve',
                 {'document_root': settings.MEDIA_ROOT}),

    # Uncomment the next line to enable the admin:
    (r'^admin/', include(admin.site.urls))
)
