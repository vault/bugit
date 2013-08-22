from django.conf.urls.defaults import patterns, url

urlpatterns = patterns('viewer.views',
    url(r'^$', 'view_index'),
    url(r'^(?P<user_name>[-\w]+)/$', 'user_index'),
    url(r'^(?P<user_name>[-\w]+)/(?P<repo_name>[-\w]+)/$', 'repo_browse', name='repo_browse'),
    url(r'^(?P<user_name>[-\w]+)/(?P<repo_name>[-\w]+)/plain/(?P<path>.*)$', 'repo_plain', {'prefix': 'plain'},name='repo_plain'),
    url(r'^(?P<user_name>[-\w]+)/(?P<repo_name>[-\w]+)/patch/(?P<path>.*)$', 'repo_plain',{'prefix': 'patch'},  name='repo_patch'),
    url(r'^(?P<user_name>[-\w]+)/(?P<repo_name>[-\w]+)/snapshot/(?P<path>.*)$', 'repo_snapshot', name='repo_snapshot'),
    url(r'^(?P<user_name>[-\w]+)/(?P<repo_name>[-\w]+)/(?P<method>[-\w]+)/(?P<path>.*)$', 'repo_browse', name='repo_browse_specific'),
)

