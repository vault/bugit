from django.conf.urls.defaults import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', 'django.views.generic.simple.direct_to_template', {'template':'welcome.html'}),
    url(r'^repo/', include('repo_manage.urls')),
    url(r'^ajax/', include('ajax.urls')),
    url(r'^settings/', include('user_manage.urls')),
    url(r'^view/', include('viewer.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^feedback/', include('feedback.urls')),
    url(r'^login/', 'django.contrib.auth.views.login', {'template_name': 'login.html'}),
)

