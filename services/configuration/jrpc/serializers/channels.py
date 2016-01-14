"""
   Copyright 2013, 2014 Ricardo Tubio-Pardavila
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

from preserialize.serialize import serialize

from services.configuration.models import bands as band_models


CHANNEL_LIST_K = 'segment_channels'

# ### JSON keys for decoding data from the dictionary
CH_ID_K = 'channel_id'
# ## Keys only for GroundStation channel parameters
BAND_K = 'band'
BANDS_K = 'bands'
MODULATIONS_K = 'modulations'
POLARIZATIONS_K = 'polarizations'
BITRATES_K = 'bitrates'
BANDWIDTHS_K = 'bandwidths'
AUTOMATED_K = 'automated'
# ### Keys only for Spacecraft Channel parameters
FREQUENCY_K = 'frequency'
MODULATION_K = 'modulation'
POLARIZATION_K = 'polarization'
BITRATE_K = 'bitrate'
BANDWIDTH_K = 'bandwidth'


def serialize_channels(channel_list):
    """
    Transform a list of channels into a JSON-like array with the identifiers
    of the channels.
    :param channel_list: list with the channel objects from the database.
    :return: JSON-like array with the identifiers of the channels.
    """
    return {
        CHANNEL_LIST_K: [c.identifier for c in channel_list]
    }


def check_gs_channel_configuration(configuration):
    """
    This method checks whether the given dictionary contains or not all the
    keys that are required for a valid channel configuration. In case it
    doesn't, an exception is raised.

    :param configuration: Configuration object
    """
    if BAND_K not in configuration:
        raise Exception("Parameter not provided, key = " + BAND_K)
    if MODULATIONS_K not in configuration:
        raise Exception("Parameter not provided, key = " + MODULATIONS_K)
    if POLARIZATIONS_K not in configuration:
        raise Exception("Parameter not provided, key = " + POLARIZATIONS_K)
    if BITRATES_K not in configuration:
        raise Exception("Parameter not provided, key = " + BITRATES_K)
    if BANDWIDTHS_K not in configuration:
        raise Exception("Parameter not provided, key = " + BANDWIDTHS_K)
    if AUTOMATED_K not in configuration:
        raise Exception("Parameter not provided, key = " + AUTOMATED_K)


def check_sc_channel_configuration(configuration):
    """
    This method checks whether the given dictionary contains or not all the
    keys that are required for a valid channel configuration. In case it
    doesn't, an exception is raised.

    :param configuration: Configuration object
    """
    if FREQUENCY_K not in configuration:
        raise Exception("Parameter not provided, key = " + FREQUENCY_K)
    if MODULATION_K not in configuration:
        raise Exception("Parameter not provided, key = " + MODULATION_K)
    if POLARIZATION_K not in configuration:
        raise Exception("Parameter not provided, key = " + POLARIZATION_K)
    if BITRATE_K not in configuration:
        raise Exception("Parameter not provided, key = " + BITRATE_K)
    if BANDWIDTH_K not in configuration:
        raise Exception("Parameter not provided, key = " + BANDWIDTH_K)


def serialize_gs_channel_configuration(channel):
    """
    This method returns a dictionary with the key, value pairs containing
    the current configuration for the given channel object. The keys used are
    the ones required by the JRPC protocol.

    :param channel: Channel object
    """
    return {
        CH_ID_K: channel.identifier,
        BAND_K: channel.band.get_band_name(),
        AUTOMATED_K: channel.automated,
        MODULATIONS_K: sorted(
            [obj.modulation for obj in channel.modulations.all()]
        ),
        POLARIZATIONS_K: sorted(
            [obj.polarization for obj in channel.polarizations.all()]
        ),
        BITRATES_K: sorted(
            [obj.bitrate for obj in channel.bitrates.all()]
        ),
        BANDWIDTHS_K: sorted(
            [obj.bandwidth for obj in channel.bandwidths.all()]
        )
    }


def serialize_sc_channel_configuration(channel):
    """
    This method returns a dictionary with the key, value pairs containing
    the current configuration for the given channel object. The keys used are
    the ones required by the JRPC protocol.

    :param channel: Channel object
    """
    return {
        CH_ID_K: channel.identifier,
        FREQUENCY_K: channel.frequency,
        MODULATION_K: channel.modulation.modulation,
        POLARIZATION_K: channel.polarization.polarization,
        BITRATE_K: channel.bitrate.bitrate,
        BANDWIDTH_K: channel.bandwidth.bandwidth
    }


def deserialize_sc_channel_parameters(configuration):
    """
    Spacecraft channel parameters are returned from within the configuration
    structure passed as first parameter.

    :param configuration: The configuration structure with all the data
    :return: Tuple containing all parameters as separate variables
    """
    check_sc_channel_configuration(configuration)

    return configuration[FREQUENCY_K], \
        band_models.AvailableModulations.objects.get(
            modulation=configuration[MODULATION_K]
    ), \
        band_models.AvailableBitrates.objects.get(
            bitrate=configuration[BITRATE_K]
    ),\
        band_models.AvailableBandwidths.objects.get(
            bandwidth=configuration[BANDWIDTH_K]
    ),\
        band_models.AvailablePolarizations.objects.get(
            polarization=configuration[POLARIZATION_K]
    )


def deserialize_gs_channel_parameters(configuration):
    """
    This method gets a list of the objects of the database based on the list
    of identifiers provided.
    :param configuration: The configuration structure with all the data.
    :return: Tuple containing all parameters as separate variables.
    """
    check_gs_channel_configuration(configuration)

    mod_l = []
    bps_l = []
    bws_l = []
    pol_l = []

    for e_i in configuration[MODULATIONS_K]:
        mod_l.append(
            band_models.AvailableModulations.objects.get(modulation=e_i)
        )
    for e_i in configuration[BITRATES_K]:
        bps_l.append(
            band_models.AvailableBitrates.objects.get(bitrate=e_i)
        )
    for e_i in configuration[BANDWIDTHS_K]:
        bws_l.append(
            band_models.AvailableBandwidths.objects.get(bandwidth=e_i)
        )
    for e_i in configuration[POLARIZATIONS_K]:
        pol_l.append(
            band_models.AvailablePolarizations.objects.get(polarization=e_i)
        )

    return (
        configuration[BAND_K],
        configuration[AUTOMATED_K],
        mod_l, bps_l, bws_l, pol_l
    )


def serialize_sc_channel(sc_channel, exclude_fields=None):
    """JSON serializer
    Serializes the given spacecraft channel.
    :param sc_channel: The Spacecraft channel object to be serialized
    :param exclude_fields: List of fields to be excluded from the object
    :return: JSON serialization
    """
    if not exclude_fields:
        exclude_fields = ['id', 'spacecraft']

    return serialize(
        sc_channel, camelcase=True, exclude=exclude_fields,
        related={
            'modulation': {'fields': ['modulation']},
            'bandwidth': {'fields': ['bandwidth']},
            'bitrate': {'fields': ['bitrate']},
            'polarization': {'fields': ['polarization']}
        }
    )


def serialize_gs_channel(gs_channel, exclude_fields=None):
    """JSON serializer
    Serializes the given groundstation channel.
    :param gs_channel: The Ground Station channel object to be serialized
    :param exclude_fields: List of fields to be excluded from the object
    :return: JSON serialization
    """
    if not exclude_fields:
        exclude_fields = ['id', 'groundstation']

    return serialize(
        gs_channel, camelcase=True, exclude=exclude_fields,
        related={
            'band': {
                'fields': [
                    'IARU_allocation_minimum_frequency',
                    'IARU_allocation_maximum_frequency',
                    'uplink',
                    'downlink'
                ],
                'aliases': {
                    'min_freq': 'IARU_allocation_minimum_frequency',
                    'max_freq': 'IARU_allocation_maximum_frequency'
                }
            },
            'modulations': {
                'fields': ['modulation']
            },
            'bandwidths': {
                'fields': ['bandwidth']
            },
            'bitrates': {
                'fields': ['bitrate']
            },
            'polarizations': {
                'fields': ['polarization']
            }
        }
    )
