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

import datetime
from django.db import models

from booking.models.tle import TwoLineElement
from common import misc, simulation
from configuration.models.availability import AvailabilitySlot,\
    AvailabilitySlotsManager
from configuration.models.channels import GroundStationChannel,\
    SpacecraftChannel
from configuration.models.compatibility import ChannelCompatibility


class OperationalSlotsManager(models.Manager):
    """
    Manager for handling all the operations associated with the objects from
    the Booking table.
    """

    def create(
        self,
        groundstation_channel, spacecraft_channel,
        start, end,
        availability_slot
    ):
        """
        Creates a new OperationalSlot in the database.
        :param groundstation_channel: The channel of the GroundStation to
        which this operational slot belongs to.
        :param spacecraft_channel: The channel of the Spacecraft that is
        compatible with this operational slot.
        :param start: The start of the operational slot.
        :param end: The end of the operational slot.
        :param availability_slot: The availability slot during which the
        channel of the GroundStation can be operated.
        :return: The just created object in the database.
        """
        return super(OperationalSlotsManager, self).create(
            identifier=OperationalSlot.create_identifier(
                groundstation_channel, spacecraft_channel, start
            ),
            groundstation_channel=groundstation_channel,
            spacecraft_channel=spacecraft_channel,
            start=start,
            end=end,
            availability_slot=availability_slot
        )

    @staticmethod
    def compatibility_gs_channel_added(sender, instance, **kwargs):
        """
        Handles the addition of a new GroundStationChannel.
        :param sender The object that sent the signal.
        :param instance The instance of the object itself.
        """
        pass

    @staticmethod
    def compatibility_sc_channel_added(sender, instance, **kwargs):
        """
        Handles the addition of a new SpacecraftChannel.
        :param sender The object that sent the signal.
        :param instance The instance of the object itself.
        """
        pass

    @staticmethod
    def availability_slot_added(sender, instance, **kwargs):
        """
        Callback for updating the OperationalSlots table when an
        AvailabilitySlot has just been added.
        :param sender The object that sent the signal.
        :param instance The instance of the object itself.
        """
        gs_ch = instance.groundstation_channel

        for sc_ch_i in ChannelCompatibility.objects.filter(
                groundstation_channel=gs_ch
        ):

            sc = sc_ch_i.spacecraft_set.all()[0]
            tle = TwoLineElement.objects.get(identifier=sc.tle_id)
            sc_sim = simulation.create_spacecraft(
                tle.identifier, tle.first_line, tle.second_line
            )

            gs = gs_ch.groundstation_set.all()[0]
            gs_sim = simulation.create_groundstation(gs)

            operational_s = simulation.calculate_pass_slots(
                gs_sim, sc_sim, [instance]
            )

            for o_s_i in operational_s:

                OperationalSlot.objects.create(
                    groundstation_channel=gs_ch,
                    spacecraft_channel=sc_ch_i,
                    start=o_s_i[0], end=o_s_i[1],
                    availability_slot=o_s_i[2]
                )

    @staticmethod
    def availability_slot_removed(sender, instance, **kwargs):
        """
        Callback for updating the OperationalSlots table when an
        AvailabilitySlot has just been removed.
        :param sender The object that sent the signal.
        :param instance The instance of the object itself.
        """
        # ### TODO Temporary insert deleted slots in a different table for
        # ### TODO clients notification.
        OperationalSlot.objects.filter(availability_slot=instance).delete()

    @staticmethod
    def update_slots(start=None, duration=datetime.timedelta(days=1)):
        """
        Static method that generates the pass slots for the given time
        interval: [start, start+duration].
        :param start: Defines the start of the interval.
        :param duration: Defines the duration of the interval.
        :return: List with the pass slots.
        """
        if start is None:
            start = misc.get_today_utc()

        for sc_ch_i in ChannelCompatibility.objects.all():

            sc = sc_ch_i.spacecraft_set.all()[0]
            tle = TwoLineElement.objects.get(identifier=sc.tle_id)
            sc_sim = simulation.create_spacecraft(
                tle.identifier, tle.first_line, tle.second_line
            )

            for gs_ch_i in sc_ch_i.groundstation_channels:

                gs = gs_ch_i.groundstation_set.all()[0]
                gs_sim = simulation.create_groundstation(gs)

                a_slots = AvailabilitySlotsManager.get_availability_slots(
                    groundstation_channel=gs_ch_i,
                    start=start, duration=duration
                )

                operational_s = simulation.calculate_pass_slots(
                    gs_sim, sc_sim,
                    a_slots
                )

                for o_s_i in operational_s:

                    OperationalSlot.objects.create(
                        groundstation_channel=gs_ch_i,
                        spacecraft_channel=sc_ch_i,
                        start=o_s_i[0], end=o_s_i[1],
                        availability_slot=o_s_i[2]
                    )


class OperationalSlot(models.Model):
    """
    Database table to store all the information related to the slots and its
    operational state.
    """
    class Meta:
        app_label = 'booking'

    ID_FIELDS_SEPARATOR = '-'

    objects = OperationalSlotsManager()

    identifier = models.CharField(
        'Unique identifier for this slot',
        max_length=150,
        unique=True
    )

    groundstation_channel = models.ForeignKey(
        GroundStationChannel,
        verbose_name='GroundStationChannel that this slot belongs to'
    )
    spacecraft_channel = models.ForeignKey(
        SpacecraftChannel,
        verbose_name='SpacecraftChannel that this slot belongs to'
    )

    start = models.DateTimeField('Slot start')
    end = models.DateTimeField('Slot end')

    availability_slot = models.ForeignKey(
        AvailabilitySlot,
        verbose_name='Availability slot that generate this operational slot'
    )

    @staticmethod
    def create_identifier(groundstation_channel, spacecraft_channel, start):

        gs = groundstation_channel.groundstation_set.all()[0]
        sc = spacecraft_channel.spacecraft_set.all()[0]

        return gs.identifier + OperationalSlot.ID_FIELDS_SEPARATOR\
            + groundstation_channel.identifier\
            + OperationalSlot.ID_FIELDS_SEPARATOR\
            + sc.identifier + OperationalSlot.ID_FIELDS_SEPARATOR\
            + spacecraft_channel.identifier\
            + OperationalSlot.ID_FIELDS_SEPARATOR\
            + str(misc.get_utc_timestamp(start))

    def __unicode__(self):
        """
        Unicode string representation of the contents of this object.
        :return: Unicode string.
        """
        return 'id = ' + str(self.identifier) + ', start = '\
               + str(self.start) + ', end = ' + str(self.end)