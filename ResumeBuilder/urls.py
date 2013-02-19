from django.contrib.staticfiles.urls import staticfiles_urlpatterns


from django.conf.urls import patterns, include, url

from builder.views import index, profile

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', index),
    url(r'^profile/([^/]+)/$', profile)
)

urlpatterns += staticfiles_urlpatterns()
