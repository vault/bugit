from django.conf.urls.defaults import patterns, include, url

urlpatterns = patterns('git.views',
    url(r'^$', 'index', name='index'),

    url(r'^user_settings/$', 'user_settings', name='user_settings'),
    url(r'^user_settings/keys/create/$', 'pubkey_add', name='pubkey_add'),
    url(r'^user_settings/keys/(?P<key_id>\d+)/delete$', 'pubkey_delete', name='pubkey_delete'),
    url(r'^user_settings/keys/(?P<key_id>\d+)/edit$', 'pubkey_edit', name='pubkey_edit'),
    url(r'^user_settings/keys/edit$', 'pubkey_edit', name='pubkey_edit'),

    url(r'^(?P<user_name>\w+)/$',  'repo_list', name='repo_list'),
    url(r'^(?P<user_name>\w+)/create/$', 'repo_add', name='repo_add'),
    url(r'^(?P<user_name>[-\w]+)/(?P<repo_name>[-\w]+)/$', 'repo_view', name='repo_view'),
    url(r'^(?P<user_name>[-\w]+)/(?P<repo_name>[-\w]+)/delete/$', 'repo_delete', name='repo_delete'),
    url(r'^(?P<user_name>[-\w]+)/(?P<repo_name>[-\w]+)/settings/$', 'repo_edit', name='repo_edit'),
    url(r'^(?P<user_name>[-\w]+)/settings/$', 'repo_new', name='repo_new'),
)

