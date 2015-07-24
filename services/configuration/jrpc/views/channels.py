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

from services.configuration.models import segments, bands, channels
from services.configuration.jrpc.serializers import serialization
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
    gs = segments.GroundStation.objects.get(identifier=identifier)
    return [str(c.identifier) for c in gs.channels.all()]


@rpcmethod(
    name='configuration.channels.getOptions',
    signature=[],
    login_required=satnet_settings.JRPC_LOGIN_REQUIRED
)
def get_options():
    """JRPC method: configuration.channels.getOptions
    Returns a dictionary containing all the possible configuration
    options for adding a new communications channel to a Ground Station.
    """
    return {
        serialization.BANDS_K: [
            obj.get_band_name()
            for obj in bands.AvailableBands.objects.all()
        ],
        serialization.MODULATIONS_K: [
            obj.modulation
            for obj in bands.AvailableModulations.objects.all()
        ],
        serialization.POLARIZATIONS_K: [
            obj.polarization
            for obj in bands.AvailablePolarizations.objects.all()
        ],
        serialization.BITRATES_K: [
            str(obj.bitrate)
            for obj in bands.AvailableBitrates.objects.all()
        ],
        serialization.BANDWIDTHS_K: [
            str(obj.bandwidth)
            for obj in bands.AvailableBandwidths.objects.all()
        ]
    }


@rpcmethod(
    name='configuration.gs.channel.isUnique',
    signature=['String'],
    login_required=satnet_settings.JRPC_LOGIN_REQUIRED
)
def gs_channel_is_unique(identifier):
    """JRPC method: configuration.gs.channel.isUnique
    Simple method that returns a boolean for indicating whether a channel for a
    ground station with the given identifier already exists.
    """
    return channels.GroundStationChannel.objects.filter(
        identifier=identifier
    ).count() > 0


@rpcmethod(
    name='configuration.gs.channel.create',
    signature=['String', 'String', 'Object'],
    login_required=satnet_settings.JRPC_LOGIN_REQUIRED
)
def gs_channel_create(ground_station_id, channel_id, configuration):
    """JRPC method: configuration.gs.channel.create
    Method that receives a configuration for a new channel to be added to the
    database. In case the channel could be added correctly to the database, it
    returns 'true'; otherwise, it raises an exception that is also returned.
    """
    # 1) Get channel parameters from JSON representation into variables
    band_name, automated, mod_l, bps_l, bws_l, pol_l =\
        serialization.deserialize_gs_channel_parameters(configuration)
    if channels.GroundStationChannel.objects.filter(
        identifier=channel_id
    ).count() > 0:
        raise Exception(
            "Channel identifier already exists, { "
            + str(serialization.CH_ID_K) + ": "
            + str(channel_id) + "}"
        )
    # 2) Save object in the database. This method first gets all the pk's for
    # the related objects (channel parameters). Therefore, in case one of the
    # given objects does not exist, an exception will be raised.
    segments.GroundStation.objects.add_channel(
        gs_identifier=ground_station_id,
        identifier=channel_id,
        band=bands.AvailableBands.objects.get(band_name=band_name),
        automated=automated,
        modulations=mod_l,
        bitrates=bps_l,
        bandwidths=bws_l,
        polarizations=pol_l
    )
    # 5) Returns true or throws exception
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
    segments.GroundStation.objects.get(
        identifier=groundstation_id
    ).channels.all().get(
        identifier=channel_id
    ).delete()
    return True


@rpcmethod(
    name='configuration.gs.channel.getConfiguration',
    signature=['String', 'String'],
    login_required=satnet_settings.JRPC_LOGIN_REQUIRED
)
def gs_channel_get_configuration(groundstation_id, channel_id):
    """JRPC method: configuration.gs.channel.getConfiguration
    Method that can be used for retrieving a complete configuration for the
    requested channel.
    """
    return serialization.serialize_gs_channel_configuration(
        segments.GroundStation.objects.get(
            identifier=groundstation_id
        ).channels.all().get(
            identifier=channel_id
        )
    )


