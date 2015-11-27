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
from django import db as django_db
from rpc4django import rpcmethod

from services.configuration.models import channels as channel_models
from services.configuration.models import segments as segment_models
from services.configuration.jrpc.serializers import channels as \
    jrpc_channels_serial
from website import settings as satnet_settings


logger = logging.getLogger('configuration')


@rpcmethod(
    name='configuration.sc.channel.list',
    signature=[],
    login_required=satnet_settings.JRPC_LOGIN_REQUIRED
)
def sc_channel_list(identifier):
    """JRPC method: configuration.sc.channel.list
    Simple method that returns the list of channels registered within this
    Spacecraft.

    :param identifier: Identifier of the Spacecraft
    """
    channels = channel_models.SpacecraftChannel.objects.filter(
        spacecraft=segment_models.Spacecraft.objects.get(
            identifier=identifier
        )
    )
    return [str(c.identifier) for c in channels]


@rpcmethod(
    name='configuration.sc.channel.unique',
    signature=['String'],
    login_required=satnet_settings.JRPC_LOGIN_REQUIRED
)
def sc_channel_is_unique(identifier):
    """JRPC method: configuration.sc.channel.isUnique
    Simple method that returns a boolean for indicating whether a channel for a
    ground station with the given identifier already exists.

    :param identifier: Identifier of the Spacecraft Channel
    """
    return channel_models.SpacecraftChannel.objects.filter(
        identifier=identifier
    ).count() > 0


@rpcmethod(
    name='configuration.sc.channel.create',
    signature=['String', 'String', 'Object'],
    login_required=satnet_settings.JRPC_LOGIN_REQUIRED
)
def sc_channel_create(spacecraft_id, channel_id, configuration):
    """JRPC method: configuration.sc.channel.create
    Method that receives a configuration for a new channel to be added to the
    database. In case the channel could be added correctly to the database, it
    returns 'true'; otherwise, it raises an exception that is also returned.

    :param spacecraft_id: Identifier of the Spacecraft
    :param channel_id: Identifier of the Channel
    :param configuration: Configuration object for the Channel
    """
    # 1) Get channel parameters from JSON representation into variables
    frequency, modulation, bitrate, bandwidth, polarization\
        = jrpc_channels_serial.deserialize_sc_channel_parameters(configuration)

    try:
        channel_models.SpacecraftChannel.objects.create(
            identifier=channel_id,
            spacecraft=segment_models.Spacecraft.objects.get(
                identifier=spacecraft_id
            ),
            frequency=frequency,
            modulation=modulation,
            bitrate=bitrate,
            bandwidth=bandwidth,
            polarization=polarization
        )

    except segment_models.Spacecraft.DoesNotExist as ex:
        logger.warn(str(ex))
        raise Exception(
            'Spacecraft identifier does not exist, id = <' + str(
                spacecraft_id
            ) + '>'
        )

    except django_db.IntegrityError as ex:
        logger.warn(str(ex))
        raise Exception(
            "Channel identifier already exists, { " + str(
                jrpc_channels_serial.CH_ID_K
            ) + ": " + str(channel_id) + "}"
        )

    # 2) Returns true or throws exception
    return True


@rpcmethod(
    name='configuration.sc.channel.get',
    signature=['String', 'String'],
    login_required=satnet_settings.JRPC_LOGIN_REQUIRED
)
def sc_channel_get_configuration(spacecraft_id, channel_id):
    """JRPC method: configuration.sc.channel.getConfiguration
    Method that can be used for retrieving a complete configuration for the
    requested channel.

    :param spacecraft_id: Identifier of the Spacecraft
    :param channel_id: Identifier of the Channel
    """
    return jrpc_channels_serial.serialize_sc_channel_configuration(
        channel_models.SpacecraftChannel.objects.get(
            identifier=channel_id,
            spacecraft=segment_models.Spacecraft.objects.get(
                identifier=spacecraft_id
            )
        )
    )


@rpcmethod(
    name='configuration.sc.channel.set',
    signature=['String', 'String', 'Object'],
    login_required=satnet_settings.JRPC_LOGIN_REQUIRED
)
def sc_channel_set_configuration(spacecraft_id, channel_id, configuration):
    """JRPC method: configuration.sc.channel.setConfiguration
    Method that can be used for setting the configuration of an existing
    channel. Configuration can be incomplete, so that users may decide only
    to update some of the parameters of the channel.

    :param spacecraft_id: Identifier of the Spacecraft
    :param channel_id: Identifier of the Channel
    :param configuration: Configuration object for the Channel
    """
    # 1) Retrieve objects from database
    ch = channel_models.SpacecraftChannel.objects.get(
        identifier=channel_id,
        spacecraft=segment_models.Spacecraft.objects.get(
            identifier=spacecraft_id
        )
    )
    # 2) Parameters sent through JRPC as a list as decoded first.
    frequency, modulation, bitrate, bandwidth, polarization =\
        jrpc_channels_serial.deserialize_sc_channel_parameters(configuration)
    # 3) Update channel configuration
    ch.update(
        frequency=frequency,
        modulation=modulation,
        bitrate=bitrate,
        bandwidth=bandwidth,
        polarization=polarization
    )
    return True


@rpcmethod(
    name='configuration.sc.channel.delete',
    signature=['String', 'String'],
    login_required=satnet_settings.JRPC_LOGIN_REQUIRED
)
def sc_channel_delete(spacecraft_id, channel_id):
    """JRPC method: configuration.sc.channel.delete
    Method that removes the given channel from the database and from the list
    of available channels of the SpacecraftConfiguration object that owns it.

    :param spacecraft_id: Identifier of the Spacecraft
    :param channel_id: Identifier of the Channel
    """
    try:
        channel_models.SpacecraftChannel.objects.get(
            identifier=channel_id,
            spacecraft=segment_models.Spacecraft.objects.get(
                identifier=spacecraft_id
            )
        ).delete()

    except segment_models.Spacecraft.DoesNotExist as ex:
        logger.warn(str(ex))
        raise Exception(
            'Spacecraft identifier does not exist, id = <' + str(
                spacecraft_id
            ) + '>'
        )

    return True
