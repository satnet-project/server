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

# ### TODO verify user permissions for certain actions.

__author__ = 'rtubiopa@calpoly.edu'

import logging
logger = logging.getLogger(__name__)

from rpc4django import rpcmethod
from configuration.models import AvailableModulations, AvailablePolarizations,\
    AvailableBitrates, AvailableBandwidths, AvailableBands,\
    GroundStationChannel, GroundStationConfiguration

# ### JSON keys for decoding data from the dictionary
__GS_ID_K = 'groundstation_id'
__IDENTIFIFER_K = 'name'
__MODULATIONS_K = 'modulations'
__BAND_K = 'band'
__POLARIZATIONS_K = 'polarizations'
__BITRATES_K = 'bitrates'
__BANDWIDTHS_K = 'bandwidths'


@rpcmethod(name='configuration.gs.channel.getOptions',
           signature=['String', 'Object'], login_required=True)
def gs_channel_get_options():
    """
    JRPC method.

    Returns a dictionary containing all the possible configuration
    options for adding a new communications channel to a Ground Station.
    """
    logger.debug(">>>>> " + __name__ + ": get_channel_options")

    results = {
        __BAND_K: [obj.get_band_name()
                   for obj in AvailableBands.objects.all()],
        __MODULATIONS_K: [obj.modulation
                          for obj in AvailableModulations.objects.all()],
        __POLARIZATIONS_K: [obj.polarization
                            for obj in AvailablePolarizations.objects.all()],
        __BITRATES_K: [obj.bitrate
                       for obj in AvailableBitrates.objects.all()],
        __BANDWIDTHS_K: [obj.bandwidth
                         for obj in AvailableBandwidths.objects.all()]
    }

    return results


@rpcmethod(name='configuration.gs.channel.uniqueIdentifier',
           signature=['String', 'Object'], login_required=True)
def gs_channel_unique_identifier(identifier):
    """
    JRPC method.

    Simple method that returns a boolean for indicating whether a channel for a
    ground station with the given identifier already exists.
    """

    logger.debug(">>>>> " + __name__ + ": gs_channel_unique_identifier")

    return GroundStationChannel.objects\
        .filter(identifier=identifier).count() > 0


@rpcmethod(name='configuration.gs.channel.create',
           signature=['String', 'Object'], login_required=True)
def gs_channel_create(ground_station_id, configuration):
    """
    JRPC callable method.

    Method that receives a configuration for a new channel to be added to the
    database. In case the channel could be added correctly to the database, it
    returns 'true'; otherwise, it raises an exception that is also returned.
    """

    # 1) Log RPC method access:
    logger.debug(">>>> " + __name__ + " gs_channel_create: " + str(
        configuration))

    # 2) Check channel configuration completeness
    check_channel_configuration(configuration)

    # 3) Get channel parameters from JSON representation into variables
    identifier, band_name, mod_l, bps_l, bws_l, pol_l = \
        get_channel_parameters(configuration)

    if GroundStationChannel.objects.filter(identifier=identifier).count() > 0:
        raise Exception("Channel identifier already exists, { "
                        + str(__IDENTIFIFER_K) + ": " + identifier + "}")

    # 4) Save object in the database. This method first gets all the pk's for
    # the related objects (channel parameters). Therefore, in case one of the
    # given objects does not exist, an exception will be raised.
    GroundStationChannel.objects\
        .create(gs_identifier=ground_station_id,
                identifier=identifier,
                band_name=band_name,
                modulations_list=mod_l,
                bitrates_list=bps_l,
                bandwidths_list=bws_l,
                polarizations_list=pol_l)

    return True


@rpcmethod(name='configuration.gs.channel.delete',
           signature=['String', 'String'], login_required=True)
def gs_channel_delete(ground_station_id, channel_id):
    """
    JRPC callable method.

    Method that removes the given channel from the database and from the list
    of available channels of the Ground Station that owns it.
    """

    # 1) Log RPC method access:
    logger.debug(">>>> " + __name__ + " gs_channel_delete: " + str(channel_id))

    # 2) Ground station channel removal through dedicated manager.
    GroundStationConfiguration.objects.delete_channel(ground_station_id,
                                                      channel_id)

    return True


@rpcmethod(name='configuration.gs.channel.getConfiguration',
           signature=['String', 'String'], login_required=True)
