from django.conf.urls.defaults import patterns, include, url

urlpatterns = patterns('wiki.views',
                       
    url(r'^$', 
        'list_pages', 
        name='list'),
        
    url(r'^add/$',
        'add_page',
        name='add'),
        
    url(r'^(?P<primary_key>\w+)/$',
        'show_page', 
        name='show'),
        
    url(r'^(?P<primary_key>\w+)/edit/$', 
        'edit_page', 
        name='edit'),
        
    url(r'^(?P<primary_key>\w+)/history/$',
        'show_history', 
        name='history'),

    url(r'^(?P<primary_key>\w+)/history/(?P<revision_pk>\w+)$',
        'show_page', 
        name='show_revision'),

    url(r'^(?P<primary_key>\w+)/delete/$', 
        'delete_page', 
        name='delete'),
    
)

