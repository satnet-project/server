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

from django import dispatch as django_dispatch
from django.db.models import signals as django_signals
import logging
from services.common import ax25
from services.communications import models as comms_models
from services.leop import push as leop_push
from services.leop.models import launch as launch_models

logger = logging.getLogger('leop')


@django_dispatch.receiver(
    django_signals.post_delete, sender=launch_models.Launch
)
def launch_deleted_handler(sender, instance, **kwargs):
    """Signal Handler (post_save).
    Signal handler that triggers the removal of the related resources for a
    given Launch object.
    :param sender: Reference to the sender.
    :param instance: Reference to the Launch object whose removal triggered
                    the execution of this handler.
    :param kwargs: Additional arguments.
    """
    if instance.tle:
        instance.tle.delete()
    else:
        logger.warning(
            '@pre-delete (SIGNAL): No TLE associated with launch, id = ' +
            str(instance.identifier)
        )


@django_dispatch.receiver(
    django_signals.post_save, sender=comms_models.PassiveMessage
)
def message_received_handler(sender, instance, created, raw, **kwargs):
    """
    Handler that feeds the received messages to the clients connected through
    the push suscription services.
    :param instance: Instance of the new message received
    :param created: Flag that marks whether this objects has just been created
    :param raw: Flag that marks whether this object is stable or not
    :param kwargs: Additional parameters
    """
    if not created or raw:
        return

    leop_push.LaunchPush.trigger_received_frame_event(instance)

    send_exocube(instance.message)



def send_exocube(data):
    """WORKAROUND
    {
        "mission":"exocube",
        "live":0,
        "name":"anonymous",
        "callsign":"anonymous",
        "lat":35.3471,
        "long":-120.4553,
        "time":1,
        "rssi":0.0,
        "range":null,
        "az":null,
        "el":null,
        "packet":"C09C6C86A040400296966C908E861503CC450000F700004000011184968141931DE0000001C350000200E34D0501C7C79660724969000500090050006A00A374FE015D74FF02776B00C56C00C31C006A001C00C36A004A006B00C3000000000000966A006A006A00C2D2580000D1270000003E09B30400000024F400000A30000113DC000DB800000425C80009E18800D513B0A3E4000000B2007200001E29000000000000A600A600000000000000000000000000000000000067FFCD01EE00000000000000000000000080000000000027013700000D1A00045794000000004E364350202031000000000000000000000000FF00000000DA6C05A0008700C300000000000000C0"
    }
    Specific method for sending an AX.25 frame to the EXOCUBE server.
    :param data: Data message to be sent (hex string)
    """
    logger.info('>>> FORWARDING TO EXOCUBE')
    ax25_p = ax25.AX25Packet.decode_base64(data)
    logger.info('Received PACKET, decoding ax25 = ' + str(ax25_p))
