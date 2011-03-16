from django.conf.urls.defaults import *

urlpatterns = patterns('djdardos.dardos.views.ligas',
    url(r'^$',    'ligas_index',    name='dardos-ligas-index'),
    url(r'^cambiar_liga/$', 'cambiar_liga',
        name='dardos-ligas-cambiar_liga'),
)
