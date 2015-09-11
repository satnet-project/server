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
from services.configuration.models import segments as segment_models
from services.simulation.models import passes as pass_models
from services.simulation.jrpc.serializers import passes as pass_serializer
from website import settings as satnet_settings


@rpc4django.rpcmethod(
    name='simulation.sc.passes',
    signature=['String', 'Object'],
    login_required=satnet_settings.JRPC_LOGIN_REQUIRED
)
def get_sc_passes(spacecraft_id, groundstations):
    """JRPC method
    Returns the passes of a given spacecraft over the specified groundstations.
    :param spacecraft_id: Identifier of the spacecraft
    :param groundstations: List of groundstation identifiers
    :return: JSON-like serializable list with the pass slots for ech
    groundstation.
    """
    slots = {}
    spacecraft = segment_models.Spacecraft.objects.get(identifier=spacecraft_id)

    for groundstation_id in groundstations:

        groundstation = segment_models.GroundStation.objects.get(
            identifier=groundstation_id
        )
        gs_slots = pass_models.PassSlots.objects\
            .filter(spacecraft=spacecraft, groundstation=groundstation)
        slots[groundstation_id] = pass_serializer.serialize_pass_slots(gs_slots)

    return slots


@rpc4django.rpcmethod(
    name='simulation.gs.passes',
    signature=['String', 'Object'],
    login_required=satnet_settings.JRPC_LOGIN_REQUIRED
)
def get_gs_passes(groundstation_id, spacecraft):
    """JRPC method
    Returns the passes of the given Spacecraft over this GroundStation.
    :param groundstation_id: Identifier of the groundstation
    :param spacecraft: List of spacecraft identifiers
    :return: JSON-like serializable list with the pass slots for each
    spacecraft.
    """
    slots = {}
    groundstation = segment_models.GroundStation.objects.get(
        identifier=groundstation_id
    )

    for spacecraft_id in spacecraft:

        spacecraft = segment_models.Spacecraft.objects.get(
            identifier=spacecraft_id
        )
        sc_slots = pass_models.PassSlots.objects\
            .filter(spacecraft=spacecraft, groundstation=groundstation)
        slots[spacecraft_id] = pass_serializer.serialize_pass_slots(sc_slots)

    return slots
