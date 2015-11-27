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
from services.configuration.models import segments as segment_models


# noinspection PyUnusedLocal
@django_dispatch.receiver(
    django_signals.post_save,
    sender=segment_models.GroundStation
)
def gs_added_or_updated_handler(sender, instance, created, raw, **kwargs):
    """
    Invokes the GS_ADDED or GS_UPDATED event through the push channel.
    :param sender: GroundStation model
    :param instance: Reference to the just created GroundStation
    :param created: Flag that indicates that this object has just been created
    :param raw: Flag that indicates that the object is not stable within the db
    :param kwargs: Additional parameters
    """
    if raw:
        return

    if created:
        satnet_push.PushService().trigger_event(
            satnet_push.PushService.CONFIGURATION_EVENTS_CHANNEL,
            satnet_push.PushService.GS_ADDED_EVENT,
            {'identifier': instance.identifier}
        )
    else:
        satnet_push.PushService().trigger_event(
            satnet_push.PushService.CONFIGURATION_EVENTS_CHANNEL,
            satnet_push.PushService.GS_UPDATED_EVENT,
            {'identifier': instance.identifier}
        )


# noinspection PyUnusedLocal
@django_dispatch.receiver(
    django_signals.pre_delete,
    sender=segment_models.GroundStation
)
def gs_removed_handler(sender, instance, **kwargs):
    """
    Invokes the GS_RMOVED event through the push channel.
    :param sender: GroundStation model
    :param instance: Reference to the just created GroundStation
    :param kwargs: Additional parameters
    """
    satnet_push.PushService().trigger_event(
        satnet_push.PushService.CONFIGURATION_EVENTS_CHANNEL,
        satnet_push.PushService.GS_REMOVED_EVENT,
        {'identifier': instance.identifier}
    )
