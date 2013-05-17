from django.conf.urls.defaults import patterns, url

urlpatterns = patterns('viewer.views',
    url(r'^$', 'view_index'),
    url(r'^(?P<user_name>[-\w]+)/$', 'user_index'),
    url(r'^(?P<user_name>[-\w]+)/(?P<repo_name>[-\w]+)/$', 'repo_browse', name='repo_browse'),
    url(r'^(?P<user_name>[-\w]+)/(?P<repo_name>[-\w]+)/plain/($?P<path>.*)$', 'repo_plain', name='repo_plain'),
    url(r'^(?P<user_name>[-\w]+)/(?P<repo_name>[-\w]+)/snapshot/($?<path.*)$', 'repo_snapshot', name='repo_snapshot'),
    url(r'^(?P<user_name>[-\w]+)/(?P<repo_name>[-\w]+)/(?P<path>.*)$', 'repo_browse', name='repo_browse'),
)

