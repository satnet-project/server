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
import logging
from services.accounts import models as account_models
from services.configuration.models import segments as segment_models
from services.configuration.jrpc.serializers import \
    segments as segment_serializers
from website import settings as satnet_settings

logger = logging.getLogger('configuration')


@rpcmethod(
    name='configuration.gs.list.mine',
    signature=[],
    login_required=satnet_settings.JRPC_LOGIN_REQUIRED
)
def list_groundstations_mine(**kwargs):
    """JRPC test: configuration.gs.list.mine
    Creates a list with the identifiers of the groundstation that belong to the
    user that is making the remote call.

    :param kwargs: Additional JRPC parameters dictionary
    :return:
    """
    # 1) user must be obtained from the request
    user, username = account_models.get_user(
        http_request=kwargs.get('request', None)
    )
    # 2) only the ground stations that belong to the incoming user are returned
    return [
        str(s.identifier) for s in segment_models.GroundStation.objects.filter(
            user=user
        )
    ]


@rpcmethod(
    name='configuration.sc.list.others',
    signature=[],
    login_required=satnet_settings.JRPC_LOGIN_REQUIRED
)
def list_groundstations_others(**kwargs):
    """JRPC test: configuration.gs.list.mine
    Creates a list with the identifiers of the groundstations that belong to the
    user that is making the remote call.

    :param kwargs: Additional JRPC parameters dictionary
    :return:
    """
    # 1) user must be obtained from the request
    user, username = account_models.get_user(
        http_request=kwargs.get('request', None)
    )
    # 2) only the groundstations that belong to the incoming user are excluded
    return [
        str(s.identifier) for s in segment_models.GroundStation.objects.exclude(
            user=user
        )
    ]


@rpcmethod(
    name='configuration.gs.list',
    signature=[],
    login_required=satnet_settings.JRPC_LOGIN_REQUIRED
)
def list_groundstations(**kwargs):
    """JRPC method: configuration.gs.list
    Creates a list with the identifiers of the available ground stations for
    the user that is logged in within this request.

    :param kwargs: Additional JRPC parameters dictionary
    """
    return [
        str(g.identifier) for g in segment_models.GroundStation.objects.all()
    ]


@rpcmethod(
    name='configuration.gs.create',
    signature=['String', 'String', 'String', 'String', 'String'],
    login_required=satnet_settings.JRPC_LOGIN_REQUIRED
)
def create(identifier, callsign, elevation, latitude, longitude, **kwargs):
    """JRPC method: configuration.gs.create
    Creates a new ground station with the given configuration.

    :param identifier: Identifier of the Ground Station
    :param callsign: Callsign string of the Ground Station
    :param elevation: Minimum contact elevation
    :param latitude: Latitude of the location
    :param longitude: Longitude of the location
    :param kwargs: Additional JRPC parameters dictionary
    """

    user, username = account_models.get_user(
        http_request=kwargs.get('request', None)
    )

    gs = segment_models.GroundStation.objects.create(
        latitude=latitude,
        longitude=longitude,
        identifier=identifier,
        callsign=callsign,
        contact_elevation=elevation,
        username=username
    )

    return {
        segment_serializers.GS_ID_K: str(gs.identifier)
    }


@rpcmethod(
    name='configuration.gs.get',
    signature=['String'],
    login_required=satnet_settings.JRPC_LOGIN_REQUIRED
)
def get_configuration(ground_station_id):
    """JRPC method: configuration.gs.getConfiguration
    Returns the configuration for the given ground station.

    :param ground_station_id: Identifier of the Ground Station
    """
    return segment_serializers.serialize_gs_configuration(
        segment_models.GroundStation.objects.get(identifier=ground_station_id)
    )


@rpcmethod(
    name='configuration.gs.set',
    signature=['String', 'Object'],
    login_required=satnet_settings.JRPC_LOGIN_REQUIRED
)
def set_configuration(ground_station_id, configuration):
    """JRPC method: configuration.gs.setConfiguration
    Sets the configuration for the given ground station.

    :param ground_station_id: Identifier of the Ground Station
    :param configuration: Configuration object for the Ground Station
    """
    callsign, contact_elevation, latitude, longitude =\
        segment_serializers.deserialize_gs_configuration(configuration)
    gs = segment_models.GroundStation.objects.get(identifier=ground_station_id)
    gs.update(
        callsign=callsign, contact_elevation=contact_elevation,
        latitude=latitude, longitude=longitude
    )
    return ground_station_id


@rpcmethod(
    name='configuration.gs.delete',
    signature=['String'],
    login_required=satnet_settings.JRPC_LOGIN_REQUIRED
)
def delete(ground_station_id):
    """JRPC method: configuration.gs.delete
    Deletes the ground station identified by the given 'ground_station_id'. It
    also deletes all channels associated to this ground station.

    :param ground_station_id: Identifier of the Ground Station
    """
    segment_models.GroundStation.objects.get(
        identifier=ground_station_id
    ).delete()
    return ground_station_id
