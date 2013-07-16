from django.conf.urls.defaults import patterns, url

urlpatterns = patterns('feedback.views',
    url(r'^$', 'feedback_main', name='feedback'),
)

