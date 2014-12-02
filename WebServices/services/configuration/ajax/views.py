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

import logging
from django.contrib.auth import decorators as auth_decorators
from jsonview import decorators, exceptions
from services.common import gis
from services.configuration.models import segments

logger = logging.getLogger('configuration')

@decorators.json_view
@auth_decorators.login_required
def groundstation_valid_id(request):
    """
    AJAX method for checking whether a given identifier is in use or not within
    the database.
    :param request: The GET HTTP request.
    :return: '{ isValid: "true/false", value: "$GET.value" }
    """
    requested_id = request.GET['value']
    if not requested_id:
        raise exceptions.BadRequest("'value' not found as a GET parameter.")

    is_valid = not segments.GroundStation.objects.filter(
        identifier=requested_id
    ).exists()

    return {
        'isValid': is_valid,
        'value': requested_id
    }

@decorators.json_view
@auth_decorators.login_required
def spacecraft_valid_id(request):
    """
    AJAX method for checking whether a given identifier is in use or not within
    the database.
    :param request: The GET HTTP request.
    :return: '{ isValid: "true/false", value: "$GET.value" }
    """
    requested_id = request.GET['value']
    if not requested_id:
        raise exceptions.BadRequest("'value' not found as a GET parameter.")

    is_valid = not segments.Spacecraft.objects.filter(
        identifier=requested_id
    ).exists()

    return {
        'isValid': is_valid,
        'value': requested_id
    }

@decorators.json_view
@auth_decorators.login_required
def user_geoip(request):
    """
    AJAX method for retrieving the estimated location of a given user using the
    IP address of the request..
    :param request: The GET HTTP request.
    :return: {  }
    """
    requested_id = request.GET['value']
    if not requested_id:
        raise exceptions.BadRequest("'value' not found as a GET parameter.")

    lat, lng = gis.get_remote_user_location(ip='')

    return {
        'latitude': lat, 'longitude': lng
    }