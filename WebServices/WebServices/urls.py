"""
   Copyright 2013, 2014 Ricardo Tubio-Pardavila

   Licensed under the Apache License, Version 2.0 (the "License");
   you may not use this file except in compliance with the License.
   You may obtain a copy of the License at

       http://www.apache.org/licenses/LICENSE-2.0

   Unless required by applicable law or agreed to in writing, software
   distributed under the License is distributed on an "AS IS" BASIS,
   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
   See the License for the specific language governing permissions and
   limitations under the License.
"""

from django.conf.urls import patterns, include, url
import accounts.views

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns =\
    patterns('',
             url(r'^$', accounts.views.redirect_home, name='index'),
             # ### for overriding default 'accounts' urls from
             # django-registration
             url(r'^accounts/', include('accounts.urls')),
             # ### sc/gs configuration service application
             url(r'^configuration/', include('configuration.urls')),
             # ### JSON-Rpc API
             url(r'^jrpc/$', 'rpc4django.views.serve_rpc_request'),
             # Uncomment the admin/doc line below to enable admin docs:
             url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
             # Uncomment the next line to enable the admin:
             url(r'^admin/', include(admin.site.urls)),
             # ### django-registration
             url(r'^accounts/', include('registration.backends.default.urls')),
             # ### django-session-security
             url(r'session_security/', include('session_security.urls')),
             )
