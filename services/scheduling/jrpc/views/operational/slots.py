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
from website import settings as satnet_settings

from services.scheduling.models import operational as operational_models
from services.scheduling.jrpc.serializers import operational as \
    schedule_serializers


@rpc4django.rpcmethod(
    name='scheduling.getSlot',
    signature=['String'],
    login_required=satnet_settings.JRPC_LOGIN_REQUIRED
)
def get_slot(slot_id):
    """JRPC method: services.scheduling.getSlot
    JRPC method that allows remote users to retrieve the information about a
    given operational slot
    :param slot_id: Identifier of the slot
    :return: JSON-like structure with the information serialized
    """
    return schedule_serializers.serialize_slot_information(
        operational_models.OperationalSlot.objects.get(
            identifier=slot_id
        )
    )
