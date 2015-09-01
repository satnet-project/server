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

from django import dispatch as django_dispatch
from django.db.models import signals as django_signals

from services.configuration.models import channels as channel_models
from services.configuration.models import compatibility as compatibility_models


# noinspection PyUnusedLocal
@django_dispatch.receiver(
    django_signals.post_save,
    sender=channel_models.GroundStationChannel
)
def groundstation_channel_saved(sender, instance, created, raw, **kwargs):
    """
    Signal that indicates that a Ground Station channel has been saved.
    :param sender: Any sender is accepted
    :param instance: The instance of the Ground Station channel
    :param created: Indicates whether the instance has just been created
    :param raw: Raw state of the information in the database
    :param kwargs: Additional parameters
    """
    if raw:
        return

    add, remove = compatibility_models.ChannelCompatibility.objects.diff_gs(
        instance
    )
    compatibility_models.ChannelCompatibility.objects.patch_gs_updated(
        instance, add, remove
    )


# noinspection PyUnusedLocal
@django_dispatch.receiver(
    django_signals.post_save,
    sender=channel_models.SpacecraftChannel
)
def spacecraft_channel_saved(sender, instance, created, raw, **kwargs):
    """
    Signal that indicates that a Spacecraft channel has been saved.
    :param sender: Any sender is accepted
    :param instance: The instance of the Spacecraft channel
    :param created: Indicates whether the instance has just been created
    :param raw: Raw state of the information in the database
    :param kwargs: Additional parameters
    """
    if raw:
        return

    add, remove = compatibility_models.ChannelCompatibility.objects.diff_sc(
        instance
    )
    compatibility_models.ChannelCompatibility.objects.patch_sc(
        instance, add, remove
    )
