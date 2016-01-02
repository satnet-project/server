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

import datetime
import logging

from services.common import misc as common_misc
from services.common import serialization as common_serializers
from services.configuration.models import segments as segment_models
from services.configuration.jrpc.serializers import \
    segments as segment_serializers
from services.scheduling.jrpc.serializers import availability as \
    availability_serializers
from services.scheduling.models import operational as operational_models

logger = logging.getLogger('scheduling')


SLOTS_K = 'slots'
STATE_K = 'state'


def serialize_test_slot_information():
    """
    Serializes the information about a TESTING slot, that is intended to be
    used only for TESTING PURPOSES.
    :return: JSON-like structure with the information of the operational slot
    """
    s_time = common_misc.get_now_utc(no_microseconds=True)
    e_time = s_time + datetime.timedelta(hours=2)

    return {
        STATE_K: 'TEST',
        'gs_username': 'test-gs-user',
        'sc_username': 'test-sc-user',
        'starting_time': common_serializers.serialize_iso8601_date(s_time),
        'ending_time': common_serializers.serialize_iso8601_date(e_time),
    }


def serialize_slot_information(slot):
    """
    Serializes the information about a given operational slot.
    :param slot: Operational slot object
    :return: JSON-like structure with the information of the operational slot
    """
    return {
        STATE_K: slot.state,
        'gs_username':
            slot.groundstation_channel.groundstation_set.all()[0].user
            .username,
        'sc_username':
            slot.spacecraft_channel.spacecraft_set.all()[0].user.username,
        'starting_time':
            common_serializers.serialize_iso8601_date(
                slot.availability_slot.start
            ),
        'ending_time':
            common_serializers.serialize_iso8601_date(
                slot.availability_slot.end
            ),
    }


def serialize_slot(slot):
    """
    Serializes an OperationalSlot object into a JSON-RPC data structure.
    :param slot: Slot to be serialized
    :return: JSON-like structure with the data serialized
    """
    return {
        availability_serializers.SLOT_IDENTIFIER_K: slot.identifier,
        STATE_K: slot.state,
        availability_serializers.DATE_START_K: slot.start.isoformat(),
        availability_serializers.DATE_END_K: slot.end.isoformat()
    }


def serialize_slots(slots):
    """
    Serializes a list of OperationalSlot objects into a JSON-RPC data structure.
    :param slots: List with the slots to be serialized
    :return: JSON-like structure with the data serialized
    """
    s_slots = []

    for s in slots:

        s_slots.append(serialize_slot(s))

    return s_slots


def insert_slot(slots, master_segment_id, slave_segment_id, slot):
    """
    Inserts the slot into the given slots dictionary, preserving the structure
    regardless of who is the master or the slave (this is, regardless of
    whether the ground station channels are the primary ones or the spacecraft
    channels are the primary). It is, pretty much, a convenience method.

    :param slots: Dictionary with the slots
    :param master_segment_id: Identifier of the primary segment
    :param slave_segment_id: Identifier of the slave segment
    :param slot: Slot object form the database
    :return: Dictionary with the new added slot
    """
    sc_ch_o = {
        segment_serializers.SEGMENT_ID_K: slave_segment_id,
        SLOTS_K: []
    }

    if master_segment_id not in slots:

        slots[master_segment_id] = {
            slave_segment_id: sc_ch_o
        }

    elif slave_segment_id not in slots[master_segment_id]:

        slots[master_segment_id][slave_segment_id] = {
            slave_segment_id: sc_ch_o
        }

    slots[master_segment_id][slave_segment_id][SLOTS_K].append(
        serialize_slot(slot)
    )


def serialize_sc_operational_slots(spacecraft_id):
    """
    Serializes all the OperationalSlots for a given spacecraft.

    :param spacecraft_id: The identifier of the Spacecraft
    :return: The list with all the serialized slots
    """
    slots = {}

    for slot in operational_models.OperationalSlot.objects.filter(
        pass_slot__spacecraft__identifier=spacecraft_id
    ):

        insert_slot(
            slots,
            slot.pass_slot.spacecraft.identifier,
            slot.pass_slot.groundstation.identifier,
            slot
        )

    return slots


def serialize_gs_operational_slots(groundstation_id):
    """
    Serializes all the OperationalSlots for a given GroundStation.

    :param groundstation_id: The identifier of the GroundStation
    :return: The list with all the serialized slots
    """

    slots = {}

    for slot in operational_models.OperationalSlot.objects.filter(
        pass_slot__groundstation=segment_models.GroundStation
            .objects.get(identifier=groundstation_id)
    ):

        if slot.pass_slot.spacecraft.identifier not in slots:
            slots[slot.pass_slot.spacecraft.identifier] = []

        slots[slot.pass_slot.spacecraft.identifier].append(
            serialize_slot(slot)
        )

    return slots
