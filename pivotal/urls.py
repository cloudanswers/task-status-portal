from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
    url(r'^(?P<project_id>\d+)/stories/(?P<tag_filter>\w+)/(?P<hash_key>\w+)/$', 'pivotal.views.stories', name='pivotal_stories'),
    url(r'^(?P<project_id>\d+)/stories/(?P<tag_filter>\w+)/(?P<hash_key>\w+)/(?P<story_id>\d+)/tasks/$', 'pivotal.views.tasks', name='pivotal_tasks'),
)
