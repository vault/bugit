from django.conf.urls.defaults import patterns, include, url


# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', 'django.views.generic.simple.direct_to_template', {'template':'welcome.html'}),
    url(r'^repo/', include('repo_manage.urls')),
    url(r'^settings/', include('user_manage.urls')),
    url(r'^view/', include('viewer.urls')),
    url(r'^admin/', include(admin.site.urls)),
)

