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

import logging
logger = logging.getLogger(__name__)

from django.contrib.auth.decorators import login_required

from jsonview.decorators import json_view

from configuration.models.channels import GroundStationChannel

@login_required
@json_view
def channel_identifier_exists(channel_identifier):
    """
    Simple method that returns a boolean for indicating whether a channel for a ground
    station with the given identifier already exists.
    """

    return GroundStationChannel.objects.exists(identifier=channel_identifier)
