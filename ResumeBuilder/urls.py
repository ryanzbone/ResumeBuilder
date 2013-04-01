from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf.urls import *
from django.conf import settings
from django.contrib.auth.views import login, logout


from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('builder.views',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', 'index', name='index'),
    url(r'^profile/([^/]+)/$', 'profile', name='profile'),
    url(r'^search/$', 'search'),
    url(r'^contact/$', 'contact'),
    url(r'^contact/thanks/$', 'thanks'),
    url(r'^form/add/(?P<formType>[^/]+)/$', 'add_form', name='add_form'),
    url(r'^form/edit/(?P<formType>[^/]+)/(?P<formId>\d+)/$', 'edit_form', name='edit_form'),
    url(r'^accounts/login/$',  login, name='login'),
    url(r'^accounts/logout/$', logout, {'next_page': '/'}, name='logout'),
    url(r'^accounts/register/$', 'register', name='register'),


)
if settings.DEBUG:
	urlpatterns += patterns('',
    	url(r'^Media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT,}),
	)

urlpatterns += staticfiles_urlpatterns()
