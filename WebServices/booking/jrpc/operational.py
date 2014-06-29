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

from rpc4django import rpcmethod

from booking.models import operational
from configuration.models import channels, segments


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

        s_slots.append(operational.OperationalSlot.serialize_slots(o_slots_i))

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

        s_slots.append(operational.OperationalSlot.serialize_slots(o_slots_i))

    if len(s_slots) == 0:
        raise Exception(
            'No OperationalSlots available for GroundStation <'
            + str(groundstation_id) + '>'
        )

    return s_slots


@rpcmethod(
    name='booking.sc.getOperationalSlots',
    signature=['String'],
    login_required=True
)
def sc_get_operational_slots(spacecraft_id):
    """
    JRPC method that permits obtaining all the OperationalSlots for all the
    channels that belong to the Spacecraft with the given identifier.
    :param spacecraft_id: Identifier of the spacecraft.
    :return: JSON-like structure with the data serialized.
    """
    return serialize_sc_operational_slots(spacecraft_id)


@rpcmethod(
    name='booking.gs.getOperationalSlots',
    signature=['String'],
    login_required=True
)
def gs_get_operational_slots(groundstation_id):
    """
    JRPC method that permits obtaining all the OperationalSlots for all the
    channels that belong to the GroundStation with the given identifier.
    :param groundstation_id: Identifier of the spacecraft.
    :return: JSON-like structure with the data serialized.
    """
    return serialize_sc_operational_slots(groundstation_id)


@rpcmethod(
    name='booking.sc.getSlotChanges',
    signature=['String', 'Object'],
    login_required=True
)
def sc_get_changes(spacecraft_id):
    """
    JRPC method that returns the OperationalSlots that have suffered changes
    for the given Spacecraft.
    :param spacecraft_id: The identifier of the Spacecraft.
    :return: JSON-like structure with the data serialized.
    """
    return operational.OperationalSlot.serialize_slots(
        operational.OperationalSlot.objects.get_spacecraft_changes(
            segments.Spacecraft.objects.get(identifier=spacecraft_id)
        )
    )


@rpcmethod(
    name='booking.sc.selectSlots',
    signature=['String', 'Object'],
    login_required=True
)
def sc_select_slots(spacecraft_id, slot_identifiers):

    return []


@rpcmethod(
    name='booking.sc.cancelSelections',
    signature=['String', 'Object'],
    login_required=True
)
def sc_cancel_selections(spacecraft_id, slot_identifiers):

    return True

@rpcmethod(
    name='booking.sc.cancelReservations',
    signature=['String', 'Object'],
    login_required=True
)
def sc_cancel_reservations(spacecraft_id, slot_identifiers):

    return True

@rpcmethod(
    name='booking.gs.getReservations',
    signature=['String'],
    login_required=True
)
def gs_get_reservations(groundstation_id, slot_identifiers):

    return True


@rpcmethod(
    name='booking.gs.confirmReservation',
    signature=['String', 'Object'],
    login_required=True
)
def gs_confirm_reservations(groundstation_id, slot_identifiers):

    return True


@rpcmethod(
    name='booking.gs.cancelReservation',
    signature=['String', 'Object'],
    login_required=True
)
def gs_cancel_reservations(groundstation_id, slot_identifiers):

    return True


@rpcmethod(
    name='booking.gs.denyReservation',
    signature=['String', 'Object'],
    login_required=True
)
def gs_deny_reservations(groundstation_id, slot_identifiers):

    return True