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

import rpc4django

from services.configuration.models import segments
from services.scheduling.models import operational
from services.scheduling.jrpc import serialization


@rpc4django.rpcmethod(
    name='scheduling.gs.getOperationalSlots',
    signature=['String'],
    login_required=True
)
def get_operational_slots(groundstation_id):
    """
    JRPC method that permits obtaining all the OperationalSlots for all the
    channels that belong to the GroundStation with the given identifier.
    :param groundstation_id: Identifier of the spacecraft.
    :return: JSON-like structure with the data serialized.
    """
    return serialization.serialize_gs_operational_slots(groundstation_id)


@rpc4django.rpcmethod(
    name='scheduling.gs.getSlotChanges',
    signature=['String'],
    login_required=True
)
def get_changes(groundstation_id):
    """
    JRPC method that returns the OperationalSlots that have suffered changes
    for the given GroundStation.
    :param groundstation_id: The identifier of the GroundStation.
    :return: JSON-like structure with the data serialized.
    """
    gs = segments.GroundStation.objects.get(identifier=groundstation_id)
    changed_slots = operational.OperationalSlot.objects\
        .get_groundstation_changes(gs)
    return operational.OperationalSlot.serialize_slots(changed_slots)


@rpc4django.rpcmethod(
    name='scheduling.gs.confirmSelections',
    signature=['String', 'Object'],
    login_required=True
)
def confirm_selections(groundstation_id, slot_identifiers):
    """
    JRPC method that changes the state of the OperationalSlots provided to
    'RESERVED', notifying the postposal of the requested operation over the
    already selected slots.
    :param groundstation_id: The identifier of the GroundStation making the
    request.
    :param slot_identifiers: The identifiers for all the requested
    OperationalSlots.
    :return: List with the final state of the OperationalSlots selected. If
    some of the slots could not be selected (because their state was not
    'SELECTED' at the time the request was made), they will be returned with
    their actual state.
    """
    if slot_identifiers is None or len(slot_identifiers) == 0:
        raise Exception('No <slot_identifiers> provided.')

    slots = operational.OperationalSlot.objects.filter(
        identifier__in=slot_identifiers
    )
    if slots is None or len(slots) == 0:
        raise Exception('No valid <slot_identifiers> provided.')

    changed_slots = operational.OperationalSlot.objects.update_state(
        state=operational.STATE_RESERVED, slots=slots,
        notify_sc=True, notify_gs=False
    )
    return operational.OperationalSlot.serialize_slots(changed_slots)


@rpc4django.rpcmethod(
    name='scheduling.gs.denySelections',
    signature=['String', 'Object'],
    login_required=True
)
def deny_selections(groundstation_id, slot_identifiers):
    """
    JRPC method that changes the state of the OperationalSlots provided to
    'DENIED', notifying the postposal of the requested operation over the
    already selected slots.
    :param groundstation_id: The identifier of the GroundStation making the
    request.
    :param slot_identifiers: The identifiers for all the requested
    OperationalSlots.
    :return: List with the final state of the OperationalSlots selected. If
    some of the slots could not be selected (because their state was not
    'SELECTED' at the time the request was made), they will be returned with
    their actual state.
    """
    if slot_identifiers is None or len(slot_identifiers) == 0:
        raise Exception('No <slot_identifiers> provided.')

    slots = operational.OperationalSlot.objects.filter(
        identifier__in=slot_identifiers
    )
    if slots is None or len(slots) == 0:
        raise Exception('No valid <slot_identifiers> provided.')

    changed_slots = operational.OperationalSlot.objects.update_state(
        state=operational.STATE_DENIED, slots=slots,
        notify_sc=True, notify_gs=False
    )
    return operational.OperationalSlot.serialize_slots(changed_slots)


@rpc4django.rpcmethod(
    name='scheduling.gs.cancelReservations',
    signature=['String', 'Object'],
    login_required=True
)
def cancel_reservations(groundstation_id, slot_identifiers):

    """
    JRPC method that changes the state of the OperationalSlots provided to
    'CANCELED', notifying the postposal of the requested operation over the
    already selected slots.
    :param groundstation_id: The identifier of the GroundStation making the
    request.
    :param slot_identifiers: The identifiers for all the requested
    OperationalSlots.
    :return: List with the final state of the OperationalSlots selected. If
    some of the slots could not be selected (because their state was not
    'RESERVED' at the time the request was made), they will be returned with
    their actual state.
    """
    if slot_identifiers is None or len(slot_identifiers) == 0:
        raise Exception('No <slot_identifiers> provided.')

    slots = operational.OperationalSlot.objects.filter(
        identifier__in=slot_identifiers
    )
    if slots is None or len(slots) == 0:
        raise Exception('No valid <slot_identifiers> provided.')

    changed_slots = operational.OperationalSlot.objects.update_state(
        state=operational.STATE_CANCELED, slots=slots,
        notify_sc=True, notify_gs=False
    )
    return operational.OperationalSlot.serialize_slots(changed_slots)