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
from services.scheduling.jrpc.serializers import serialization

@rpc4django.rpcmethod(
    name='scheduling.sc.getOperationalSlots',
    signature=['String'],
    login_required=True
)
def get_operational_slots(spacecraft_id):
    """
    JRPC method that permits obtaining all the OperationalSlots for all the
    channels that belong to the Spacecraft with the given identifier.
    :param spacecraft_id: Identifier of the spacecraft.
    :return: JSON-like structure with the data serialized.
    """
    return sorted(
        serialization.serialize_sc_operational_slots(spacecraft_id),
        key=lambda s: s[operational.SLOT_IDENTIFIER]
    )


@rpc4django.rpcmethod(
    name='scheduling.sc.getSlotChanges',
    signature=['String'],
    login_required=True
)
def get_changes(spacecraft_id):
    """
    JRPC method that returns the OperationalSlots that have suffered changes
    for the given Spacecraft.
    :param spacecraft_id: The identifier of the Spacecraft.
    :return: JSON-like structure with the data serialized.
    """
    sc = segments.Spacecraft.objects.get(identifier=spacecraft_id)
    changed_slots = operational.OperationalSlot.objects\
        .get_spacecraft_changes(sc)

    return sorted(
        operational.OperationalSlot.serialize_slots(changed_slots),
        key=lambda s: s[operational.SLOT_IDENTIFIER]
    )


@rpc4django.rpcmethod(
    name='scheduling.sc.selectSlots',
    signature=['String', 'Object'],
    login_required=True
)
def select_slots(spacecraft_id, slot_identifiers):
    """
    JRPC method that changes the state of the OperationalSlots provided to
    'SELECTED', requesting the selection for remote operation of that given
    GroundStation. GroundStation operators have still to confirm the remote
    operation requested, which will change the state of the OperationalSlot
    from 'SELECTED' to 'RESERVED'.
    :param spacecraft_id: The identifier of the Spacecraft making the request.
    :param slot_identifiers: The identifiers for all the requested
    OperationalSlots.
    :return: List with the final state of the OperationalSlots selected. If
    some of the slots could not be selected (because their state was not either
    'FREE' or 'SELECTED' at the time the request was made), they will be
    returned with their actual state.
    """
    if slot_identifiers is None or len(slot_identifiers) == 0:
        raise Exception('No <slot_identifiers> provided.')

    slots = operational.OperationalSlot.objects.filter(
        identifier__in=slot_identifiers
    )
    if slots is None or len(slots) == 0:
        raise Exception('No valid <slot_identifiers> provided.')

    changed_slots = operational.OperationalSlot.objects.update_state(
        state=operational.STATE_SELECTED, slots=slots,
        notify_sc=False, notify_gs=True
    )
    return sorted(
        operational.OperationalSlot.serialize_slots(changed_slots),
        key=lambda s: s[operational.SLOT_IDENTIFIER]
    )


@rpc4django.rpcmethod(
    name='scheduling.sc.cancelSelections',
    signature=['String', 'Object'],
    login_required=True
)
def cancel_selections(spacecraft_id, slot_identifiers):
    """
    JRPC method that changes the state of the OperationalSlots provided to
    'FREE', notifying the postposal of the requested operation over the
    already selected slots.
    :param spacecraft_id: The identifier of the Spacecraft making the request.
    :param slot_identifiers: The identifiers for all the requested
    OperationalSlots.
    :return: List with the final state of the OperationalSlots selected. If
    some of the slots could not be selected (because their state was not
    'SELECTED' at the time the request was made), they will be returned with
    their actual state.
    """
    if slot_identifiers is None or len(slot_identifiers) == 0:
        raise Exception('No <slot_identifiers> provided.')

    slots = operational.OperationalSlot.objects\
        .filter(identifier__in=slot_identifiers)
    if slots is None or len(slots) == 0:
        raise Exception('No valid <slot_identifiers> provided.')

    changed_slots = operational.OperationalSlot.objects.update_state(
        state=operational.STATE_FREE, slots=slots,
        notify_sc=False, notify_gs=True
    )
    return sorted(
        operational.OperationalSlot.serialize_slots(changed_slots),
        key=lambda s: s[operational.SLOT_IDENTIFIER]
    )


@rpc4django.rpcmethod(
    name='scheduling.sc.cancelReservations',
    signature=['String', 'Object'],
    login_required=True
)
def cancel_reservations(spacecraft_id, slot_identifiers):
    """
    JRPC method that changes the state of the OperationalSlots provided to
    'FREE', notifying the postposal of the requested operation over the
    already selected slots.
    :param spacecraft_id: The identifier of the Spacecraft making the request.
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
        state=operational.STATE_FREE, slots=slots,
        notify_sc=False, notify_gs=True
    )
    return sorted(
        operational.OperationalSlot.serialize_slots(changed_slots),
        key=lambda s: s[operational.SLOT_IDENTIFIER]
    )