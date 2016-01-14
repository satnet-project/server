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

USER_K = 'username'

# ### JSON keys for encoding/decoding information related to any segment
SEGMENT_ID_K = 'segment_id'

# ### JSON keys for enconding/decoding GroundStation dictionaries
GS_ID_K = 'groundstation_id'
GS_LATLON_K = 'groundstation_latlon'
GS_ALTITUDE_K = 'groundstation_altitude'
GS_CALLSIGN_K = 'groundstation_callsign'
GS_ELEVATION_K = 'groundstation_elevation'

# ### JSON keys for encoding/decoding Spacecraft dictionaries
SC_ID_K = 'spacecraft_id'
SC_CALLSIGN_K = 'spacecraft_callsign'
SC_TLE_ID_K = 'spacecraft_tle_id'


def serialize_sc_configuration(sc):
    """
    Internal method for serializing the complete configuration of a
    SpacecraftConfiguration object.
    :param sc: The object to be serialized.
    :return: The serializable version of the object.
    """
    return {
        SC_ID_K: sc.identifier,
        SC_CALLSIGN_K: sc.callsign,
        SC_TLE_ID_K: sc.tle.identifier,
        USER_K: sc.user.username
    }


def deserialize_sc_configuration(configuration):
    """
    This method de-serializes the parameters for a Ground Station as provided
    in the input configuration parameter.
    :param configuration: Structure with the configuration parameters for the
                            Ground Station.
    :return: All the parameteres returned as a N-tuple (callsign, tle_id)
    """

    callsign = None
    tle_id = None

    if SC_CALLSIGN_K in configuration:
        callsign = configuration[SC_CALLSIGN_K]
    if SC_TLE_ID_K in configuration:
        tle_id = configuration[SC_TLE_ID_K]

    return callsign, tle_id


def serialize_gs_configuration(gs):
    """
    Internal method for serializing the complete configuration of a
    GroundStationConfiguration object.
    :param gs: The object to be serialized.
    :return: The serializable version of the object.
    """
    return {
        GS_ID_K: gs.identifier,
        GS_CALLSIGN_K: gs.callsign,
        GS_ELEVATION_K: gs.contact_elevation,
        GS_LATLON_K: [gs.latitude, gs.longitude],
        GS_ALTITUDE_K: gs.altitude,
        USER_K: gs.user.username
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

    if GS_CALLSIGN_K in configuration:
        callsign = configuration[GS_CALLSIGN_K]
    if GS_ELEVATION_K in configuration:
        contact_elevation = configuration[GS_ELEVATION_K]
    if GS_LATLON_K in configuration:
        latlon = configuration[GS_LATLON_K]
        latitude = latlon[0]
        longitude = latlon[1]

    return callsign, contact_elevation, latitude, longitude
