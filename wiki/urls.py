from django.conf.urls.defaults import patterns, include, url

urlpatterns = patterns('wiki.views',
    url(r'^exercises/$', 'list_exercises'),
    url(r'^exercises/add/$', 'add_exercise'),
    url(r'^exercises/(?P<exercise_id>\w+)/$', 'show_exercise'),
    url(r'^exercises/(?P<exercise_id>\w+)/edit/$', 'edit_exercise'),
    url(r'^exercises/(?P<exercise_id>\w+)/delete/$', 'delete_exercise'),
    
)
