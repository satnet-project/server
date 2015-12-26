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

SLOT_IDENTIFIER_K = 'identifier'
DATE_START_K = 'date_start'
DATE_END_K = 'date_end'


def serialize_slots(slots):
    """
    Serializes a list of OperationalSlot objects into a JSON-RPC data structure.
    :param slots: List with the slots to be serialized
    :return: JSON-like structure with the data serialized
    """
    s_slots = []

    for s in slots:

        s_slots.append({
            SLOT_IDENTIFIER_K: s.identifier,
            DATE_START_K: s.start.isoformat(),
            DATE_END_K: s.end.isoformat()
        })

    return s_slots
