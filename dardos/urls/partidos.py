from django.conf.urls.defaults import *

urlpatterns = patterns('djdardos.dardos.views.partidos',
    url(r'^$', 'index', name='dardos-partidos-index'),
    url(r'^(?P<partido_id>\d+)/(?P<reporting>\w+)/$',
        'detail', name='dardos-partidos-detail-reporting'),
    url(r'^(?P<partido_id>\d+)/$', 'detail',
        name='dardos-partidos-detail'),
    url(r'^new/$', 'new', name='dardos-partidos-new'),
    url(r'^partidas/(?P<partido_id>\d+)/$', 'setpartidas',
        name='dardos-partidos-setpartidas'),
    url(r'^new_jornada/$', 'new_jornada',
        name='dardos-partidos-new_jornada'),
    url(r'^liga/(?P<liga_id>\d+)/ajax_get_siguiente_jornada/$',
        'ajax_get_siguiente_jornada',
        name='dardos-partidos-ajax_get_siguiente_jornada'),
)
