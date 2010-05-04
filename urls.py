# -*- mode: python; tab-width: 4; indent-tabs-mode: nil -*-

from django.conf.urls.defaults import *
from django.conf import settings


# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    (r'^$', 'djdardos.dardos.views.index'),
    (r'^equipos$', 'djdardos.dardos.equipos.views.index'),
    (r'^equipos/(?P<equipo_id>\d+)/$', 'djdardos.dardos.equipos.views.detail'),
    (r'^jugadores$', 'djdardos.dardos.jugadores.views.index'),
    (r'^jugadores/(?P<jugador_id>\d+)/$', 'djdardos.dardos.jugadores.views.detail'),
    (r'^partidos$', 'djdardos.dardos.partidos.views.index'),
    (r'^partidos/new$', 'djdardos.dardos.partidos.views.new'),
    (r'^partidos/prenew$', 'djdardos.dardos.partidos.views.prenew'),
    (r'^partidos/(?P<partido_id>\d+)/$', 'djdardos.dardos.partidos.views.detail'),
    # Example:
    # (r'^djdardos/', include('djdardos.foo.urls')),

    # Uncomment the admin/doc line below and add 'django.contrib.admindocs' 
    # to INSTALLED_APPS to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    #Media files
    (r'^site_media/(?P<path>.*)$', 'django.views.static.serve',
                 {'document_root': settings.MEDIA_ROOT}),

    # Uncomment the next line to enable the admin:
    (r'^admin/', include(admin.site.urls))
)
