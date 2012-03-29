
from django.conf.urls.defaults import patterns, include, url

urlpatterns = patterns('',
    url(r'^', include('registration.urls')),
    url(r'^profile/$', 'accounts.views.profile', name='auth_profile'),

    # Account management
#    url(r'^register/$', 'accounts.views.register'),
#    url(r'^login/$', 'django.contrib.auth.views.login'),
#    url(r'^logout/$', 'django.contrib.auth.views.logout'),
#    url(r'^accounts/profile/$', 'django.contrib.auth.views.profile'),
#    url(r'^reset/$', 'django.contrib.auth.views.password_reset'),
#    url(r'^reset/done/$', 'django.contrib.auth.views.password_reset_done'),
#    url(r'^reset/confirm/$', 'django.contrib.auth.views.password_reset_confirm'),
)
