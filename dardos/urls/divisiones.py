from django.conf.urls.defaults import *

urlpatterns = patterns('djdardos.dardos.views.divisiones',
    url(r'^(?P<division_id>\d+)/$', 'detail',
        name='dardos-divisiones-detail'),
)
