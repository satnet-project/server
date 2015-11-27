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
from services.configuration.ajax import views

urlpatterns = urls.patterns(
    '',
    urls.url(
        r'^groundstations/valid_id$', views.groundstation_valid_id,
        name='ajax-cfg-gs-valid-id'
    ),
    urls.url(
        r'^spacecraft/valid_id$', views.spacecraft_valid_id,
        name='ajax-cfg-sc-valid-id'
    ),
    urls.url(
        r'^user/geoip$', views.user_geoip, name='ajax-cfg-user-geoip'
    ),
    urls.url(
        r'^hostname/geoip$', views.hostname_geoip,
        name='ajax-cfg-hostname-geoip'
    )
)
