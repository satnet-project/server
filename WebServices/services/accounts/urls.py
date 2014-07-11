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
from django.contrib.auth.decorators import login_required

from services.accounts import ajax, views

urlpatterns = urls.patterns(
    '',
    urls.url(
        r'^register/$',
        views.RegisterView.as_view(),
        name='register'
    ),
    urls.url(
        r'^login_ok/$',
        views.redirect_home,
        name='login_ok'
    ),
    # ### Staff specific views
    urls.url(
        r'^pending/$',
        login_required(views.PendingRegView.as_view()),
        name='pending'
    ),
    urls.url(
        r'^blocked/$',
        login_required(views.BlockedRegView.as_view()),
        name='blocked'
    ),
    urls.url(
        r'^verified/$',
        login_required(views.VerifiedView.as_view()),
        name='verified'
    ),
    urls.url(
        r'^inactive/$',
        login_required(views.InactiveView.as_view()),
        name='inactive'
    ),
    # ### UserProfile views
    urls.url(
        r'^user_profile/$',
        login_required(views.UserProfileView.as_view()),
        name='user_profile'
    ),
    # ### AJAX views
    urls.url(
        r'^ajax/user_details/$',
        ajax.user_details,
        name='ajax_user_details'
    ),
    urls.url(
        r'^ajax/user_verification/$',
        ajax.user_verification,
        name='ajax_user_verification'
    ),
)