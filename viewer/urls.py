from django.conf.urls.defaults import patterns, include, url

urlpatterns = patterns('viewer.views',
    url(r'^$', 'view_index'),
    url(r'^(?P<user_name>[-\w]+)/$', 'user_index'),
    url(r'^(?P<user_name>[-\w]+)/(?P<repo_name>[-\w]+)/view$', 'repo_browse', name='repo_browse'),
    url(r'^(?P<user_name>[-\w]+)/(?P<repo_name>[-\w]+)/(?P<path>.*)$', 'repo_browse', name='repo_browse'),
)

