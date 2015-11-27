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
from services.configuration.models import tle as tle_models
from services.configuration.models.celestrak import CelestrakDatabase
from services.configuration.jrpc.serializers import tle as tle_serializers
from website import settings as satnet_settings


@rpc4django.rpcmethod(
    name='configuration.tle.celestrak.sections',
    signature=[],
    login_required=satnet_settings.JRPC_LOGIN_REQUIRED
)
def get_celestrak_sections():
    """JRPC method
    Returns the sections structure of the Celestrak database.

    :return: Array with the pairs 'section' and 'subsection'
    """
    return CelestrakDatabase.CELESTRAK_SELECT_SECTIONS


@rpc4django.rpcmethod(
    name='configuration.tle.celestrak.resource',
    signature=['String'],
    login_required=satnet_settings.JRPC_LOGIN_REQUIRED
)
def get_celestrak_resource(subsection):
    """JRPC method
    Returns the URI of the resources associated with the given
    subsection of the Celestrak database.

    :param subsection: Subsection of the Celestrak database as retrieved from
                        the JRPC method 'get_celestrak_sections()'
    :return: URI to the resource within the Celestrak database
    """
    url = CelestrakDatabase.CELESTRAK_RESOURCES[subsection]
    tles = tle_models.TwoLineElement.objects.filter(source=url).all()
    return tle_serializers.TleSerializer.serialize_resource(url, tles)


@rpc4django.rpcmethod(
    name='configuration.tle.celestrak.tle',
    signature=['String'],
    login_required=satnet_settings.JRPC_LOGIN_REQUIRED
)
def get_spacecraft_tle(spacecraft_id):
    """JRPC method
    Returns the TLE object associated with the spacecraft for the given
    identifier.

    :param spacecraft_id: Identififer of the spacecraft
    :return: Object containing: { spacecraft_id, tle_id, line_1, line_2 }
    """
    sc = segment_models.Spacecraft.objects.get(identifier=spacecraft_id)
    return tle_serializers.TleSerializer.serialize_tle(sc)
