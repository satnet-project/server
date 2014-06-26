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

from django.db.models import signals

from booking.models.tle import TwoLineElementsManager
from booking.models.operational import OperationalSlotsManager
from configuration.models.availability import AvailabilitySlotsManager,\
    AvailabilitySlot
from configuration.models.channels import GroundStationChannel,\
    SpacecraftChannel
from configuration.models.compatibility import ChannelCompatibilityManager
from configuration.models.rules import AvailabilityRuleOnce,\
    AvailabilityRuleDaily, AvailabilityRuleWeekly
from configuration.models.segments import Spacecraft


def connect_rules_2_availability():
    """
    This function connects all the signals triggered during the creation/save
    of a rule with the callbacks for updating the AvailabilitySlots table.
    """
    signals.post_save.connect(
        AvailabilitySlotsManager.availability_rule_updated,
        sender=AvailabilityRuleOnce
    )
    signals.post_save.connect(
        AvailabilitySlotsManager.availability_rule_updated,
        sender=AvailabilityRuleDaily
    )
    signals.post_save.connect(
        AvailabilitySlotsManager.availability_rule_updated,
        sender=AvailabilityRuleWeekly
    )

    signals.post_delete.connect(
        AvailabilitySlotsManager.availability_rule_updated,
        sender=AvailabilityRuleOnce
    )
    signals.post_delete.connect(
        AvailabilitySlotsManager.availability_rule_updated,
        sender=AvailabilityRuleDaily
    )
    signals.post_delete.connect(
        AvailabilitySlotsManager.availability_rule_updated,
        sender=AvailabilityRuleWeekly
    )


def connect_segments_2_compatibility():
    """
    This function connects all the signals triggered during the
    creation/save/removal of a segment (either a GroundStaiton or a
    Spacecraft), with some callback functions at the SegmentCompatibility
    table that are responsible for updating the contents of the latter.
    """
    signals.post_save.connect(
        ChannelCompatibilityManager.gs_channel_saved,
        sender=GroundStationChannel
    )
    signals.post_save.connect(
        ChannelCompatibilityManager.sc_channel_saved,
        sender=SpacecraftChannel
    )
    signals.pre_delete.connect(
        ChannelCompatibilityManager.gs_channel_deleted,
        sender=GroundStationChannel
    )
    signals.pre_delete.connect(
        ChannelCompatibilityManager.sc_channel_deleted,
        sender=SpacecraftChannel
    )


def connect_segments_2_booking_tle():
    """
    This function connects all the signals triggered during the
    creation/save/removal of a segment (either a GroundStaiton or a
    Spacecraft), with some callback functions at the NoradTLE models.
    """
    signals.post_save.connect(
        TwoLineElementsManager.spacecraft_added,
        sender=Spacecraft
    )
    signals.pre_delete.connect(
        TwoLineElementsManager.spacecraft_removed,
        sender=Spacecraft
    )


def connect_availability_2_operational():
    """
    This function connects all the signals triggered during the
    creation/save/removla of an AvailabilitySlots to the OperationalSlots
    table.
    """
    signals.post_save.connect(
        OperationalSlotsManager.availability_slot_added,
        sender=AvailabilitySlot
    )
    signals.pre_delete.connect(
        OperationalSlotsManager.availability_slot_removed,
        sender=AvailabilitySlot
    )


def connect_compatibility_2_operational():
    """

    :return:
    """
    pass