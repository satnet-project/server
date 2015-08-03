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

from services.common import serialization as common_serializers
from services.configuration.models import segments, channels
from services.scheduling.models import operational


def serialize_slot_information(slot):
    """
    Serializes the information about a given operational slot.
    :param slot: Operational slot object
    :return: JSON-like structure with the information of the operational slot
    """
    return {
        'state': slot.state,
        'gs_username':
            slot[0].groundstation_channel.groundstation_set.all()[0].user.username,
        'sc_username':
            slot[0].spacecraft_channel.spacecraft_set.all()[0].user.username,
        'starting_time': common_serializers.serialize_iso8601_date(
            slot.availability_slot.start
        ),
        'ending_time': common_serializers.serialize_iso8601_date(
            slot.availability_slot.end
        ),
    }


def serialize_sc_operational_slots(spacecraft_id):
    """
    Serializes all the OperationalSlots for a given spacecraft.
    :param spacecraft_id: The identifier of the Spacecraft.
    :return: The list with all the serialized slots.
    """
    s_slots = []

    for sc_ch_i in channels.SpacecraftChannel.objects.filter(
            enabled=True,
            spacecraft=segments.Spacecraft.objects.get(identifier=spacecraft_id)
    ):

        o_slots_i = operational.OperationalSlot.objects.filter(
            spacecraft_channel=sc_ch_i
        )

        for o in operational.OperationalSlot.serialize_slots(o_slots_i):
            s_slots.append(o)

    if len(s_slots) == 0:
        raise Exception(
            'No OperationalSlots available for Spacecraft <'
            + str(spacecraft_id) + '>'
        )

    return s_slots


def serialize_gs_operational_slots(groundstation_id):
    """
    Serializes all the OperationalSlots for a given GroundStation.
    :param groundstation_id: The identifier of the GroundStation.
    :return: The list with all the serialized slots.
    """
    s_slots = []

    for gs_ch_i in channels.GroundStationChannel.objects.filter(
            enabled=True,
            groundstation=segments.GroundStation.objects.get(
                identifier=groundstation_id
            )
    ):

        o_slots_i = operational.OperationalSlot.objects.filter(
            groundstation_channel=gs_ch_i
        )

        for o in operational.OperationalSlot.serialize_slots(o_slots_i):
            s_slots.append(o)

    if len(s_slots) == 0:
        raise Exception(
            'No OperationalSlots available for GroundStation <'
            + str(groundstation_id) + '>'
        )

    return s_slots
