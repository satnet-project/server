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

JRPC_K_LEOP_ID = 'identifier'
JRPC_K_AVAILABLE_GS = 'leop_gs_available'
JRPC_K_IN_USE_GS = 'leop_gs_inuse'
JRPC_K_DATE = 'date'
JRPC_K_TLE = 'tle'
JRPC_K_TLE_L1 = 'tle_l1'
JRPC_K_TLE_L2 = 'tle_l2'
JRPC_K_CALLSIGN = 'callsign'
JRPC_K_UNKNOWN_OBJECTS = 'ufos'
JRPC_K_OBJECT_ID = 'object_id'
JRPC_K_IDENTIFIED_OBJECTS = 'identified'


def serialize_leop_id(leop_id):
    """JRPC serializer.
    Serializes the identifier of a given LEOP cluster.
    :param leop_id: The identifier to be serialized.
    :return: JSON-RPC object with the identifier.
    """
    return {
        JRPC_K_LEOP_ID: leop_id
    }


def serialize_gs_lists(available_gs, in_use_gs):
    """JRPC serializer.
    Method that serializes into a JRPC-like structure the lists of available
    and in-use ground stations for a given LEOP cluster.
    :param available_gs: The Ground Stations that have not been included in the
                            LEOP cluster yet.
    :param in_use_gs: The Ground Stations that have already been included in the
                        LEOP cluster.
    :return: JSON-RPC object with both lists.
    """
    return {
        JRPC_K_AVAILABLE_GS: [str(g.identifier) for g in available_gs],
        JRPC_K_IN_USE_GS: [str(g.identifier) for g in in_use_gs]
    }


def serialize_launch_unknown(unknown):
    """Serialization method
    Serializes the unknown objects list
    :param unknown: The list to be serialized
    :return: Resulting object
    """
    result = []

    if not unknown:
        return result

    for u in unknown:
        result.append({JRPC_K_OBJECT_ID: str(u.identifier)})

    return result


def serialize_launch_identified(identified):
    """Serialization method
    Serializes the identified spacecraft objects for a given launch.
    :param identified: List with the spacecraft objects
    :return: JSON-RPC serializable object
    """
    result = []

    if len(identified) < 1:
        return result

    for i in identified:

        result.append({
            JRPC_K_OBJECT_ID: str(i.identifier),
            JRPC_K_CALLSIGN: str(i.spacecraft.callsign),
            JRPC_K_TLE_L1: str(i.spacecraft.tle.first_line),
            JRPC_K_TLE_L2: str(i.spacecraft.tle.second_line)
        })

    return result


def serialize_launch(launch):
    """Serialization method
    Serializes the current configuration for a given LEOP cluster.
    :param launch: The LEOP cluster
    :return: JSON serialized structure with the configuration
    """
    unknown = serialize_launch_unknown(launch.unknown_objects.all())
    identified_objects = launch.identified_objects.all()
    identified = serialize_launch_identified(identified_objects)

    return {
        JRPC_K_LEOP_ID: str(launch.identifier),
        JRPC_K_TLE_L1: str(launch.tle.first_line),
        JRPC_K_TLE_L2: str(launch.tle.second_line),
        JRPC_K_DATE: str(launch.date.isoformat()),
        JRPC_K_UNKNOWN_OBJECTS: unknown,
        JRPC_K_IDENTIFIED_OBJECTS: identified
    }


def deserialize_launch(launch):
    # ### TODO Full configuration including UFO and IDENTIFIED arrays.
    """Deserialization method
    Deserializes the configuration for a given LAUNCH cluster, without getting
    into the "ufo" or "identified" arrays (should be set separately).
    :param launch: JSON-like object with the configuration of the launch
    :return: (date, tle_l1, tle_l2) as a tuple
    """
    if not launch:
        return None, None, None

    date = None
    tle_l1 = None
    tle_l2 = None

    if JRPC_K_DATE in launch:
        date = launch[JRPC_K_DATE]
    if JRPC_K_TLE_L1 in launch:
        tle_l1 = launch[JRPC_K_TLE_L1]
    if JRPC_K_TLE_L2 in launch:
        tle_l2 = launch[JRPC_K_TLE_L2]

    return date, tle_l1, tle_l2