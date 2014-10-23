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

from rpc4django import rpcmethod

from services.accounts import models as account_models
from services.configuration.models import segments
from services.configuration.jrpc.serializers import serialization as jrpc_serial


@rpcmethod(
    name='configuration.sc.list',
    signature=[],
    login_required=True
)
def list_spacecraft(**kwargs):
    """
    JRPC method.

    Creates a list with the identifiers of the available Spacecraft for
    the user that is requesting the service.
    """

    # 1) user must be obtained from the request, since this has already been
    #       validated by the authentication backend
    http_request = kwargs.get('request', None)
    spacecraft = segments.Spacecraft.objects.filter(
        user=http_request.user
    ).all()
    return [str(s.identifier) for s in spacecraft]


@rpcmethod(
    name='configuration.sc.create',
    signature=['String', 'String', 'String'],
    login_required=True
)
def create(identifier, callsign, tle_id, **kwargs):
    """
    JRPC method.

    Creates a new ground station with the given configuration.
    """

    request = kwargs.get('request', None)
    if request is None:
        return
    username = request.user.username

    if username is None:
        raise Exception('Could not find <username> within HTTP request.')

    user = account_models.UserProfile.objects.get(username=username)
    if user is None:
        raise Exception('User <' + username + '> could not be found.')

    sc = segments.Spacecraft.objects.create(
        user=user,
        identifier=identifier,
        callsign=callsign,
        tle_id=tle_id
    )

    return {
        jrpc_serial.SC_ID_K: str(sc.identifier)
    }


@rpcmethod(
    name='configuration.sc.getConfiguration',
    signature=['String'],
    login_required=True
)
def get_configuration(spacecraft_id):
    """
    JRPC method.

    Returns the configuration for the given Spacecraft.
    """
    return jrpc_serial.serialize_sc_configuration(
        segments.Spacecraft.objects.get(identifier=spacecraft_id)
    )


@rpcmethod(
    name='configuration.sc.setConfiguration',
    signature=['String', 'Object'],
    login_required=True
)
def set_configuration(spacecraft_id, configuration):
    """
    JRPC method.

    Returns the configuration for the given Spacecraft.
    """
    callsign, tle_id = jrpc_serial.deserialize_sc_configuration(configuration)
    sc = segments.Spacecraft.objects.get(identifier=spacecraft_id)
    sc.update(callsign=callsign, tle_id=tle_id)
    return True


@rpcmethod(
    name='configuration.sc.getChannels',
    signature=['String'],
    login_required=True
)
def list_channels(spacecraft_id):
    """
    JRPC method.

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
    login_required=True
)
def delete(spacecraft_id):
    """
    JRPC method.

    Deletes the ground station identified by the given Spacecraft. It
    also deletes all channels associated to this ground station.
    """
    segments.Spacecraft.objects.get(identifier=spacecraft_id).delete()
    return True