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
logger = logging.getLogger(__name__)

from rpc4django import rpcmethod
from configuration.models import AvailableModulations, AvailablePolarizations, \
    AvailableBitrates, AvailableBandwidths, AvailableBands,\
    GroundStationChannel

# ### JSON keys for decoding data from the dictionary
__GS_ID_K = 'groundstation_id'
__NAME_K = 'name'
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

    return GroundStationChannel.objects.\
        filter(identifier=identifier).count() > 0


@rpcmethod(name='configuration.gs.channel.create',
           signature=['String', 'Object'], login_required=True)
def gs_channel_create(configuration):
    """
    JRPC callable method.

    Method that receives a configuration for a new channel to be added to the
    database. In case the channel could be added correctly to the database, it
    returns 'true'; otherwise, it raises an exception that is also returned.
    """

    # 1) Check configuration structure correctness
    logger.debug(__name__ + ">>>> " + str(configuration))

    if not __GS_ID_K in configuration:
        raise Exception("Parameter not provided, key = " + __GS_ID_K)
    if not __NAME_K in configuration:
        raise Exception("Parameter not provided, key = " + __NAME_K)
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

    # 2) Check channel name uniqueness
    if GroundStationChannel.objects.filter(identifier=configuration[__NAME_K]).\
            count() > 0:
        raise Exception("Channel name already exists, { "
                        + str(__NAME_K) + ": " + configuration[__NAME_K] + "}")

    # 3) By getting the band object we are also checking whether the band
    # exists or not. In case it does not exist or its object cannot be
    # retrieved using the provided information, an exception is raised
    band = AvailableBands.objects.get(band_name=configuration[__BAND_K])

    # 4) Save object in the database. This method first gets all the pk's for
    # the related objects (channel parameters). Therefore, in case one of the
    # given objects does not exist, an exception will be raised.
    GroundStationChannel.objects\
        .create(gs_identifier=configuration[__GS_ID_K],
                identifier=configuration[__NAME_K],
                band=band,
                modulations_list=configuration[__MODULATIONS_K],
                bitrates_list=configuration[__BITRATES_K],
                bandwidths_list=configuration[__BANDWIDTHS_K],
                polarizations_list=configuration[__POLARIZATIONS_K])

    return True
