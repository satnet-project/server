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

from services.configuration.models import availability
from services.configuration.models import rules


def connect_rules_2_availability():
    """
    This function connects all the signals triggered during the creation/save
    of a rule with the callbacks for updating the AvailabilitySlots table.
    """

    django_signals.post_save.connect(
        availability.AvailabilitySlotsManager.availability_rule_updated,
        sender=rules.AvailabilityRuleOnce
    )
    django_signals.post_save.connect(
        availability.AvailabilitySlotsManager.availability_rule_updated,
        sender=rules.AvailabilityRuleDaily
    )
    django_signals.post_save.connect(
        availability.AvailabilitySlotsManager.availability_rule_updated,
        sender=rules.AvailabilityRuleWeekly
    )

    django_signals.post_delete.connect(
        availability.AvailabilitySlotsManager.availability_rule_updated,
        sender=rules.AvailabilityRuleOnce
    )
    django_signals.post_delete.connect(
        availability.AvailabilitySlotsManager.availability_rule_updated,
        sender=rules.AvailabilityRuleDaily
    )
    django_signals.post_delete.connect(
        availability.AvailabilitySlotsManager.availability_rule_updated,
        sender=rules.AvailabilityRuleWeekly
    )

connect_rules_2_availability()
