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

import logging

from services.common import serialization as common_serializers
from services.configuration.models import segments as segment_models
from services.configuration.models import channels as channel_models
from services.configuration.jrpc.serializers import rules as \
    cfg_serializers
from services.scheduling.models import operational as operational_models

logger = logging.getLogger('scheduling')


SLOTS_K = 'slots'
SLOT_IDENTIFIER_K = 'identifier'
DATE_START_K = 'date_start'
DATE_END_K = 'date_end'
STATE_K = 'state'


def serialize_slot_information(slot):
    """
    Serializes the information about a given operational slot.
    :param slot: Operational slot object
    :return: JSON-like structure with the information of the operational slot
    """
    return {
        'state': slot.state,
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
        SLOT_IDENTIFIER_K: slot.identifier,
        STATE_K: slot.state,
        DATE_START_K: slot.start.isoformat(),
        DATE_END_K: slot.end.isoformat()
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


def serialize_sc_operational_slots(spacecraft_id):
    """
    Serializes all the OperationalSlots for a given spacecraft.
    :param spacecraft_id: The identifier of the Spacecraft.
    :return: The list with all the serialized slots.
    """
    slots = []

    for sc_ch_i in channel_models.SpacecraftChannel.objects.filter(
        enabled=True,
        spacecraft=segment_models.Spacecraft.objects.get(
            identifier=spacecraft_id
        )
    ):

        o_slots_i = operational_models.OperationalSlot.objects.filter(
            spacecraft_channel=sc_ch_i
        )

        for o in operational_models.OperationalSlot.serialize_slots(o_slots_i):
            slots.append(o)

    return slots


def insert_slot(slots, master_ch_id, slave_ch_id, segment_id, slot):
    """
    Inserts the slot into the given slots dictionary, preserving the structure
    regardless of who is the master or the slave (this is, regardless of
    whether the ground station channels are the primary ones or the spacecraft
    channels are the primary). It is, pretty much, a convenience method.

    :param slots: Dictionary with the slots
    :param master_ch_id: Identifier of the primary channel
    :param slave_ch_id: Identifier of the secondary channel
    :param segment_id: Identifier of the segment to which the secondary
    channel belongs to
    :param slot: Slot object form the database
    :return: Dictionary with the new added slot
    """

    sc_ch_o = {
        cfg_serializers.SC_ID_K: segment_id,
        SLOTS_K: []
    }

    if master_ch_id not in slots:

        slots[master_ch_id] = {
            slave_ch_id: sc_ch_o
        }

    elif slave_ch_id not in slots[master_ch_id]:

        slots[master_ch_id][slave_ch_id] = {
            slave_ch_id: sc_ch_o
        }

    slots[master_ch_id][slave_ch_id][SLOTS_K].append(serialize_slot(slot))

    return slots


def serialize_gs_operational_slots(groundstation_id):
    """
    Serializes all the OperationalSlots for a given GroundStation.

    :param groundstation_id: The identifier of the GroundStation
    :return: The list with all the serialized slots
    """

    slots = {}

    gs_channels = channel_models.GroundStationChannel.objects.filter(
        enabled=True,
        groundstation=segment_models.GroundStation.objects.get(
            identifier=groundstation_id
        )
    )

    for slot in operational_models.OperationalSlot.objects.filter(
        compatible_channels__groundstation_channel__in=gs_channels
    ):

        insert_slot(
            slots,
            slot.groundstation_channel.identifier,
            slot.spacecraft_channel.identifier,
            slot.spacecraft_channel.spacecraft_set.all()[0].identifier,
            slot
        )

    return slots
