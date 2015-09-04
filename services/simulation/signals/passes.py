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

import logging
from django import dispatch as django_dispatch
from django.db.models import signals as django_signals

from services.configuration.models import segments as segment_models
from services.simulation.models import passes as pass_models

logger = logging.getLogger('simulation')


# noinspection PyUnusedLocal
@django_dispatch.receiver(
    django_signals.post_save,
    sender=segment_models.GroundStation
)
def groundstation_created(sender, instance, created, raw, **kwargs):
    """Signal handler (post_save)
    Generates the pass slots associated with this groundstation.
    :param sender: Reference to the sender
    :param instance: Reference to the GroundStation object whose creation/update
                    triggered the execution of this handler
    :param created: Flag that indicates that this object has just been created
    :param raw: Flag that indicates whether the database is stable or not
    :param kwargs: Additional arguments
    :return:
    """
    if not created or raw:
        return

    pass_models.PassSlots.objects.create_pass_slots_gs(instance)


# noinspection PyUnusedLocal
@django_dispatch.receiver(
    django_signals.post_save,
    sender=segment_models.GroundStation
)
def groundstation_updated(
    sender, instance, created, raw, update_fields, **kwargs
):
    """Signal handler (post_save)
    Generates the pass slots associated with this groundstation.
    :param sender: Reference to the sender
    :param instance: Reference to the GroundStation object whose creation/update
                    triggered the execution of this handler
    :param created: Flag that indicates that this object has just been created
    :param raw: Flag that indicates whether the database is stable or not
    :param update_fields: List of the fields that were updated
    :param kwargs: Additional arguments
    :return:
    """
    if created or raw:
        return

    if not update_fields:
        return

    if 'latitude' in update_fields or 'longitude' in update_fields:
        pass_models.PassSlots.objects.create_pass_slots_gs(instance)


# noinspection PyUnusedLocal
@django_dispatch.receiver(
    django_signals.pre_delete,
    sender=segment_models.Spacecraft
)
def groundstation_deleted(sender, instance, **kwargs):
    """Signal Handler (post_save).
    Signal handler that triggers the removal of the related simulation
    resources for a given Spacecraft.
    :param sender: Reference to the sender.
    :param instance: Reference to the Spacecraft object whose removal
                    triggered the execution of this handler.
    :param kwargs: Additional arguments.
    """
    pass_models.PassSlots.objects.remove_pass_slots_gs(instance)


# noinspection PyUnusedLocal
@django_dispatch.receiver(
    django_signals.post_save,
    sender=segment_models.Spacecraft
)
def spacecraft_created(sender, instance, created, raw, **kwargs):
    """Signal Handler (post_save).
    Signal handler that triggers the creation or update of the related
    simulation resources for a given Spacecraft.
    :param sender: Reference to the sender.
    :param instance: Reference to the Spacecraft object whose creation/update
                    triggered the execution of this handler.
    :param created: Flag that indicates that this object has just been created.
    :param raw: Flag that indicates whether the database is stable or not.
    :param kwargs: Additional arguments.
    """
    if not created or raw:
        return

    pass_models.PassSlots.objects.create_pass_slots_sc(instance)


# noinspection PyUnusedLocal
@django_dispatch.receiver(
    django_signals.post_save,
    sender=segment_models.Spacecraft
)
def spacecraft_updated(sender, instance, created, raw, **kwargs):
    """Signal Handler (post_save).
    Signal handler that triggers the creation or update of the related
    simulation resources for a given Spacecraft.
    :param sender: Reference to the sender.
    :param instance: Reference to the Spacecraft object whose creation/update
                    triggered the execution of this handler.
    :param created: Flag that indicates that this object has just been created.
    :param raw: Flag that indicates whether the database is stable or not.
    :param kwargs: Additional arguments.
    """
    if created or raw:
        return

    pass_models.PassSlots.objects.remove_pass_slots_sc(instance)
    pass_models.PassSlots.objects.create_pass_slots_sc(instance)


# noinspection PyUnusedLocal
@django_dispatch.receiver(
    django_signals.pre_delete,
    sender=segment_models.Spacecraft
)
def spacecraft_deleted(sender, instance, **kwargs):
    """Signal Handler (post_save).
    Signal handler that triggers the removal of the related simulation
    resources for a given Spacecraft.
    :param sender: Reference to the sender.
    :param instance: Reference to the Spacecraft object whose removal
                    triggered the execution of this handler.
    :param kwargs: Additional arguments.
    """
    pass_models.PassSlots.objects.filter(spacecraft=instance).delete()
