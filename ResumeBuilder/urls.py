from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf.urls import *
from django.conf import settings

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('builder.views',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', 'index'),
    url(r'^profile/([^/]+)/$', 'profile'),
    url(r'^search/$', 'search'),
    url(r'^contact/$', 'contact'),
    url(r'^contact/thanks/$', 'thanks'),
    url(r'^form/add/(?P<formType>[^/]+)/$', 'add_form'),
)
if settings.DEBUG:
	urlpatterns += patterns('',
    	url(r'^Media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT,}),
	)
urlpatterns += staticfiles_urlpatterns()
