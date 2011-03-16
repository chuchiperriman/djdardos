from django.conf.urls.defaults import *

urlpatterns = patterns('djdardos.dardos.views.graficas',
    url(r'^ajax_grafica_evolucion/$', 'ajax_grafica_evolucion',
        name='dardos-graficas-ajax_grafica_evolucion'),
)
