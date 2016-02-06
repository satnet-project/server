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
from services.configuration.jrpc.serializers import \
    segments as segment_serializers
from website import settings as satnet_settings

logger = logging.getLogger('configuration')


@rpcmethod(
    name='configuration.sc.list.mine',
    signature=[],
    login_required=satnet_settings.JRPC_LOGIN_REQUIRED
)
def list_spacecraft_mine(**kwargs):
    """JRPC test: configuration.sc.list.mine
    Creates a list with the identifiers of the spacecraft that belong to the
    user that is making the remote call.

    :param kwargs: Additional JRPC parameters dictionary
    :return:
    """
    # 1) user must be obtained from the request
    user, username = account_models.get_user(
        http_request=kwargs.get('request', None)
    )
    # 2) only the spacecraft that belong to the incoming user are returned
    return [
        str(s.identifier) for s in segments.Spacecraft.objects.filter(
            user=user
        )
    ]


@rpcmethod(
    name='configuration.sc.list.others',
    signature=[],
    login_required=satnet_settings.JRPC_LOGIN_REQUIRED
)
def list_spacecraft_others(**kwargs):
    """JRPC test: configuration.sc.list.mine
    Creates a list with the identifiers of the spacecraft that belong to the
    user that is making the remote call.

    :param kwargs: Additional JRPC parameters dictionary
    :return:
    """
    # 1) user must be obtained from the request
    user, username = account_models.get_user(
        http_request=kwargs.get('request', None)
    )
    # 2) only the spacecraft that belong to the incoming user are excluded
    return [
        str(s.identifier) for s in segments.Spacecraft.objects.exclude(
            user=user
        )
    ]


@rpcmethod(
    name='configuration.sc.list',
    signature=[],
    login_required=satnet_settings.JRPC_LOGIN_REQUIRED
)
def list_spacecraft(**kwargs):
    """JRPC test: configuration.sc.list
    Creates a list with the identifiers of the available Spacecraft for
    the user that is requesting the service.
    User name must be obtained from the request, since this has already been
    validated by the authentication backend

    :param kwargs: Additional JRPC parameters dictionary
    """
    return [str(s.identifier) for s in segments.Spacecraft.objects.all()]


@rpcmethod(
    name='configuration.sc.create',
    signature=['String', 'String', 'String'],
    login_required=satnet_settings.JRPC_LOGIN_REQUIRED
)
def create(identifier, callsign, tle_id, **kwargs):
    """JRPC test: configuration.sc.create
    Creates a new ground station with the given configuration.
    User name must be obtained from the request, since this has already been
    validated by the authentication backend

    :param identifier: Identifier of the Spacecraft
    :param callsign: Callsign string of the Spacecraft
    :param tle_id: Identifier of the TLE associated with the Spacecraft
    :param kwargs: Additional JRPC parameters dictionary
    """

    try:

        user, username = account_models.get_user(
            http_request=kwargs.get('request', None)
        )

        sc = segments.Spacecraft.objects.create(
            tle_id,
            username=username,
            identifier=identifier,
            callsign=callsign
        )

    except Exception as ex:

        logger.exception(ex)
        raise ex

    return {
        segment_serializers.SC_ID_K: str(sc.identifier)
    }


@rpcmethod(
    name='configuration.sc.get',
    signature=['String'],
    login_required=satnet_settings.JRPC_LOGIN_REQUIRED
)
def get_configuration(spacecraft_id):
    """JRPC test: configuration.sc.getConfiguration
    Returns the configuration for the given Spacecraft.

    :param spacecraft_id: Identifier of the Spacecraft
    """
    return segment_serializers.serialize_sc_configuration(
        segments.Spacecraft.objects.get(identifier=spacecraft_id)
    )


@rpcmethod(
    name='configuration.sc.set',
    signature=['String', 'Object'],
    login_required=satnet_settings.JRPC_LOGIN_REQUIRED
)
def set_configuration(spacecraft_id, configuration):
    """JRPC test: configuration.sc.setConfiguration
    Returns the configuration for the given Spacecraft.

    :param spacecraft_id: Identifier of the Spacecraft
    :param configuration: Configuration object for the Ground Station
    """
    callsign, tle_id = segment_serializers.deserialize_sc_configuration(
        configuration
    )
    sc = segments.Spacecraft.objects.get(identifier=spacecraft_id)
    sc.update(callsign=callsign, tle_id=tle_id)
    return spacecraft_id


@rpcmethod(
    name='configuration.sc.delete',
    signature=['String'],
    login_required=satnet_settings.JRPC_LOGIN_REQUIRED
)
def delete(spacecraft_id):
    """JRPC test: configuration.sc.delete
    Deletes the ground station identified by the given Spacecraft. It also
    deletes all channels associated to this ground station.

    :param spacecraft_id: Identifier of the Spacecraft
    """
    segments.Spacecraft.objects.get(identifier=spacecraft_id).delete()
    return spacecraft_id
