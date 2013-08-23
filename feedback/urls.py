from django.conf.urls.defaults import patterns, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('feedback.views',
    url(r'^$', 'feedback_main', name='feedback'),
)

