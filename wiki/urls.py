from django.conf.urls.defaults import patterns, include, url

urlpatterns = patterns('wiki.views',
    url(r'^exercises/(?P<exercise_id>\w+)/$', 'show_exercise'),
    url(r'^exercises/(?P<exercise_id>\w+)/edit/$', 'edit_exercise'),
    
)
