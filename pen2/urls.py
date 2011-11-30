from django.conf.urls.defaults import *
from django.views.generic.simple import direct_to_template
from pen2.views import fb_home

#from django.contrib import admin
#admin.autodiscover()
 
urlpatterns = patterns('',
#    (r'^admin/(.*)', admin.site.root),
    (r'^accounts/', include('registration.urls')),
    (r'^$', fb_home),
    (r'^$', direct_to_template, { 'template': 'index.html' }, 'index'),
    url(r'^facebook/login$', 'facebook.views.login'),
    url(r'^facebook/authentication_callback$', 'facebook.views.authentication_callback'),
)
