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


@rpc4django.rpcmethod(
    name='simulation.spacecraft.getPasses',
    signature=['String'],
    login_required=True
)
def get_sc_passes(spacecraft_id):
    """JRPC method
    Returns the passes of a given spacecraft over all the registered
    GroundStations.
    :param spacecraft_id: Identifier of the spacecraft
    :return: JSON-like serializable list with the pass slots
    """
    spacecraft = segment_models.Spacecraft.objects.get(identifier=spacecraft_id)
    pass_slots = pass_models.PassSlots.objects.filter(spacecraft=spacecraft)
    return pass_serializer.serialize_pass_slots(pass_slots)


@rpc4django.rpcmethod(
    name='simulation.groundstation.getPasses',
    signature=['String'],
    login_required=True
)
def get_gs_passes(groundstation_id):
    """JRPC method
    Returns the passes of all the registered Spacecraft over this
    GroundStation.
    :param groundstation_id: Identifier of the groundstation
    :return: JSON-like serializable list with the pass slots
    """
    groundstation = segment_models.GroundStation.objects.get(
        identifier=groundstation_id
    )
    pass_slots = pass_models.PassSlots.objects.filter(
        groundstation=groundstation
    )
    return pass_serializer.serialize_pass_slots(pass_slots)