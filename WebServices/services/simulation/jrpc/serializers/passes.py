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

from services.leop.jrpc.serializers import launch as launch_serializers


def serialize_pass_slots(pass_slots):
    """
    Serializes a list of pass slots into an array of JSON-like serializable
    slot objects.
    :param pass_slots: Original array with the database slot models
    :return: Serializable list
    """
    serial_array = []

    for s in pass_slots:

        serial_array.append({
            launch_serializers.JRPC_K_SC_ID: s.spacecraft.identifier,
            launch_serializers.JRPC_K_GS_ID: s.groundstation.identifier,
            launch_serializers.JRPC_K_SLOT_START: s.start.isoformat(),
            launch_serializers.JRPC_K_SLOT_END: s.end.isoformat()
        })

    return serial_array