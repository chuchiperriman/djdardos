from django.conf.urls.defaults import *

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    (r'^jugadores$', 'djbolos.bolos.jugadores.views.index'),
    (r'^jugadores/(?P<jugador_id>\d+)/$', 'djbolos.bolos.jugadores.views.detail'),
    # Example:
    # (r'^djbolos/', include('djbolos.foo.urls')),

    # Uncomment the admin/doc line below and add 'django.contrib.admindocs' 
    # to INSTALLED_APPS to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    (r'^admin/', include(admin.site.urls))
)
