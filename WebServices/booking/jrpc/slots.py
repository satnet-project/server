"""
   Copyright 2013, 2014 Ricardo Tubio-Pardavila

   Licensed under the Apache License, Version 2.0 (the "License")
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

from configuration.models.segments import GroundStationConfiguration
from rpc4django import rpcmethod

# ### Keys for the transmission of slots.
SLOT_START_DATETIME = 'slot_start_datetime'
SLOT_ENDING_DATETIME = 'slot_ending_datetime'


@rpcmethod(name='booking.gs.channel.getAvailableSlots',
           signature=['String', 'String'], login_required=True)
def get_availability_slots(ground_station_id, channel_id):
    """
    JRPC method that reteurns the availability for the next 7 days,
    as a result of applying the availability rules already defined.
    :param ground_station_id: The identifier of the ground station.
    :param channel_id: The identifier of the channel within the ground station.
    :return: Array with the availability slots in ISO date format, UTC.
    """
    ch = GroundStationConfiguration.objects.get_channel(ground_station_id,
                                                        channel_id)
    return serialize_slots(ch.get_available_slots())


def serialize_slots(slot_list):
    """
    This method serializes a list of slots.
    :param slot_list: The list to be serialized.
    :return: An array with all the elements individually serialized.
    """
    if slot_list is None:
        return []

    serialized_s = []

    for s in slot_list:
        serialized_s.append({
            SLOT_START_DATETIME: s[0].isoformat(),
            SLOT_ENDING_DATETIME: s[1].isoformat()
        })

    return serialized_s