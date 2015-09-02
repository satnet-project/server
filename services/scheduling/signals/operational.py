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

from services.configuration.models import availability as availability_models
from services.scheduling.models import compatibility as compatibility_models
from services.scheduling.models import operational as operational_models


# noinspection PyUnusedLocal
@django_dispatch.receiver(
    django_signals.post_save,
    sender=compatibility_models.ChannelCompatibility
)
def compatibility_added(sender, instance, created, raw, **kwargs):
    """
    Updates the available Operational Slots after a new compatibility entry
    has been added to the Compatibility table.
    :param sender: any sender is accepted
    :param instance: Reference to the just created object
    :param created: Flag that indicates that this object has just been created
    :param raw: Flag that indicates that the object is not stable within the db
    :param kwargs: Additional parameters
    """
    if not created or raw:
        return


# noinspection PyUnusedLocal
@django_dispatch.receiver(
    django_signals.pre_delete,
    sender=compatibility_models.ChannelCompatibility
)
def compatibility_deleted(sender, instance, **kwargs):
    """
    Updates the available Operational Slots after an existing compatibility
    entry has been deleted from the Compatibility table.
    :param sender: any sender is accepted
    :param instance: Reference to the just created object
    :param kwargs: Additional parameters
    """
    operational_models.OperationalSlot.objects.filter(
        compatible_channels=instance
    ).delete()


# noinspection PyUnusedLocal
@django_dispatch.receiver(
    django_signals.post_save,
    sender=availability_models.AvailabilitySlot
)
def availability_slot_added(sender, instance, **kwargs):
    """
    Callback for updating the OperationalSlots table when an AvailabilitySlot
    has just been created.
    :param sender The object that sent the signal.
    :param instance The instance of the object itself.
    :param kwargs: Additional parameters
    """
    operational_models.OperationalSlotsManager.availability_slot_added(
        sender, instance, **kwargs
    )


# noinspection PyUnusedLocal
@django_dispatch.receiver(
    django_signals.pre_delete,
    sender=availability_models.AvailabilitySlot
)
def availability_slot_deleted(sender, instance, **kwargs):
    """
    Callback for updating the OperationalSlots table when an AvailabilitySlot
    has just been removed.
    :param sender The object that sent the signal.
    :param instance The instance of the object itself.
    :param kwargs: Additional parameters
    """
    operational_models.OperationalSlot.objects.filter(
        availability_slot=instance
    ).delete()
