from django.conf.urls import patterns, include, url


urlpatterns = patterns('',
    #url(r'^language/(?P<language>[a-z\-]+)/$', 'article.views.language'),
    #url(r'^like/(?P<article_id>\d+)/$', 'article.views.like_article'),
    #url(r'^search/$', 'article.views.search_titles'),
    #url(r'^api/', include(article_resource.urls)),

    #courses
    url(r'^get_one_course/(?P<course_id>\d+)/$', 'ticwiapp.views.get_one_course'),
    url(r'^all_courses/$', 'ticwiapp.views.all_courses'),
    url(r'^create_course/$', 'ticwiapp.views.create_course'),
    url(r'^edit_course/(?P<course_id>\d+)/$', 'ticwiapp.views.create_course'),
    url(r'^update_course/$', 'ticwiapp.views.update_course'),
    url(r'^delete_course/(?P<course_id>\d+)$', 'ticwiapp.views.delete_course'),
    url(r'^add_presenter/(?P<course_id>\d+)/$', 'ticwiapp.views.add_presenter'),
    url(r'^add_presenter_now/(?P<course_id>\d+)/(?P<user_id>\d+)/$', 'ticwiapp.views.add_presenter_now'),
    url(r'^add_participant/(?P<course_id>\d+)/$', 'ticwiapp.views.add_participant'),
    url(r'^add_participant_now/(?P<course_id>\d+)/(?P<user_id>\d+)/$', 'ticwiapp.views.add_participant_now'),
    url(r'^remove_participant/(?P<course_id>\d+)/(?P<user_id>\d+)/$', 'ticwiapp.views.remove_participant'),   
    url(r'^remove_presenter/(?P<course_id>\d+)/(?P<user_id>\d+)/$', 'ticwiapp.views.remove_presenter'),
    url(r'^search_course/$', 'ticwiapp.views.search_course'),
    url(r'^add_comment/(?P<course_id>\d+)/$', 'ticwiapp.views.add_comment'),

    #Tics
    url(r'^add_tic/(?P<course_id>\d+)/(?P<user_type>\d+)/$', 'ticwiapp.views.add_tic'),
    url(r'^get_one_tic/(?P<tic_id>\d+)/$', 'ticwiapp.views.get_one_tic'),

    #Course Commments
    url(r'^change_course_comment_access/(?P<course_id>\d+)/(?P<comment_id>\w+)/$', 'ticwiapp.views.change_course_comment_access'),
    url(r'^search_user/$', 'ticwiapp.views.search_user'),

    #inbox
    url(r'^send_message/(?P<user_id>\d+)/(?P<sender_id>\w+)/$', 'ticwiapp.views.send_message'),
    
    #desktop
    url(r'^inst_desktop/$', 'ticwiapp.views.inst_desktop'),
    url(r'^user_desktop/$', 'ticwiapp.views.user_desktop'),
    url(r'^desktop/$', 'ticwiapp.views.desktop'),

)

