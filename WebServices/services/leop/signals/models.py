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
from services.common import exocube
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
    exocube.ExocubeService.send_exocube(instance)