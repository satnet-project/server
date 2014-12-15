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

import rpc4django
from services.configuration.models import segments as segment_models


@rpc4django.rpcmethod(
    name='leop.gs.list',
    signature=[],
    login_required=True
)
def list_groundstations(**kwargs):
    """JRPC method (LEOP service).
    Returns the list of groundstations available for creating this LEOP
    system. In case a Ground Station is already in use for this system, it will
    not be listed.
    :param kwargs: Dictionary with additional variables like the HTTP request
                    itself (defined by RPC4Django).
    :return: List of the identifiers of the available groundstations.
    """

    # user must be obtained from the request, since this has already been
    # validated by the authentication backend
    http_request = kwargs.get('request', None)

    if not http_request.user.is_staff:
        raise Exception('Forbidden')

    return [
        str(g.identifier) for g in segment_models.GroundStation.objects.all()
    ]