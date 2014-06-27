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


@rpcmethod(
    name='booking.sc.getOperationalSlots',
    signature=['String'],
    login_required=True
)
def sc_get_operational_slots(spacecraft_id):

    return []


@rpcmethod(
    name='booking.gs.getOperationalSlots',
    signature=['String'],
    login_required=True
)
def gs_get_operational_slots(groundstation_id):

    return []


@rpcmethod(
    name='booking.sc.makeReservations',
    signature=['String', 'Object'],
    login_required=True
)
def sc_make_reservations(spacecraft_id, operational_slots):

    return 0


@rpcmethod(
    name='booking.sc.cancelReservations',
    signature=['String', 'Object'],
    login_required=True
)
def sc_cancel_reservation(spacecraft_id, reservation_identifiers):

    return True


@rpcmethod(
    name='booking.gs.getReservations',
    signature=['String'],
    login_required=True
)
def gs_get_reservations(groundstation_id, reservation_identifiers):

    return True


@rpcmethod(
    name='booking.gs.confirmReservation',
    signature=['String', 'Object'],
    login_required=True
)
def gs_confirm_reservations(groundstation_id, reservation_identifiers):

    return True


@rpcmethod(
    name='booking.gs.denyReservation',
    signature=['String', 'Object'],
    login_required=True
)
def gs_deny_reservations(groundstation_id, reservation_identifiers):

    return True