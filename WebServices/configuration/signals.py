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

:Author:
    Ricardo Tubio-Pardavila (rtubiopa@calpoly.edu)
"""
__author__ = 'rtubiopa@calpoly.edu'

from django.db.models.signals import post_save, post_delete

from configuration.models.availability import AvailabilitySlotsManager
from configuration.models.rules import AvailabilityRuleOnce,\
    AvailabilityRuleDaily, AvailabilityRuleWeekly


def connect_rules_2_slots():
    """
    This function connects all the signals triggered during the creation/save
    of a rule with the callbacks for updating the AvailabilitySlots table.
    """
    post_save.connect(
        AvailabilitySlotsManager.availability_rule_updated,
        sender=AvailabilityRuleOnce
    )
    post_save.connect(
        AvailabilitySlotsManager.availability_rule_updated,
        sender=AvailabilityRuleDaily
    )
    post_save.connect(
        AvailabilitySlotsManager.availability_rule_updated,
        sender=AvailabilityRuleWeekly
    )

    post_delete.connect(
        AvailabilitySlotsManager.availability_rule_updated,
        sender=AvailabilityRuleOnce
    )
    post_delete.connect(
        AvailabilitySlotsManager.availability_rule_updated,
        sender=AvailabilityRuleDaily
    )
    post_delete.connect(
        AvailabilitySlotsManager.availability_rule_updated,
        sender=AvailabilityRuleWeekly
    )

# ### Simple signal connection
connect_rules_2_slots()
