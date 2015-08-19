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
from services.configuration.models import segments, channels, compatibility \
    as compatiblity_models
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
            STATE_K: s.state,
            DATE_START_K: s.start.isoformat(),
            DATE_END_K: s.end.isoformat()
        })

    return s_slots


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

    gs_channels = channels.SpacecraftChannel.objects.filter(
        enabled=True,
        groundstation=segments.GroundStation.objects.get(
            identifier=groundstation_id
        )
    )

    for pair in compatiblity_models.ChannelCompatibility.objects.filter(
        grounstation_channels__in=gs_channels
    ):

        o_slots_i = operational_models.OperationalSlot.objects.filter(
            groundstation_channel=pair.
        )

        for o in serialize_slots(o_slots_i):
            slots.append(o)

    return slots
