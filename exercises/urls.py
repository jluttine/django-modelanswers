from django.conf.urls.defaults import patterns, include, url

from wiki import views
from exercises import models, forms

class classes:
    Versioned = models.Exercise
    Revision = models.ExerciseRevision
    EditForm = forms.ExerciseEditForm
    CreateForm = forms.ExerciseCreateForm
class templates:
    show = 'exercises/show_exercise.html'
    add = 'exercises/add_exercise.html'
    edit = 'exercises/edit_exercise.html'
    list = 'exercises/list_exercises.html'
    history = 'exercises/show_exercise_history.html'
    delete = 'exercises/delete_exercise.html'
class urls:
    show = 'exercises:show'
    list = 'exercises:list'


urlpatterns = patterns('',

    (r'^', 
     include('wiki.urls', 
             namespace='exercises'),
     {
         'classes': classes,
         'templates': templates,
         'urls': urls
     }),


    ## url(r'^$', 
    ##     views.list_pages, 
    ##     kwargs={
    ##         'template_name': 'exercises/list_exercises.html'
    ##         },
    ##     name='list_exercises'),
        
    ## url(r'^add/$',
    ##     views.add_page,
    ##     kwargs={
    ##         'template_name': 'exercises/add_exercise.html',
    ##         'revision_class': ExerciseRevision
    ##         },
    ##     name='add_exercise'),
        
    ## url(r'^(?P<primary_key>\w+)/$',
    ##     views.show_page, 
    ##     kwargs={
    ##         'template_name': 'exercises/show_exercise.html',
    ##         'revision_class': ExerciseRevision
    ##         },
    ##     name='show_exercise'),
        
    ## url(r'^(?P<primary_key>\w+)/edit/$', 
    ##     views.edit_page, 
    ##     kwargs={
    ##         'template_name': 'exercises/edit_exercise.html',
    ##         'revision_class': ExerciseRevision
    ##         },
    ##     name='edit_exercise'),
        
    ## url(r'^(?P<primary_key>\w+)/history/$',
    ##     views.show_history, 
    ##     kwargs={
    ##         'template_name': 'exercises/show_exercise_history.html'
    ##         },
    ##     name='show_exercise_history'),

    ## url(r'^(?P<primary_key>\w+)/history/(?P<revision_pk>\w+)$',
    ##     views.show_page, 
    ##     kwargs={
    ##         'template_name': 'exercises/show_exercise.html',
    ##         'revision_class': ExerciseRevision
    ##         },
    ##     name='show_exercise_revision'),

    ## url(r'^(?P<primary_key>\w+)/delete/$', 
    ##     views.delete_page, 
    ##     kwargs={
    ##         'template_name': 'exercises/delete_exercise.html'
    ##         },
    ##     name='delete_exercise'),
    
)
