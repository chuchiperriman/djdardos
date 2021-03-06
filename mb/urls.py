from django.conf.urls.defaults import *

urlpatterns = patterns('djdardos.mb.views',
    url(r'^$', 'list', name='mb-list'),
    url(r'^list/$', 'list', name='mb-list'),
    url(r'^new/$', 'new_tweet', name='mb-new_tweet'),
    url(r'^follow/(?P<content_type_id>\d+)/(?P<object_id>\d+)$', 'follow', name='mb-follow'),
)
