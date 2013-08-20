from django.conf.urls.defaults import patterns, url

urlpatterns = patterns('repo_manage.views',
    url(r'^$', 'index', name='index'),
    url(r'^create/$', 'repo_simple_new', name='repo_simple_new'),
    url(r'^create/settings/$', 'repo_new', name='repo_new'),
    url(r'^(?P<user_name>\w+)/$',  'repo_list', name='repo_list'),
    url(r'^(?P<user_name>[-\w]+)/(?P<repo_name>[-\w]+)/$', 'repo_desc', name='repo_desc'),
    url(r'^(?P<user_name>[-\w]+)/(?P<repo_name>[-\w]+)/access$', 'repo_access', name='repo_access'),
    url(r'^(?P<user_name>[-\w]+)/(?P<repo_name>[-\w]+)/clone$', 'repo_clone', name='repo_clone'),
    url(r'^(?P<user_name>[-\w]+)/(?P<repo_name>[-\w]+)/delete/$', 'repo_delete', name='repo_delete'),
    url(r'^(?P<user_name>[-\w]+)/(?P<repo_name>[-\w]+)/settings/$', 'repo_edit', name='repo_edit'),
)

