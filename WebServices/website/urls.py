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
from django.contrib import admin
from django.views.generic import base as django_views

from services.accounts import views

admin.autodiscover()

urlpatterns = urls.patterns(
    '',
    urls.url(
        r'^$',
        views.redirect_login,
        name='index'
    ),
    # ### Command and Control Interface
    urls.url(
        r'^c2/',
        views.redirect_home,
        name='c2_interface'
    ),
    urls.url(
        r'^phpmyadmin/',
        django_views.RedirectView.as_view(url='/phpmyadmin'),
        name='phpmyadmin'
    ),
    # ### for overriding default 'accounts' urls from
    # django-registration
    urls.url(
        r'^accounts/',
        urls.include('services.accounts.urls')
    ),
    # ### django-registration
    urls.url(
        r'^accounts/',
        urls.include('allauth.urls')
    ),
    # ### JSON-Rpc API
    urls.url(
        r'^jrpc/$',
        'rpc4django.views.serve_rpc_request'
    ),
    # ### django-session-security
    urls.url(
        r'session_security/',
        urls.include('session_security.urls')
    ),
    # ### django admin
    urls.url(
        r'^admin/',
        urls.include(admin.site.urls)
    ),
)