from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf.urls import *
from django.conf import settings
from django.contrib.auth.views import login, logout


from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('builder.views',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', 'index', name='index'),
    url(r'^profile/(?P<userId>\d+)/$', 'profile', name='profile'),
    url(r'^profile/(?P<userId>\d+)/all/(?P<entryType>[^/]+)/$', 'view_all', name='view_all'),
    url(r'^form/add/(?P<formType>[^/]+)/$', 'add_form', name='add_form'),
    url(r'^form/edit/(?P<formType>[^/]+)/(?P<formId>\d+)/$', 'edit_form', name='edit_form'),
    url(r'^form/deleterequest/(?P<formType>[^/]+)/(?P<formId>\d+)/$', 'delete_request', name='delete_request'),
    url(r'^form/deleteconfirm/(?P<formType>[^/]+)/(?P<formId>\d+)/$', 'delete_confirm', name='delete_confirm'),
    url(r'^accounts/login/$',  login, name='login'),
    url(r'^accounts/logout/$', logout, {'next_page': '/'}, name='logout'),
    url(r'^accounts/register/$', 'register', name='register'),
    url(r'^export/options/(?P<userId>\d+)/$', 'export_options', name='export_options'),
    url(r'^export/(?P<fileType>[^/]+)/(?P<userId>\d+)/$', 'export_file', name='export'),
)
if settings.DEBUG:
	urlpatterns += patterns('',
    	url(r'^Media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT,}),
	)

urlpatterns += staticfiles_urlpatterns()
