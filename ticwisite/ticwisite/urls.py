from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

import settings

urlpatterns = patterns('',
    (r'^ticwiapp/', include('ticwiapp.urls')),
    (r'^userprofile/', include('userprofile.urls')),
 
   # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),

    # user auth urls
    url(r'^accounts/login/$',  'ticwisite.views.login'),
    url(r'^accounts/auth/$',  'ticwisite.views.auth_view'),
    url(r'^accounts/logout/$', 'ticwisite.views.logout'),
    url(r'^accounts/loggedin/$', 'ticwisite.views.loggedin'),
    url(r'^accounts/invalid/$', 'ticwisite.views.invalid_login'),
    url(r'^accounts/register/$', 'ticwisite.views.register_user'),
    url(r'^accounts/register_success/$', 'ticwisite.views.register_success'),


    url(r'^accounts/register_success/$', 'userprofile.views.redirect_to_desktop'),
    url(r'^accounts/go_home/$', 'ticwisite.views.go_home'),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)

if not settings.DEBUG:
    from django.contrib.staticfiles.urls import staticfiles_urlpatterns

    urlpatterns += staticfiles_urlpatterns()

