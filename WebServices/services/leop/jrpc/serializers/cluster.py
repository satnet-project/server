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
JRPC_K_TLE = 'tle'
JRPC_K_TLE_L1 = 'l1'
JRPC_K_TLE_L2 = 'l2'
JRPC_K_CALLSIGN = 'callsign'
JRPC_K_UFOS = 'ufos'
JRPC_K_UFO_ID = 'object_id'
JRPC_K_IDENTIFIED = 'identified'


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


def serialize_leop_cluster(cluster):
    """Serialization method
    Serializes the ufos and identified objects from the given LEOP cluster.
    :param cluster: The LEOP cluster to be serialized
    :return: Tuple with the resulting arrays
    """
    ufos = []
    identified = []

    for ufo in cluster.all():

        if not ufo.is_identified:
            ufos.append({JRPC_K_UFO_ID: str(ufo.identifier)})
        else:
            identified.append({
                JRPC_K_UFO_ID: str(ufo.identifier),
                JRPC_K_CALLSIGN: str(ufo.callsign),
                JRPC_K_TLE: {
                    JRPC_K_TLE_L1: str(ufo.tle.first_line),
                    JRPC_K_TLE_L2: str(ufo.tle.second_line)
                }
            })

    return ufos, identified


def serialize_leop_cfg(leop):
    """Serialization method
    Serializes the current configuration for a given LEOP cluster.
    :param leop: The LEOP cluster
    :return: JSON serialized structure with the configuration
    """
    cluster = serialize_leop_cluster(leop.cluster)
    return {
        JRPC_K_LEOP_ID: str(leop.identifier),
        JRPC_K_TLE: {
            JRPC_K_TLE_L1: str(leop.cluster_tle.first_line),
            JRPC_K_TLE_L2: str(leop.cluster_tle.second_line),
        },
        JRPC_K_UFOS: cluster[0],
        JRPC_K_IDENTIFIED: cluster[1]
    }