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
logger = logging.getLogger('configuration')
from django import db as django_db
from rpc4django import rpcmethod

from services.configuration.models import bands as band_models
from services.configuration.models import channels as channel_models
from services.configuration.models import segments as segment_models
from services.configuration.jrpc.serializers import channels as \
    jrpc_channels_serial
from website import settings as satnet_settings


@rpcmethod(
    name='configuration.gs.channel.list',
    signature=[],
    login_required=satnet_settings.JRPC_LOGIN_REQUIRED
)
def gs_channel_list(identifier):
    """JRPC method: configuration.gs.channel.list
    Simple method that returns the list of channels registered within this
    Ground Station.
    """
    channels = channel_models.GroundStationChannel.objects.filter(
        groundstation=segment_models.GroundStation.objects.get(
            identifier=identifier
        )
    )
    return [str(c.identifier) for c in channels]


@rpcmethod(
    name='configuration.gs.channel.unique',
    signature=['String'],
    login_required=satnet_settings.JRPC_LOGIN_REQUIRED
)
def gs_channel_is_unique(identifier):
    """JRPC method: configuration.gs.channel.isUnique
    Simple method that returns a boolean for indicating whether a channel for a
    ground station with the given identifier already exists.
    """
    return channel_models.GroundStationChannel.objects.filter(
        identifier=identifier
    ).count() > 0


@rpcmethod(
    name='configuration.gs.channel.create',
    signature=['String', 'String', 'Object'],
    login_required=satnet_settings.JRPC_LOGIN_REQUIRED
)
def gs_channel_create(groundstation_id, channel_id, configuration):
    """JRPC method: configuration.gs.channel.create
    Method that receives a configuration for a new channel to be added to the
    database. In case the channel could be added correctly to the database, it
    returns 'true'; otherwise, it raises an exception that is also returned.
    """
    # 1) Get channel parameters from JSON representation into variables
    band_name, automated, mod_l, bps_l, bws_l, pol_l =\
        jrpc_channels_serial.deserialize_gs_channel_parameters(configuration)

    try:

        channel_models.GroundStationChannel.objects.create(
            identifier=channel_id,
            groundstation=segment_models.GroundStation.objects.get(
                identifier=groundstation_id
            ),
            band=band_models.AvailableBands.objects.get(
                band_name=band_name
            ),
            automated=automated,
            modulations=mod_l,
            bitrates=bps_l,
            bandwidths=bws_l,
            polarizations=pol_l
        )

    except segment_models.GroundStation.DoesNotExist as ex:
        logger.warn(str(ex))
        raise Exception(
            'GroundStation identifier does not exist, id = <' + str(
                groundstation_id
            ) + '>'
        )

    except django_db.IntegrityError as ex:
        logger.warn(str(ex))
        raise Exception(
            "Channel identifier already exists, { "
            + str(jrpc_channels_serial.CH_ID_K) + ": "
            + str(channel_id) + "}"
        )

    # 2) Returns true or throws exception
    return True


@rpcmethod(
    name='configuration.gs.channel.get',
    signature=['String', 'String'],
    login_required=satnet_settings.JRPC_LOGIN_REQUIRED
)
def gs_channel_get_configuration(groundstation_id, channel_id):
    """JRPC method: configuration.gs.channel.getConfiguration
    Method that can be used for retrieving a complete configuration for the
    requested channel.
    """
    return jrpc_channels_serial.serialize_gs_channel_configuration(
        channel_models.GroundStationChannel.objects.get(
            identifier=channel_id,
            groundstation=segment_models.GroundStation.objects.get(
                identifier=groundstation_id
            )
        )
    )


@rpcmethod(
    name='configuration.gs.channel.set',
    signature=['String', 'String', 'Object'],
    login_required=satnet_settings.JRPC_LOGIN_REQUIRED
)
def gs_channel_set_configuration(groundstation_id, channel_id, configuration):
    """JRPC method: configuration.gs.channel.setConfiguration
    Method that can be used for setting the configuration of an existing
    channel. Configuration can be incomplete, so that users may decide only
    to update some of the parameters of the channel.
    """
    # 1) Retrieve objects from database
    ch = channel_models.GroundStationChannel.objects.get(
        identifier=channel_id,
        groundstation=segment_models.GroundStation.objects.get(
            identifier=groundstation_id
        )
    )
    # 2) Parameters sent through JRPC as a list as decoded first.
    band_name, automated, mod_l, bps_l, bws_l, pol_l =\
        jrpc_channels_serial.deserialize_gs_channel_parameters(configuration)
    band = band_models.AvailableBands.objects.get(band_name=band_name)
    # 3) Update channel configuration
    ch.update(
        band=band,
        automated=automated,
        modulations_list=mod_l,
        bitrates_list=bps_l,
        bandwidths_list=bws_l,
        polarizations_list=pol_l
    )
    return True


@rpcmethod(
    name='configuration.gs.channel.delete',
    signature=['String', 'String'],
    login_required=satnet_settings.JRPC_LOGIN_REQUIRED
)
def gs_channel_delete(groundstation_id, channel_id):
    """JRPC method: configuration.gs.channel.delete
    Method that removes the given channel from the database and from the list
    of available channels of the Ground Station that owns it.
    """
    channel_models.GroundStationChannel.objects.get(
        identifier=channel_id,
        groundstation=segment_models.GroundStation.objects.get(
            identifier=groundstation_id
        )
    ).delete()

    return True
