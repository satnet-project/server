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
__author__ = 'rtubiopa@calpoly.edu'

from django.conf import urls
from accounts import views

urlpatterns = urls.patterns(
    '',
    urls.url(r'^$', views.redirect_home, name='index'),
    # ### for overriding default 'accounts' urls from
    # django-registration
    urls.url(r'^accounts/', urls.include('accounts.urls')),
    # ### default django auth accounts
    (r'^accounts/', urls.include('django.contrib.auth.urls')),
    # ### sc/gs configuration service application
    urls.url(r'^configuration/', urls.include('configuration.urls')),
    # ### JSON-Rpc API
    urls.url(r'^jrpc/$', 'rpc4django.views.serve_rpc_request'),
    # ### django-registration
    urls.url(r'^accounts/', urls.include('registration.backends.default.urls')),
    # ### django-session-security
    urls.url(r'session_security/', urls.include('session_security.urls'))

)