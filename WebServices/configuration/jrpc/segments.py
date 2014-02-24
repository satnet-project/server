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
from rpc4django import rpcmethod
from configuration.models.segments import GroundStationConfiguration
logger = logging.getLogger(__name__)

# ### JSON keys for enconding/decoding dictionaries
__GS_ID_K = 'groundstation_id'
__GS_LATLON_K = 'groundstation_latlon'
__GS_CALLSIGN_K = 'groundstation_callsign'
__GS_ELEVATION_K = 'groundstation_elevation'
__GS_CHANNELS = 'groundstation_channels'

@rpcmethod(name='configuration.gs.delete',
           signature=[], login_required=True)
def gs_list(**kwargs):
    """
    JRPC method.

    Creates a list with the identifiers of the available ground stations for
    the user that is requesting the service.
    """

    # 1) user must be obtained from the request, since this has already been
    #       validated by the authentication backend
    http_request = kwargs.get('request', None)
    gs_objects = GroundStationConfiguration.objects\
        .filter(user=http_request.user)\
        .all()
    return [str(g.identifier) for g in gs_objects]


@rpcmethod(name='configuration.gs.getConfiguration',
           signature=['String'], login_required=True)
def gs_get_configuration(ground_station_id):
    """
    JRPC method.

    Returns the configuration for the given ground station.
    """
    logger.debug(">>>>> " + __name__ + ": gs_get_configuration")
    gs = GroundStationConfiguration.objects.get(identifier=ground_station_id)
    return serialize_gs_configuration(gs)


@rpcmethod(name='configuration.gs.setConfiguration',
           signature=['String', 'Object'], login_required=True)
def gs_set_configuration(ground_station_id, configuration):
    """
    JRPC method.

    Returns the configuration for the given ground station.
    """
    logger.debug(">>>>> " + __name__ + ": gs_set_configuration")
    logger.debug('>>>>> ' + __name__ + ': gs_id = ' + ground_station_id
                 + ', configuration = ' + str(configuration))

    callsign, contact_elevation, latitude, longitude =\
        deserialize_gs_configuration(configuration)
    gs = GroundStationConfiguration.objects.get(identifier=ground_station_id)
    gs.update(callsign=callsign, contact_elevation=contact_elevation,
              latitude=latitude, longitude=longitude)
    return True


@rpcmethod(name='configuration.gs.getChannels',
           signature=['String'], login_required=True)
def gs_get_channels(ground_station_id):
    """
    JRPC method.

    Returns the channels for the given ground station.
    """
    logger.debug(">>>>> " + __name__ + ": gs_get_channels")
    ch_objects = GroundStationConfiguration.objects\
        .get(identifier=ground_station_id)\
        .channels.all()
    return {__GS_CHANNELS: [str(c.identifier) for c in ch_objects]}


@rpcmethod(name='configuration.gs.delete',
           signature=['String'], login_required=True)
def gs_delete(ground_station_id):
    """
    JRPC method.

    Deletes the ground station identified by the given 'ground_station_id'. It
    also deletes all channels associated to this ground station.
    """
    logger.debug(">>>>> " + __name__ + ": gs_delete")
    GroundStationConfiguration.objects\
        .get(identifier=ground_station_id)\
        .delete()
    return True


def serialize_gs_configuration(gs):
    """
    Internal method for serializing the complete configuration of a
    GroundStationConfiguration object.
    :param gs: The object to be serialized.
    :return: The serializable version of the object.
    """
    return {
        __GS_CALLSIGN_K: gs.callsign,
        __GS_ELEVATION_K: str(gs.contact_elevation),
        __GS_LATLON_K: [str(gs.latitude), str(gs.longitude)]
    }


def deserialize_gs_configuration(configuration):
    """
    This method de-serializes the parameters for a Ground Station as provided
    in the input configuration parameter.
    :param configuration: Structure with the configuration parameters for the
                            Ground Station.
    :return: All the parameteres returned as a N-tuple.
    """

    callsign = None
    contact_elevation = None
    latitude = None
    longitude = None

    if __GS_CALLSIGN_K in configuration:
        callsign = configuration[__GS_CALLSIGN_K]
    if __GS_ELEVATION_K in configuration:
        contact_elevation = configuration[__GS_ELEVATION_K]
    if __GS_LATLON_K in configuration:
        latlon = configuration[__GS_LATLON_K]
        latitude = latlon[0]
        longitude = latlon[1]

    return callsign, contact_elevation, latitude, longitude
