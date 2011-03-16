from django.conf.urls.defaults import *
from django.views.generic.simple import direct_to_template

urlpatterns = patterns('djdardos.dardos.views.general',
    url(r'^login/$',    'login',        name='dardos-general-login'),
    url(r'^logout/$',   'logout',       name='dardos-general-logout'),
    url(r'^error_permisos/$',direct_to_template, {
        'template': 'dardos/general/error_permisos.html'},
        name='dardos-general-error-permisos'),
)
