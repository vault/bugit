from django.conf.urls.defaults import patterns, include, url

urlpatterns = patterns('user_manage.views',
    url(r'^$', 'user_settings', name='user_settings'),
    url(r'^profile/$', 'user_profile', name='user_profile'),
    url(r'^keys/create/$', 'pubkey_add', name='pubkey_add'),
    url(r'^keys/edit$', 'pubkey_edit', name='pubkey_edit'),
    url(r'^keys/(?P<key_id>\d+)/delete$', 'pubkey_delete', name='pubkey_delete'),
    url(r'^keys/(?P<key_id>\d+)/edit$', 'pubkey_edit', name='pubkey_edit'),
)
