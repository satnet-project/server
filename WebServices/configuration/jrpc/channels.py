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

# ### TODO verify user permissions for certain actions.

from rpc4django import rpcmethod

from configuration.models.channels import GroundStationChannel,\
    SpacecraftChannel
from configuration.models.bands import AvailableModulations,\
    AvailablePolarizations, AvailableBitrates, AvailableBandwidths,\
    AvailableBands
from configuration.models.segments import GroundStation,\
    Spacecraft
from configuration.jrpc.serialization import\
    serialize_gs_channel_configuration, serialize_sc_channel_configuration,\
    deserialize_sc_channel_parameters, deserialize_gs_channel_parameters,\
    CH_ID_K, MODULATIONS_K, BAND_K, POLARIZATIONS_K,\
    BITRATES_K, BANDWIDTHS_K


@rpcmethod(
    name='configuration.channels.getOptions',
    signature=[],
    login_required=True
)
def get_options():
    """
    JRPC method.

    Returns a dictionary containing all the possible configuration
    options for adding a new communications channel to a Ground Station.
    """
    return {
        BAND_K: [
            obj.get_band_name() for obj in AvailableBands.objects.all()
        ],
        MODULATIONS_K: [
            obj.modulation for obj in AvailableModulations.objects.all()
        ],
        POLARIZATIONS_K: [
            obj.polarization for obj in AvailablePolarizations.objects.all()
        ],
        BITRATES_K: [
            str(obj.bitrate) for obj in AvailableBitrates.objects.all()
        ],
        BANDWIDTHS_K: [
            str(obj.bandwidth) for obj in AvailableBandwidths.objects.all()
        ]
    }


@rpcmethod(
    name='configuration.gs.channel.isUnique',
    signature=['String'],
    login_required=True
)
def gs_channel_is_unique(identifier):
    """
    JRPC method.

    Simple method that returns a boolean for indicating whether a channel for a
    ground station with the given identifier already exists.
    """
    return GroundStationChannel.objects\
        .filter(identifier=identifier).count() > 0


@rpcmethod(
    name='configuration.gs.channel.create',
    signature=['String', 'String', 'Object'],
    login_required=True
)
def gs_channel_create(ground_station_id, channel_id, configuration):
    """
    JRPC callable method.

    Method that receives a configuration for a new channel to be added to the
    database. In case the channel could be added correctly to the database, it
    returns 'true'; otherwise, it raises an exception that is also returned.
    """
    # 1) Get channel parameters from JSON representation into variables
    band_name, mod_l, bps_l, bws_l, pol_l =\
        deserialize_gs_channel_parameters(configuration)
    if GroundStationChannel.objects.filter(identifier=channel_id).count() > 0:
        raise Exception(
            "Channel identifier already exists, { "
            + str(CH_ID_K) + ": "
            + str(channel_id) + "}"
        )
    # 2) Save object in the database. This method first gets all the pk's for
    # the related objects (channel parameters). Therefore, in case one of the
    # given objects does not exist, an exception will be raised.
    GroundStation.objects.add_channel(
        gs_identifier=ground_station_id,
        identifier=channel_id,
        band=AvailableBands.objects.get(band_name=band_name),
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
    login_required=True
)
def gs_channel_delete(ground_station_id, channel_id):
    """
    JRPC callable method.

    Method that removes the given channel from the database and from the list
    of available channels of the Ground Station that owns it.
    """
    GroundStation.objects.delete_channel(
        ground_station_id, channel_id
    )
    return True


@rpcmethod(
    name='configuration.gs.channel.getConfiguration',
    signature=['String', 'String'],
    login_required=True
)
def gs_channel_get_configuration(ground_station_id, channel_id):
    """
    JRPC callable method.

    Method that can be used for retrieving a complete configuration for the
    requested channel.
    """
    return serialize_gs_channel_configuration(
        GroundStation.objects.get_channel(
            ground_station_id, channel_id
        )
    )


