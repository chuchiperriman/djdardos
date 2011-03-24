# -*- mode: python; tab-width: 4; indent-tabs-mode: nil -*-

from django.conf.urls.defaults import *
from django.conf import settings

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', 'django.views.generic.simple.redirect_to', {'url': 'dardos/'}),
    (r'^dardos/', include('djdardos.dardos.urls.general')),
    (r'^dardos/equipos/', include('djdardos.dardos.urls.equipos')),
    (r'^dardos/jugadores/', include('djdardos.dardos.urls.jugadores')),
    (r'^dardos/partidos/', include('djdardos.dardos.urls.partidos')),
    (r'^dardos/graficas/', include('djdardos.dardos.urls.graficas')),
    (r'^dardos/ligas/', include('djdardos.dardos.urls.ligas')),
    (r'^dardos/divisiones/', include('djdardos.dardos.urls.divisiones')),
    (r'^dardos/jornadas/', include('djdardos.dardos.urls.jornadas')),

    #Media files
    (r'^site_media/(?P<path>.*)$', 'django.views.static.serve',
                 {'document_root': settings.MEDIA_ROOT}),

    # Uncomment the next line to enable the admin:
    (r'^admin/', include(admin.site.urls))
)
