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

from django.db.models import signals as django_signals
from django import dispatch as django_dispatch
import logging
from website import settings as satnet_cfg
from services.simulation import push as simulation_push
from services.simulation.models import passes as pass_models

logger = logging.getLogger('simulation')


# noinspection PyUnusedLocal
@django_dispatch.receiver(
    django_signals.post_save, sender=pass_models.PassSlots
)
def passes_updated(sender, instance, created, raw, **kwargs):
    """Signal handler (post_save)
    Handles the events related with the update of the passes, either the
    creation of new ones or the update of the existing passes. It triggers the
    execution of a remote event through the available push service.
    :param sender: Reference to the sender
    :param instance: Reference to the TLE that jas just been updated
    :param created: Flag that indicates that this object has just been created
    :param raw: Flag that indicates whether the database is stable or not
    :param kwargs: Additional arguments
    """
    if raw:
        return

    if satnet_cfg.USE_PUSHER:
        simulation_push.SimulationPush.trigger_passes_updated_event()


# noinspection PyUnusedLocal
@django_dispatch.receiver(
    django_signals.pre_delete, sender=pass_models.PassSlots
)
def passes_removed(sender, instance, **kwargs):
    """Signal Handler (post_save).
    Signal handler that triggers the removal of the related simulation
    resources for a given Spacecraft.
    :param sender: Reference to the sender.
    :param instance: Reference to the Spacecraft object whose removal
                    triggered the execution of this handler.
    :param kwargs: Additional arguments.
    """
    if satnet_cfg.USE_PUSHER:
        simulation_push.SimulationPush.trigger_passes_updated_event()