def gs_channel_get_configuration(ground_station_id, channel_id):
    """
    JRPC callable method.

    Method that can be used for retrieving a complete configuration for the
    requested channel.
    """
    # 1) Log RPC method access
    logger.debug(">>>> " + __name__ + " gs_channel_get_configuration: " +
                 str(channel_id))
    # 2) Retrieve objects from database
    gs, ch = GroundStationConfiguration.objects.get_channel(
        ground_station_id, channel_id)

    logger.debug('>>>>> ' + __name__ + ' ch = ' + str(ch.identifier))

    # 3) Return only the channel object
    return get_channel_configuration(ch)


@rpcmethod(name='configuration.gs.channel.setConfiguration',
           signature=['String', 'String', 'Object'], login_required=True)
def gs_channel_set_configuration(ground_station_id, channel_id, configuration):
    """
    JRPC callable method.

    Method that can be used for setting the configuration of an existing
    channel.

    Configuration can be incomplete, so that users may decide only to update
    some of the parameters of the channel.
    """

    # 1) Log RPC method access
    logger.debug(">>>> " + __name__ + " gs_channel_set_configuration: " +
                 str(channel_id))

    # 2) Retrieve objects from database
    gs, ch = GroundStationConfiguration.objects.get_channel(
        ground_station_id, channel_id)

    # 3) Parameters sent through JRPC as a list as decoded first.
    identifier, band_name, mod_l, bps_l, bws_l, pol_l = \
        get_channel_parameters(configuration)

    # 5) Update channel configuration
    ch.update(identifier=identifier,
              band_name=band_name,
              modulations_list=mod_l,
              bitrates_list=bps_l,
              bandwidths_list=bws_l,
              polarizations_list=pol_l)

    return True


def check_channel_configuration(configuration):
    """
    This method checks whether the given dictionary contains or not all the
    keys that are required for a valid channel configuration. In case it
    doesn't, an exception is raised.
    """

    if not __IDENTIFIFER_K in configuration:
        raise Exception("Parameter not provided, key = " + __IDENTIFIFER_K)
    if not __MODULATIONS_K in configuration:
        raise Exception("Parameter name not provided, key = " + __MODULATIONS_K)
    if not __POLARIZATIONS_K in configuration:
        raise Exception("Parameter name not provided, key = " +
                        __POLARIZATIONS_K)
    if not __BITRATES_K in configuration:
        raise Exception("Parameter name not provided, key = " + __BITRATES_K)
    if not __BAND_K in configuration:
        raise Exception("Parameter name not provided, key = " + __BAND_K)
    if not __BANDWIDTHS_K in configuration:
        raise Exception("Parameter name not provided, key = " + __BANDWIDTHS_K)


def get_channel_configuration(channel):
    """
    This method returns a dictionary with the key, value pairs containing
    the current configuration for the given channel object. The keys used are
    the ones required by the JRPC protocol.
    """

    results = {
        __IDENTIFIFER_K: channel.identifier,
        __BAND_K: channel.band.get_band_name(),
        __MODULATIONS_K: [obj.modulation
                          for obj in channel.modulation.all()],
        __POLARIZATIONS_K: [obj.polarization
                            for obj in channel.polarization.all()],
        __BITRATES_K: [obj.bitrate
                       for obj in channel.bitrate.all()],
        __BANDWIDTHS_K: [obj.bandwidth
                         for obj in channel.bandwidth.all()]
    }

    return results


def get_channel_parameters(configuration):
    """
    This method gets a list of the objects of the database based on the list
    of identifiers provided.
    """

    identifier = None
    band = None
    mod_l = []
    bps_l = []
    bws_l = []
    pol_l = []

    if __IDENTIFIFER_K in configuration:
        identifier = configuration[__IDENTIFIFER_K]
    if __BAND_K in configuration:
        band = AvailableBands.objects.get(band_name=configuration[__BAND_K])

    if __MODULATIONS_K in configuration:
        for e_i in configuration[__MODULATIONS_K]:
            mod_l.append(AvailableModulations.objects.get(modulation=e_i))
    if __BITRATES_K in configuration:
        for e_i in configuration[__BITRATES_K]:
            bps_l.append(AvailableBitrates.objects.get(bitrate=e_i))
    if __BANDWIDTHS_K in configuration:
        for e_i in configuration[__BANDWIDTHS_K]:
            bws_l.append(AvailableBandwidths.objects.get(bandwidth=e_i))
    if __POLARIZATIONS_K in configuration:
        for e_i in configuration[__POLARIZATIONS_K]:
            pol_l.append(AvailablePolarizations.objects.get(polarization=e_i))

    return identifier, band, mod_l, bps_l, bws_l, pol_l
