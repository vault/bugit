
from django.conf.urls.defaults import patterns, url

urlpatterns = patterns('ajax.views',
    url(r'^users/complete/$', 'user_complete', name='user_complete'),
)

