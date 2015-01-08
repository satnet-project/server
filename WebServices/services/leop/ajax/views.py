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

import logging
from django.contrib.auth import decorators as auth_decorators
from jsonview import decorators, exceptions
from services.leop.models import ufo as ufo_models

logger = logging.getLogger('leop')


@decorators.json_view
@auth_decorators.login_required
def ufo_valid_id(request):
    """AJAX method.
    Checks whether a given identifier is in use or not within the database.
    :param request: The GET HTTP request
    :return: '{ isValid: "true/false", value: "$GET.value" }
    """
    requested_id = request.GET['value']
    if not requested_id:
        raise exceptions.BadRequest("'value' not found as a GET parameter.")
    valid = not ufo_models.UFO.objects.filter(identifier=requested_id).exists()

    return {
        'isValid': valid,
        'value': requested_id
    }