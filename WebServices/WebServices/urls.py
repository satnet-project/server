from django.conf.urls import patterns, include, url
from django.views.generic import TemplateView

import accounts.views

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',

    url(r'^$', accounts.views.redirect_home, name='index'),

    # ### for overriding default 'accounts' urls from django-registration
    url(r'^accounts/', include('accounts.urls')),
    
    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
    
    # ### django-registration
    url(r'^accounts/', include('registration.backends.default.urls')),
    
    # ### django-session-security
    url(r'session_security/', include('session_security.urls')),
    
)
