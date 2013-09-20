from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
        url(r'^inst_profile/$', 'userprofile.views.inst_profile'),
        url(r'^user_profile/$', 'userprofile.views.user_profile'),\
        url(r'^redirect_to_desktop/$', 'userprofile.views.redirect_to_desktop'),
)
