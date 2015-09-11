"""
   Copyright 2015 Ricardo Tubio-Pardavila

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
from services.configuration.models import segments as segment_models
from services.scheduling.models import availability as availability_models
from services.scheduling.jrpc.serializers import \
    operational as operational_serial
from website import settings as satnet_settings


@rpcmethod(
    name="scheduling.gs.availability",
    signature=['String'],
    login_required=satnet_settings.JRPC_LOGIN_REQUIRED
)
def sc_channel_get_compatible(groundstation_id):
    """JRPC method: scheduling.gs.availability
    JRPC method that returns the availability slots for a given ground station.
    :param groundstation_id: String with the groundstation identifier
    :return: JSON-like object with the availability slots
    """
    return operational_serial.serialize_slots(
        availability_models.AvailabilitySlot.objects.filter(
            groundstation=segment_models.GroundStation.objects.get(
                identifier=groundstation_id
            )
        )
    )
