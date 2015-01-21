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
from django.contrib.auth import decorators
from django.views.generic.base import RedirectView
from services.accounts import views as account_views
from website import views as website_views

admin.autodiscover()

urlpatterns = urls.patterns(
    '',

    # ### ######################################################################
    # ### ################################################## OVERRIDEN MAIN URLS
    # ### ######################################################################
    urls.url(
        r'^$',
        account_views.redirect_login,
        name='index'
    ),
    # ### Command and Control Interface
    urls.url(
        r'^operations/',
        decorators.login_required(website_views.redirect_operations),
        name='operations_interface'
    ),
    urls.url(
        r'^leop_staff/(?P<identifier>\w+)$',
        #decorators.login_required(website_views.redirect_leop),
        website_views.redirect_leop,
        name='leop_access'
    ),
   urls.url(
        r'^leop/',
        urls.include('services.leop.urls')
    ),
    urls.url(
        r'^communications/',
        urls.include('services.communications.urls')
    ),
    urls.url(
        r'^phppgadmin/$',
        RedirectView.as_view(url='/phppgadmin'),
        name='phppgadmin'
    ),

    # ### ######################################################################
    # ### ############################################ ACCOUNTS AND REGISTRATION
    # ### ######################################################################

    # ### for overriding default 'accounts' urls from
    urls.url(
        r'^accounts/',
        urls.include('services.accounts.urls')
    ),
    urls.url(
        r'^accounts/',
        urls.include('allauth.urls')
    ),

    # ### ######################################################################
    # ### ########################################## REST, AJAX, JRPC INTERFACES
    # ### ######################################################################

    # ### Django REST framework (api)
    urls.url(
        r'^api-auth/',
        urls.include('rest_framework.urls', namespace='rest_framework')
    ),
    # ### AJAX, configuration service
    urls.url(
        r'configuration/',
        urls.include('services.configuration.ajax.urls')
    ),
    # ### JSON-Rpc API
    urls.url(
        r'^jrpc/$',
        'rpc4django.views.serve_rpc_request'
    ),

    # ### ######################################################################
    # ### ################################################################# MISC
    # ### ######################################################################

    # ### django-session-security
    urls.url(
        r'session_security/',
        urls.include('session_security.urls')
    ),
    # ### django admin
    urls.url(
        r'^admin/',
        urls.include(admin.site.urls)
    )

)