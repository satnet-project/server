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
from services.configuration.models import rules as rule_models


# noinspection PyUnusedLocal
@django_dispatch.receiver(
    django_signals.pre_delete, sender=channel_models.GroundStationChannel
)
def groundstation_channel_deleted(sender, instance, **kwargs):
    """
    Signal receiver to delete the rules associated to a Ground Station
    channel once this has been deleted.
    :param sender: Any sender is accepted
    :param instance: The instance of the Ground Station channel
    :param kwargs: Additional parameters
    """
    rule_models.AvailabilityRule.objects.filter(gs_channel=instance).delete()