@rpcmethod(
    name='configuration.gs.channel.setConfiguration',
    signature=['String', 'String', 'Object'],
    login_required=True
)
def gs_channel_set_configuration(ground_station_id, channel_id, configuration):
    """
    JRPC callable method.

    Method that can be used for setting the configuration of an existing
    channel. Configuration can be incomplete, so that users may decide only
    to update some of the parameters of the channel.
    """
    # 1) Retrieve objects from database
    ch = GroundStation.objects.get_channel(
        ground_station_id, channel_id
    )
    # 2) Parameters sent through JRPC as a list as decoded first.
    band_name, mod_l, bps_l, bws_l, pol_l =\
        deserialize_gs_channel_parameters(configuration)
    band = AvailableBands.objects.get(band_name=band_name)
    # 3) Update channel configuration
    ch.update(
        band=band,
        modulations_list=mod_l,
        bitrates_list=bps_l,
        bandwidths_list=bws_l,
        polarizations_list=pol_l
    )
    return True


@rpcmethod(
    name='configuration.sc.channel.isUnique',
    signature=['String'],
    login_required=True
)
def sc_channel_is_unique(identifier):
    """
    JRPC method.

    Simple method that returns a boolean for indicating whether a channel for a
    ground station with the given identifier already exists.
    """
    return SpacecraftChannel.objects.filter(identifier=identifier).count() > 0


@rpcmethod(
    name='configuration.sc.channel.create',
    signature=['String', 'String', 'Object'],
    login_required=True
)
def sc_channel_create(spacecraft_id, channel_id, configuration):
    """
    JRPC callable method.

    Method that receives a configuration for a new channel to be added to the
    database. In case the channel could be added correctly to the database, it
    returns 'true'; otherwise, it raises an exception that is also returned.
    """
    # 1) Get channel parameters from JSON representation into variables
    frequency, modulation, bitrate, bandwidth, polarization\
        = deserialize_sc_channel_parameters(configuration)

    if SpacecraftChannel.objects.filter(identifier=channel_id).count() > 0:
        raise Exception(
            "Channel identifier already exists, { "
            + str(CH_ID_K) + ": "
            + str(channel_id) + "}"
        )
    # 2) Save object in the database. This method first gets all the pk's for
    # the related objects (channel parameters). Therefore, in case one of the
    # given objects does not exist, an exception will be raised.
    Spacecraft.objects.add_channel(
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
    login_required=True
)
def sc_channel_delete(spacecraft_id, channel_id):
    """
    JRPC callable method.

    Method that removes the given channel from the database and from the list
    of available channels of the SpacecraftConfiguration object that owns it.
    """
    Spacecraft.objects.delete_channel(
        spacecraft_id, channel_id
    )
    return True


@rpcmethod(
    name='configuration.sc.channel.getConfiguration',
    signature=['String', 'String'],
    login_required=True
)
def sc_channel_get_configuration(spacecraft_id, channel_id):
    """
    JRPC callable method.

    Method that can be used for retrieving a complete configuration for the
    requested channel.
    """
    return serialize_sc_channel_configuration(
        Spacecraft.objects.get_channel(spacecraft_id, channel_id)
    )


@rpcmethod(
    name='configuration.sc.channel.setConfiguration',
    signature=['String', 'String', 'Object'],
    login_required=True
)
def sc_channel_set_configuration(spacecraft_id, channel_id, configuration):
    """
    JRPC callable method.

    Method that can be used for setting the configuration of an existing
    channel. Configuration can be incomplete, so that users may decide only
    to update some of the parameters of the channel.
    """
    # 1) Retrieve objects from database
    ch = Spacecraft.objects.get_channel(
        spacecraft_id, channel_id
    )
    # 2) Parameters sent through JRPC as a list as decoded first.
    frequency, modulation, bitrate, bandwidth, polarization =\
        deserialize_sc_channel_parameters(configuration)
    # 3) Update channel configuration
    ch.update(
        frequency=frequency,
        modulation=modulation,
        bitrate=bitrate,
        bandwidth=bandwidth,
        polarization=polarization
    )
    return True