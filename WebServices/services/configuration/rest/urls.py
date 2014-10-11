"""
   Copyright 2014 Ricardo Tubio-Pardavila

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

from services.configuration.rest.views import segments as segment_views

urlpatterns = urls.patterns('',
    urls.url(r'^groundstations$',
        decorators.login_required(
            segment_views.ListGroundStationsView.as_view()
        ),
        name='rest-cfg-gs-list'
    ),
    urls.url(r'^spacecraft',
        decorators.login_required(
            segment_views.ListSpacecraftView.as_view()
        ),
        name='rest-cfg-sc-list'
    )
)