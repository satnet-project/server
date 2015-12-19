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
logger = logging.getLogger('scheduling')

from django import dispatch as django_dispatch
from django.db.models import signals as django_signals

from services.configuration.models import rules as rule_models
from services.scheduling.models import availability as availability_models
from website import signals as sn_signals
from website import settings as sn_settings


# noinspection PyUnusedLocal
@django_dispatch.receiver(sn_signals.sn_loaded)
def satnet_loaded(sender, **kwargs):
    """
    Signal that indicates that the application has already been loaded and,
    therefore, the database is ready to be used.
    :param sender: Any sender is accepted
    :param kwargs: Additional parameters
    """
    logger.info('>>> scheduling@satnet_loaded (SIGNAL):  Propagate SLOTS...')
    if not sn_settings.TESTING and sn_settings.RUNNING_AS_SERVER:
        availability_models.AvailabilitySlot.objects.propagate_slots()


def rule_updated(rule):
    """
    Common handler to be invoked whenever any of the different rules is
    updated.
    :param rule: Rule object that has been updated/created
    """
    availability_models.AvailabilitySlot.objects.update_slots(
        rule.groundstation,
        rule_models.AvailabilityRule.objects.get_availability_slots(
            rule.groundstation
        )
    )


# noinspection PyUnusedLocal
@django_dispatch.receiver(
    django_signals.post_save,
    sender=rule_models.AvailabilityRuleOnce
)
def once_rule_saved(sender, instance, created, raw, **kwargs):
    """
    Signal that indicates that a Ground Station channel has been saved.
    :param sender: Any sender is accepted
    :param instance: The instance of the Ground Station channel
    :param created: Indicates whether the instance has just been created
    :param raw: Raw state of the information in the database
    :param kwargs: Additional parameters
    """
    if not created or raw:
        return

    rule_updated(instance)


# noinspection PyUnusedLocal
@django_dispatch.receiver(
    django_signals.post_save,
    sender=rule_models.AvailabilityRuleDaily
)
def daily_rule_saved(sender, instance, created, raw, **kwargs):
    """
    Signal that indicates that a Ground Station channel has been saved.
    :param sender: Any sender is accepted
    :param instance: The instance of the Ground Station channel
    :param created: Indicates whether the instance has just been created
    :param raw: Raw state of the information in the database
    :param kwargs: Additional parameters
    """
    if not created or raw:
        return

    rule_updated(instance)


# noinspection PyUnusedLocal
@django_dispatch.receiver(
    django_signals.post_save,
    sender=rule_models.AvailabilityRuleWeekly
)
def weekly_rule_saved(sender, instance, created, raw, **kwargs):
    """
    Signal that indicates that a Ground Station channel has been saved.
    :param sender: Any sender is accepted
    :param instance: The instance of the Ground Station channel
    :param created: Indicates whether the instance has just been created
    :param raw: Raw state of the information in the database
    :param kwargs: Additional parameters
    """
    if not created or raw:
        return

    rule_updated(instance)


# noinspection PyUnusedLocal
@django_dispatch.receiver(
    django_signals.post_delete,
    sender=rule_models.AvailabilityRuleOnce
)
def once_rule_deleted(sender, instance, **kwargs):
    """
    Signal that indicates that a Ground Station channel has been saved.
    :param sender: Any sender is accepted
    :param instance: The instance of the Ground Station channel
    :param kwargs: Additional parameters
    """
    rule_updated(instance)


# noinspection PyUnusedLocal
@django_dispatch.receiver(
    django_signals.post_delete,
    sender=rule_models.AvailabilityRuleDaily
)
def daily_rule_deleted(sender, instance, **kwargs):
    """
    Signal that indicates that a Ground Station channel has been saved.
    :param sender: Any sender is accepted
    :param instance: The instance of the Ground Station channel
    :param kwargs: Additional parameters
    """
    rule_updated(instance)


# noinspection PyUnusedLocal
@django_dispatch.receiver(
    django_signals.post_delete,
    sender=rule_models.AvailabilityRuleWeekly
)
def weekly_rule_deleted(sender, instance, **kwargs):
    """
    Signal that indicates that a Ground Station channel has been saved.
    :param sender: Any sender is accepted
    :param instance: The instance of the Ground Station channel
    :param kwargs: Additional parameters
    """
    rule_updated(instance)
