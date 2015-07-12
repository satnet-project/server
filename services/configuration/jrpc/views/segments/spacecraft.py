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
from rpc4django import rpcmethod
from services.accounts import models as account_models
from services.configuration.models import segments
from services.configuration.jrpc.serializers import serialization as jrpc_serial
from website import settings as satnet_settings

logger = logging.getLogger('configuration')


@rpcmethod(
    name='configuration.sc.list',
    signature=[],
    login_required=satnet_settings.JRPC_LOGIN_REQUIRED
)
def list_spacecraft(**kwargs):
    """JRPC method.
    Creates a list with the identifiers of the available Spacecraft for
    the user that is requesting the service.
    User name must be obtained from the request, since this has already been
    validated by the authentication backend
    """
    # 1) user must be obtained from the request
    user, username = account_models.get_user(
        http_request=kwargs.get('request', None)
    )
    # 2) only the ground stations that belong to the incoming user are returned
    spacecraft = segments.Spacecraft.objects.filter(user=user).all()
    return [str(s.identifier) for s in spacecraft]


@rpcmethod(
    name='configuration.sc.create',
    signature=['String', 'String', 'String'],
    login_required=satnet_settings.JRPC_LOGIN_REQUIRED
)
def create(identifier, callsign, tle_id, **kwargs):
    """JRPC method.
    Creates a new ground station with the given configuration.
    User name must be obtained from the request, since this has already been
    validated by the authentication backend
    """

    user, username = account_models.get_user(
        http_request=kwargs.get('request', None)
    )

    sc = segments.Spacecraft.objects.create(
        tle_id,
        user=user,
        identifier=identifier,
        callsign=callsign
    )

    return {
        jrpc_serial.SC_ID_K: str(sc.identifier)
    }


@rpcmethod(
    name='configuration.sc.getConfiguration',
    signature=['String'],
    login_required=satnet_settings.JRPC_LOGIN_REQUIRED
)
def get_configuration(spacecraft_id):
    """JRPC method.
    Returns the configuration for the given Spacecraft.
    """
    return jrpc_serial.serialize_sc_configuration(
        segments.Spacecraft.objects.get(identifier=spacecraft_id)
    )


@rpcmethod(
    name='configuration.sc.setConfiguration',
    signature=['String', 'Object'],
    login_required=satnet_settings.JRPC_LOGIN_REQUIRED
)
def set_configuration(spacecraft_id, configuration):
    """JRPC method.
    Returns the configuration for the given Spacecraft.
    """
    callsign, tle_id = jrpc_serial.deserialize_sc_configuration(configuration)
    sc = segments.Spacecraft.objects.get(identifier=spacecraft_id)
    sc.update(callsign=callsign, tle_id=tle_id)
    return spacecraft_id


@rpcmethod(
    name='configuration.sc.getChannels',
    signature=['String'],
    login_required=satnet_settings.JRPC_LOGIN_REQUIRED
)
def list_channels(spacecraft_id):
    """JRPC method.
    Returns the channels for the given Spacecraft.
    """
    return jrpc_serial.serialize_channels(
        segments.Spacecraft.objects.get(
            identifier=spacecraft_id
        ).channels.all()
    )


@rpcmethod(
    name='configuration.sc.delete',
    signature=['String'],
    login_required=satnet_settings.JRPC_LOGIN_REQUIRED
)
def delete(spacecraft_id):
    """JRPC method.
    Deletes the ground station identified by the given Spacecraft. It
    also deletes all channels associated to this ground station.
    """
    segments.Spacecraft.objects.get(identifier=spacecraft_id).delete()
    return spacecraft_id
