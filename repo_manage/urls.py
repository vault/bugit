from django.conf.urls.defaults import patterns, url

urlpatterns = patterns('repo_manage.views',
    url(r'^$', 'index', name='index'),
    url(r'^(?P<user_name>\w+)/$',  'repo_list', name='repo_list'),
    url(r'^(?P<user_name>\w+)/create/$', 'repo_new', name='repo_new'),
    url(r'^(?P<user_name>[-\w]+)/(?P<repo_name>[-\w]+)/$', 'repo_view', name='repo_view'),
    url(r'^(?P<user_name>[-\w]+)/(?P<repo_name>[-\w]+)/delete/$', 'repo_delete', name='repo_delete'),
    url(r'^(?P<user_name>[-\w]+)/(?P<repo_name>[-\w]+)/settings/$', 'repo_edit', name='repo_edit'),
)

