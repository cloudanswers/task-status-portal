from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^pivotal/', include('pivotal.urls')),
    url(r'^$', 'django_project.views.index'),
)
