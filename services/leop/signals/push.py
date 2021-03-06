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

from services.common import pusher as satnet_push
from services.leop.models import launch as launch_models


@django_dispatch.receiver(
    django_signals.post_save,
    sender=launch_models.Launch
)
def launch_updated_handler(sender, instance, created, raw, **kwargs):
    """
    Invokes the LAUNCH_UPDATED event through the push channel.
    :param sender: Launch model
    :param instance: Reference to the just created Launch
    :param created: Flag that indicates that this object has just been created
    :param raw: Flag that indicates that the object is not stable within the db
    :param kwargs: Additional parameters
    """
    if created or raw:
        return

    satnet_push.PushService().trigger_event(
        satnet_push.PushService.LEOP_EVENTS_CHANNEL,
        satnet_push.PushService.LEOP_UPDATED_EVENT,
        {'identifier': instance.identifier}
    )


@django_dispatch.receiver(
    django_signals.pre_delete,
    sender=launch_models.Launch
)
def leop_removed_handler(sender, instance, **kwargs):
    """
    Invokes the LAUNCH_FINISHED event through the push channel.
    :param sender: Launch model
    :param instance: Reference to the just created Launch
    :param kwargs: Additional parameters
    """
    # ### TODO Implement this signal for users to be terminated
    pass