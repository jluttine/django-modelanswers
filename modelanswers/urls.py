from django.conf.urls.defaults import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^wiki/', include('wiki.urls')),

    url(r'^exercises/', include('exercises.urls')),

    url(r'^accounts/', include('accounts.urls')),

                       
    # Examples:
    # url(r'^$', 'modelanswers.views.home', name='home'),
    # url(r'^modelanswers/', include('modelanswers.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)
