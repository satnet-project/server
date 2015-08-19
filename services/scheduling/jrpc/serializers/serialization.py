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
from services.configuration.jrpc.serializers import serialization as \
    cfg_serialization
from services.configuration.models import segments, channels
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


def serialize_operational_slot(slot):
    """
    Serializes a single OperationalSlot into a JSON-RPC data structure.
    :return: JSON-like structure with the data serialized.
    """
    return {
        SLOT_IDENTIFIER_K: slot.identifier,
        STATE_K: slot.state,
        cfg_serialization.CH_ID_K: slot.spacecraft_channel.identifier,
        DATE_START_K: slot.start.isoformat(),
        DATE_END_K: slot.end.isoformat()
    }


def serialize_sc_operational_slots(spacecraft_id):
    """
    Serializes all the OperationalSlots for a given spacecraft.
    :param spacecraft_id: The identifier of the Spacecraft.
    :return: The list with all the serialized slots.
    """
    slots = []

    for sc_ch_i in channels.SpacecraftChannel.objects.filter(
            enabled=True,
            spacecraft=segments.Spacecraft.objects.get(identifier=spacecraft_id)
    ):

        o_slots_i = operational_models.OperationalSlot.objects.filter(
            spacecraft_channel=sc_ch_i
        )

        for o in operational_models.OperationalSlot.serialize_slots(o_slots_i):
            slots.append(o)

    return slots


def serialize_gs_operational_slots(groundstation_id):
    """
    Serializes all the OperationalSlots for a given GroundStation.
    :param groundstation_id: The identifier of the GroundStation.
    :return: The list with all the serialized slots.
    """
    slots = []

    for gs_ch_i in channels.GroundStationChannel.objects.filter(
        enabled=True,
        groundstation=segments.GroundStation.objects.get(
            identifier=groundstation_id
        )
    ):

        for slot in operational_models.OperationalSlot.objects.filter(
            groundstation_channel=gs_ch_i
        ):
            o_slots_i = serialize_operational_slot(slot)

        slots.append({
            cfg_serialization.CH_ID_K: gs_ch_i, {
                cfg_serialization
            }
        })

    return slots
