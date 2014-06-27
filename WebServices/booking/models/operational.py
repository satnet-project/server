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

from booking.models import tle
from common import misc, simulation
from configuration.models import availability, channels, compatibility


class OperationalSlotsManager(models.Manager):
    """
    Manager for handling all the operations associated with the objects from
    the Booking table.
    """

    def create(
        self, groundstation_channel, spacecraft_channel,
        start, end, availability_slot
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
            start=start, end=end,
            availability_slot=availability_slot
        )

    def create_list(
            self, groundstation_channel, spacecraft_channel, simulations
    ):
        """
        Creates all the objects from the given list.
        :param simulations: List with 3-tuple objects containing the
        a list with all the passes during a given AvailabilitySlot and the
        identifier of the AvailabilitySlot.
        :return: List with all the objects created.
        """
        o_slots = []

        for info_i in simulations:

            a_slot = availability.AvailabilitySlot.objects.get(
                identifier=info_i[1]
            )

            for pass_i in info_i[0]:

                o_slots.append(
                    self.create(
                        groundstation_channel, spacecraft_channel,
                        pass_i[0], pass_i[1],
                        a_slot
                    )
                )

        return o_slots

    @staticmethod
    def compatibility_sc_channel_added(
        sender, instance, compatible_channels, **kwargs
    ):
        """
        Handles the addition of a new SpacecraftChannel.
        :param sender: The database object that sent the signal.
        :param instance: The Channel affected by the event.
        :param compatible_channels: List with the channels compatible with
        the Channel affected by the event.
        """
        OperationalSlotsManager.update_spacecraft_channel_slots(
            instance, compatible_channels
        )

    @staticmethod
    def compatibility_gs_channel_added(
        sender, instance, compatible_channels, **kwargs
    ):
        """
        Handles the addition of a new GroundStationChannel.
        :param sender: The database object that sent the signal.
        :param instance: The Channel affected by the event.
        :param compatible_channels: List with the channels compatible with
        the Channel affected by the event.
        """
        if len(instance.groundstation_set.all()) == 0:
            return

        gs = instance.groundstation_set.all()[0]
        gs_sim = simulation.create_groundstation(gs)

        start = misc.get_today_utc()
        end = start + datetime.timedelta(days=2)

        a_slots = availability.AvailabilitySlot.objects.get_applicable(
            groundstation_channel=instance, start=start, end=end
        )

        for sc_ch_i in compatible_channels:

            sc = sc_ch_i.spacecraft_set.all()[0]
            tle_o = tle.TwoLineElement.objects.get(identifier=sc.tle_id)
            sc_sim = simulation.create_spacecraft(
                tle_o.identifier, tle_o.first_line, tle_o.second_line
            )

            operational_s = simulation.calculate_pass_slots(
                gs_sim, sc_sim, a_slots
            )

            OperationalSlot.objects.create_list(
                instance, sc_ch_i, operational_s
            )

    @staticmethod
    def compatibility_sc_channel_deleted(sender, instance, **kwargs):
        """
        Handles the removal of a new SpacecraftChannel.
        :param sender: The database object that sent the signal.
        :param instance: The Channel affected by the event.
        """
        # ### TODO Temporary insert deleted slots in a different table for
        # ### TODO clients notification.
        OperationalSlot.objects.filter(spacecraft_channel=instance).delete()

    @staticmethod
    def compatibility_gs_channel_deleted(sender, instance, **kwargs):
        """
        Handles the removal of a new GroundStationChannel.
        :param sender: The database object that sent the signal.
        :param instance: The Channel affected by the event.
        """
        # ### TODO Temporary insert deleted slots in a different table for
        # ### TODO clients notification.
        OperationalSlot.objects.filter(groundstation_channel=instance).delete()

    @staticmethod
    def availability_slot_added(sender, instance, **kwargs):
        """
        Callback for updating the OperationalSlots table when an
        AvailabilitySlot has just been added.
        :param sender The object that sent the signal.
        :param instance The instance of the object itself.
        """
        gs_ch = instance.groundstation_channel

        for comp_i in compatibility.ChannelCompatibility.objects.filter(
                groundstation_channels=gs_ch
        ):

            sc = comp_i.spacecraft_channel.spacecraft_set.all()[0]
            tle_o = tle.TwoLineElement.objects.get(identifier=sc.tle_id)
            sc_sim = simulation.create_spacecraft(
                tle_o.identifier, tle_o.first_line, tle_o.second_line
            )

            gs = gs_ch.groundstation_set.all()[0]
            gs_sim = simulation.create_groundstation(gs)

            start = misc.get_today_utc()
            end = misc.get_midnight() + datetime.timedelta(days=2)
            t_slot = availability.AvailabilitySlotsManager.truncate(
                instance, start=start, end=end
            )

            operational_s = simulation.calculate_pass_slots(
                gs_sim, sc_sim, [t_slot]
            )

            OperationalSlot.objects.create_list(
                gs_ch, comp_i.spacecraft_channel, operational_s
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
    def update_spacecraft_channel_slots(
        spacecraft_channel, groundstation_channels, start=None, end=None
    ):
        """
        Static method that updates the OperationalSlots for a given
        SpacecraftChannel.
        :param spacecraft_channel: The channel whose slots are to be updated.
        :param groundstation_channels: The list of compatible GroundStation
        channels.
        :param start: The start for the update process.
        :param end: The end for the update process.
        """
        if start is None or end is None:
            start = misc.get_today_utc()
            end = start + datetime.timedelta(days=1)

        if start >= end:
            raise TypeError(
                '<start=' + str(start) + '> '
                + 'should occurr sooner than <end=' + str(end) + '>'
            )

        sc = spacecraft_channel.spacecraft_set.all()[0]
        tle_o = tle.TwoLineElement.objects.get(identifier=sc.tle_id)
        sc_sim = simulation.create_spacecraft(
            tle_o.identifier, tle_o.first_line, tle_o.second_line
        )

        for gs_ch_i in groundstation_channels:

            gs = gs_ch_i.groundstation_set.all()[0]
            gs_sim = simulation.create_groundstation(gs)

            a_slots = availability.AvailabilitySlot.objects.get_applicable(
                groundstation_channel=gs_ch_i,
                start=start, end=end
            )

            operational_s = simulation.calculate_pass_slots(
                gs_sim, sc_sim, a_slots
            )

            OperationalSlot.objects.create_list(
                gs_ch_i, spacecraft_channel, operational_s
            )

    @staticmethod
    def populate_slots(start=None, duration=datetime.timedelta(days=1)):
        """
        Static method that generates the pass slots for the given time
        interval: [start, start+duration].
        :param start: Defines the start of the interval.
        :param duration: Defines the duration of the interval.
        :return: List with the pass slots.
        """
        if start is None:
            start = misc.get_today_utc()

        for compatible_i in compatibility.ChannelCompatibility.objects.all():

            OperationalSlotsManager.update_spacecraft_channel_slots(
                compatible_i.spacecraft_channel,
                compatible_i.groundstation_channels,
                start, duration
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
        channels.GroundStationChannel,
        verbose_name='GroundStationChannel that this slot belongs to'
    )
    spacecraft_channel = models.ForeignKey(
        channels.SpacecraftChannel,
        verbose_name='SpacecraftChannel that this slot belongs to'
    )

    start = models.DateTimeField('Slot start')
    end = models.DateTimeField('Slot end')

    # ### TODO It is right now a task for the client to check whether a slot
    # ### TODO has changed its state with respect to the previous one. Maybe
    # ### TODO future versions could include an additional table that saves
    # ### TODO notifications to be made.
    STATE_CHOICES = (
        ('FREE', 'Slot not assigned for operation'),
        ('RESERVED', 'Slot waiting for GroundStation confirmation'),
        ('CONFIRMED', 'Slot confirmed for operation'),
    )

    state = models.CharField(
        'String that indicates the current state of the slot',
        max_length=10,
        choices=STATE_CHOICES,
        default=STATE_CHOICES[0][0]
    )

    availability_slot = models.ForeignKey(
        availability.AvailabilitySlot,
        verbose_name='Availability slot that generate this operational slot'
    )

    @staticmethod
    def create_identifier(groundstation_channel, spacecraft_channel, start):
        """
        This method creates a unique identifier for this OperationalSlot
        based on the information of the channels related with the slot itself.
        :param groundstation_channel: The channel of the GroundStation that
        owns this OperationalSlot.
        :param spacecraft_channel: The channel of the Spacecraft that is
        compatible with this OperationalSlot.
        :param start: The start datetime of this slot.
        :return: The just created identifier as a String.
        """
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
        return 'id = ' + str(self.identifier)\
               + ', start = ' + str(self.start)\
               + ', end = ' + str(self.end)