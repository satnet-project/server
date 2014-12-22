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

JRPC_K_LEOP_ID = 'leop_id'
JRPC_K_AVAILABLE_GS = 'leop_gs_available'
JRPC_K_IN_USE_GS = 'leop_gs_inuse'


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
        JRPC_K_AVAILABLE_GS: [ str(g.identifier) for g in available_gs ],
        JRPC_K_IN_USE_GS: [ str(g.identifier) for g in in_use_gs ]
    }