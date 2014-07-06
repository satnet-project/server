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

:Author:
    Ricardo Tubio-Pardavila (rtubiopa@calpoly.edu)
"""
__author__ = 'rtubiopa@calpoly.edu'

from rpc4django import rpcmethod

from configuration.jrpc import serialization as jrpc_serial
from configuration.models.segments import Spacecraft


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
    spacecraft = Spacecraft.objects.filter(
        user=http_request.user
    ).all()
    return [str(g.identifier) for g in spacecraft]


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
        Spacecraft.objects.get(identifier=spacecraft_id)
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
    sc = Spacecraft.objects.get(identifier=spacecraft_id)
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
        Spacecraft.objects.get(
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
    Spacecraft.objects.get(identifier=spacecraft_id).delete()
    return True