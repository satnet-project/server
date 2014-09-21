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

from services.configuration.jrpc import serialization
from services.configuration.models import segments


@rpcmethod(
    name='configuration.gs.list',
    signature=[],
    login_required=True
)
def list_groundstations(**kwargs):
    """
    JRPC method.

    Creates a list with the identifiers of the available ground stations for
    the user that is logged in within this request.
    """

    # 1) user must be obtained from the request, since this has already been
    #       validated by the authentication backend
    http_request = kwargs.get('request', None)
    gs_objects = segments.GroundStation.objects.filter(
        user=http_request.user
    ).all()
    return [str(g.identifier) for g in gs_objects]


@rpcmethod(
    name='configuration.gs.getConfiguration',
    signature=['String'],
    login_required=True
)
def get_configuration(ground_station_id):
    """
    JRPC method.

    Returns the configuration for the given ground station.
    """
    return serialization.serialize_gs_configuration(
        segments.GroundStation.objects.get(identifier=ground_station_id)
    )


@rpcmethod(
    name='configuration.gs.setConfiguration',
    signature=['String', 'Object'],
    login_required=True
)
def set_configuration(ground_station_id, configuration):
    """
    JRPC method.

    Returns the configuration for the given ground station.
    """
    callsign, contact_elevation, latitude, longitude =\
        serialization.deserialize_gs_configuration(configuration)
    gs = segments.GroundStation.objects.get(identifier=ground_station_id)
    gs.update(
        callsign=callsign, contact_elevation=contact_elevation,
        latitude=latitude, longitude=longitude
    )
    return True


@rpcmethod(
    name='configuration.gs.getChannels',
    signature=['String'],
    login_required=True
)
def list_channels(ground_station_id):
    """
    JRPC method.

    Returns the channels for the given ground station.
    """
    ch_objects = segments.GroundStation.objects.get(
        identifier=ground_station_id
    ).channels.all()
    return {
        serialization.CHANNEL_LIST_K: [str(c.identifier) for c in ch_objects]
    }


@rpcmethod(
    name='configuration.gs.delete',
    signature=['String'],
    login_required=True
)
def delete(ground_station_id):
    """
    JRPC method.

    Deletes the ground station identified by the given 'ground_station_id'. It
    also deletes all channels associated to this ground station.
    """
    segments.GroundStation.objects.get(identifier=ground_station_id).delete()
    return True