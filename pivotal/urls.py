from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
    url(r'^stories/(?P<project_id>\d+)/(?P<tag_filter>\S+)/(?P<hash_key>\S+)/$', 'pivotal.views.stories', name='pivotal_stories'),
)
