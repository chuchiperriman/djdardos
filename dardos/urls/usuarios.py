from django.conf.urls.defaults import *

urlpatterns = patterns('djdardos.dardos.views.usuarios',
    url(r'^$', 'home', name='dardos-usuarios-home'),
)
