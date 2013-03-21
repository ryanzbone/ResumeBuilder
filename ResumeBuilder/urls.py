from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf.urls import *

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('builder.views',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', 'index'),
    url(r'^profile/([^/]+)/$', 'profile'),
    url(r'^search-form/$', 'search_form'),
    url(r'^search/$', 'search'),
    url(r'^contact/$', 'contact'),
    url(r'^contact/thanks/$', 'thanks'),
    url(r'^workexperience-form/$', 'work_experience_form')
)

urlpatterns += staticfiles_urlpatterns()
