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

from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver
import logging
from services.configuration.models import segments
from services.configuration.models import tle as tle_models
from services.simulation.models import groundtracks as gt_models

logger = logging.getLogger('simulation')


@receiver(post_save, sender=segments.Spacecraft)
def spacecraft_saved(sender, instance, created, raw, **kwargs):
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

    #pass_models.PassSlots.objects.create(instance)
    gt_models.GroundTrack.objects.create(instance)


@receiver(post_save, sender=segments.Spacecraft)
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

    # When the spacecraft is created, before updating the lists of channels
    # (ManyToMany), a first just-non-created signal is sent and should be
    # filtered.
    try:
        gt = gt_models.GroundTrack.objects.get(spacecraft=instance)
    except gt_models.GroundTrack.DoesNotExist:
        return

    if instance.tle != gt.tle:
        gt.delete()
        gt_models.GroundTrack.objects.create(instance)


@receiver(pre_delete, sender=segments.Spacecraft)
def spacecraft_deleted(sender, instance, **kwargs):
    """Signal Handler (post_save).
    Signal handler that triggers the removal of the related simulation
    resources for a given Spacecraft.
    :param sender: Reference to the sender.
    :param instance: Reference to the Spacecraft object whose removal
                    triggered the execution of this handler.
    :param kwargs: Additional arguments.
    """
    try:
        gt = gt_models.GroundTrack.objects.get(spacecraft=instance)
        gt.delete()
    except gt_models.GroundTrack.DoesNotExist:
        logger.warn(
            '>>> Spacecraft did not have an associated GT, id = ' + str(
                instance.identifier
            )
        )


@receiver(post_save, sender=tle_models.TwoLineElement)
def tle_updated(sender, instance, created, raw, **kwargs):
    """Signal handler (post_save)
    Handles the update of the groundtracks and other simulation resources that
    may change for all the registered spacecraft associated with the TLE that
    has just changed.
    :param sender: Reference to the sender
    :param instance: Reference to the TLE that jas just been updated
    :param created: Flag that indicates that this object has just been created
    :param raw: Flag that indicates whether the database is stable or not
    :param kwargs: Additional arguments
    """
    if created or raw:
        return

    for gt in gt_models.GroundTrack.objects.filter(tle=instance):

        spacecraft = gt.spacecraft
        gt.delete()
        gt_models.GroundTrack.objects.create(spacecraft)