@rpcmethod(
    name='configuration.gs.channel.setConfiguration',
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
    ch = segments.GroundStation.objects.get(
        identifier=groundstation_id
    ).channels.all().get(
        identifier=channel_id
    )
    # 2) Parameters sent through JRPC as a list as decoded first.
    band_name, automated, mod_l, bps_l, bws_l, pol_l =\
        serialization.deserialize_gs_channel_parameters(configuration)
    band = bands.AvailableBands.objects.get(band_name=band_name)
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
    name='configuration.sc.channel.list',
    signature=[],
    login_required=satnet_settings.JRPC_LOGIN_REQUIRED
)
def sc_channel_list(identifier):
    """JRPC method: configuration.sc.channel.list
    Simple method that returns the list of channels registered within this
    Spacecraft.
    """
    sc = segments.Spacecraft.objects.get(identifier=identifier)
    return [str(c.identifier) for c in sc.channels.all()]


@rpcmethod(
    name='configuration.sc.channel.isUnique',
    signature=['String'],
    login_required=satnet_settings.JRPC_LOGIN_REQUIRED
)
def sc_channel_is_unique(identifier):
    """JRPC method: configuration.sc.channel.isUnique
    Simple method that returns a boolean for indicating whether a channel for a
    ground station with the given identifier already exists.
    """
    return channels.SpacecraftChannel.objects.filter(
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
    """

    # 1) Get channel parameters from JSON representation into variables
    frequency, modulation, bitrate, bandwidth, polarization\
        = serialization.deserialize_sc_channel_parameters(configuration)

    if channels.SpacecraftChannel.objects.filter(
        identifier=channel_id
    ).count() > 0:
        raise Exception(
            'Channel identifier already exists, { '
            + str(serialization.CH_ID_K) + ': '
            + str(channel_id) + '}'
        )

    # 2) Save object in the database. This method first gets all the pk's for
    # the related objects (channel parameters). Therefore, in case one of the
    # given objects does not exist, an exception will be raised.
    segments.Spacecraft.objects.add_channel(
        sc_identifier=spacecraft_id,
        identifier=channel_id,
        frequency=frequency,
        modulation=modulation,
        bitrate=bitrate,
        bandwidth=bandwidth,
        polarization=polarization
    )

    # 3) Returns true or throws exception
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
    """
    segments.Spacecraft.objects.get(
        identifier=spacecraft_id
    ).channels.all().get(
        identifier=channel_id
    ).delete()
    return True


@rpcmethod(
    name='configuration.sc.channel.getConfiguration',
    signature=['String', 'String'],
    login_required=satnet_settings.JRPC_LOGIN_REQUIRED
)
def sc_channel_get_configuration(spacecraft_id, channel_id):
    """JRPC method: configuration.sc.channel.getConfiguration
    Method that can be used for retrieving a complete configuration for the
    requested channel.
    """
    return serialization.serialize_sc_channel_configuration(
        segments.Spacecraft.objects.get(
            identifier=spacecraft_id
        ).channels.all().get(
            identifier=channel_id
        )
    )


@rpcmethod(
    name='configuration.sc.channel.setConfiguration',
    signature=['String', 'String', 'Object'],
    login_required=satnet_settings.JRPC_LOGIN_REQUIRED
)
def sc_channel_set_configuration(spacecraft_id, channel_id, configuration):
    """JRPC method: configuration.sc.channel.setConfiguration
    Method that can be used for setting the configuration of an existing
    channel. Configuration can be incomplete, so that users may decide only
    to update some of the parameters of the channel.
    """
    # 1) Retrieve objects from database
    ch = segments.Spacecraft.objects.get(
        identifier=spacecraft_id
    ).channels.all().get(
        identifier=channel_id
    )
    # 2) Parameters sent through JRPC as a list as decoded first.
    frequency, modulation, bitrate, bandwidth, polarization =\
        serialization.deserialize_sc_channel_parameters(configuration)
    # 3) Update channel configuration
    ch.update(
        frequency=frequency,
        modulation=modulation,
        bitrate=bitrate,
        bandwidth=bandwidth,
        polarization=polarization
    )
    return True
