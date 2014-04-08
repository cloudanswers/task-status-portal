from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
    url(r'^stories/$', 'pivotal.views.stories', name='pivotal_stories'),
)
