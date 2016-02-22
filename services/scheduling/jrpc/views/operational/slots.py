
from django.db.models import Q
import rpc4django
from website import settings as satnet_settings

from services.common import misc as sn_misc
from services.scheduling.models import operational as operational_models
from services.scheduling.jrpc.serializers import operational as \
    schedule_serializers

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


@rpc4django.rpcmethod(
    name='scheduling.slot.get',
    signature=['String'],
    login_required=satnet_settings.JRPC_LOGIN_REQUIRED
)
def get_slot(slot_id):
    """JRPC: services.scheduling.getSlot
    JRPC method that allows remote users to retrieve the information about a
    given operational slot
    :param slot_id: Identifier of the slot
    :return: JSON-like structure with the information serialized
    """
    if slot_id < 0:
        return schedule_serializers.serialize_test_slot_information()

    return schedule_serializers.serialize_slot(
        operational_models.OperationalSlot.objects.get(
            identifier=slot_id
        )
    )


@rpc4django.rpcmethod(
    name='scheduling.slot.next',
    signature=['String'],
    login_required=satnet_settings.JRPC_LOGIN_REQUIRED
)
def get_next_slot(user_email):
    """JRPC: services.scheduling.slots.next
    Returns the next slot that is going to be available for the given user.

    Args:
        user_email: String with the email of the user
    Returns:
        Slot object with the following operational slot (null if no available)
    """
    return schedule_serializers.serialize_slot(
        operational_models.OperationalSlot.objects.filter(
            Q(pass_slot__spacecraft__user__email=user_email) |
            Q(pass_slot__groundstation__user__email=user_email)
        ).order_by('start').filter(
            end__gt=sn_misc.get_now_utc()
        ).first()
    )
