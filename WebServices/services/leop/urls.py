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
from django.contrib.auth import decorators
from services.leop import views as leop_views

urlpatterns = urls.patterns(
    '',
    urls.url(
        r'^management$',
        decorators.login_required(leop_views.LeopManagementView.as_view()),
        name='leop_management'
    ),
    urls.url(
        r'^create$',
        decorators.login_required(leop_views.LeopCreateView.as_view()),
        name='leop_create'
    ),
    urls.url(
        r'^update/(?P<identifier>\w+)$',
        decorators.login_required(leop_views.LeopUpdateView.as_view()),
        name='leop_update'
    ),
    urls.url(
        r'^delete/(?P<identifier>\w+)$',
        decorators.login_required(leop_views.LeopDeleteView.as_view()),
        name='leop_delete'
    ),
    urls.url(
        r'^access/(?P<identifier>\w+)$',
        decorators.login_required(leop_views.redirect_leop),
        name='leop_access'
    ),
)