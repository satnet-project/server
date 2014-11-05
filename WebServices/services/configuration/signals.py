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

from django.db.models import signals

from services.configuration.models import availability, compatibility, channels
from services.configuration.models import rules
from services.scheduling.models import operational


def connect_rules_2_availability():
    """
    This function connects all the signals triggered during the creation/save
    of a rule with the callbacks for updating the AvailabilitySlots table.
    """
    signals.post_save.connect(
        availability.AvailabilitySlotsManager.availability_rule_updated,
        sender=rules.AvailabilityRuleOnce
    )
    signals.post_save.connect(
        availability.AvailabilitySlotsManager.availability_rule_updated,
        sender=rules.AvailabilityRuleDaily
    )
    signals.post_save.connect(
        availability.AvailabilitySlotsManager.availability_rule_updated,
        sender=rules.AvailabilityRuleWeekly
    )

    signals.post_delete.connect(
        availability.AvailabilitySlotsManager.availability_rule_updated,
        sender=rules.AvailabilityRuleOnce
    )
    signals.post_delete.connect(
        availability.AvailabilitySlotsManager.availability_rule_updated,
        sender=rules.AvailabilityRuleDaily
    )
    signals.post_delete.connect(
        availability.AvailabilitySlotsManager.availability_rule_updated,
        sender=rules.AvailabilityRuleWeekly
    )


def connect_channels_2_compatibility():
    """
    This function connects all the signals triggered during the
    creation/save/removal of a segment (either a GroundStaiton or a
    Spacecraft), with some callback functions at the SegmentCompatibility
    table that are responsible for updating the contents of the latter.
    """
    signals.post_save.connect(
        compatibility.ChannelCompatibilityManager.gs_channel_saved,
        sender=channels.GroundStationChannel
    )
    signals.post_save.connect(
        compatibility.ChannelCompatibilityManager.sc_channel_saved,
        sender=channels.SpacecraftChannel
    )
    signals.pre_delete.connect(
        compatibility.ChannelCompatibilityManager.gs_channel_deleted,
        sender=channels.GroundStationChannel
    )
    signals.pre_delete.connect(
        compatibility.ChannelCompatibilityManager.sc_channel_deleted,
        sender=channels.SpacecraftChannel
    )


def connect_availability_2_operational():
    """
    This function connects all the signals triggered during the
    creation/save/removla of an AvailabilitySlots to the OperationalSlots
    table.
    """
    signals.post_save.connect(
        operational.OperationalSlotsManager.availability_slot_added,
        sender=availability.AvailabilitySlot
    )
    signals.pre_delete.connect(
        operational.OperationalSlotsManager.availability_slot_removed,
        sender=availability.AvailabilitySlot
    )


def connect_compatibility_2_operational():
    """
    Connects the events (gs_ch add/remove and sc_ch add/remove) that occur at
    the Compatibility table with the OperationalSlots table.
    """
    compatibility.compatibility_add_gs_ch_signal.connect(
        operational.OperationalSlotsManager.compatibility_gs_channel_added,
        sender=compatibility.ChannelCompatibility
    )
    compatibility.compatibility_add_sc_ch_signal.connect(
        operational.OperationalSlotsManager.compatibility_sc_channel_added,
        sender=compatibility.ChannelCompatibility
    )
    compatibility.compatibility_delete_gs_ch_signal.connect(
        operational.OperationalSlotsManager.compatibility_gs_channel_deleted,
        sender=compatibility.ChannelCompatibility
    )
    compatibility.compatibility_delete_sc_ch_signal.connect(
        operational.OperationalSlotsManager.compatibility_sc_channel_deleted,
        sender=compatibility.ChannelCompatibility
    )

connect_availability_2_operational()
connect_channels_2_compatibility()
connect_compatibility_2_operational()
connect_rules_2_availability()