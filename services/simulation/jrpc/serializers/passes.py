"""
   Copyright 2015 Ricardo Tubio-Pardavila

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

from services.configuration.jrpc.serializers import segments as segment_serial

SLOT_START_K = 'slot_start'
SLOT_END_K = 'slot_end'


# noinspection PyUnusedLocal
def serialize_pass_slots(pass_slots, by_gs=True):
    """
    Serializes a list of pass slots into an array of JSON-like serializable
    slot objects.

    :param pass_slots: Original array with the database slot models
    :param by_gs: Indicates whether the serialization should be by GS
    :return: Serializable list
    """
    serial_array = []

    for s in pass_slots:

        serial_array.append({
            segment_serial.SC_ID_K: s.spacecraft.identifier,
            segment_serial.GS_ID_K: s.groundstation.identifier,
            SLOT_START_K: s.start.isoformat(),
            SLOT_END_K: s.end.isoformat()
        })

    return serial_array
