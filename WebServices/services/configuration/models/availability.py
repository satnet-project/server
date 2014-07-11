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

from django.db import models

from services.common import misc, simulation
from services.configuration.models import rules, channels


class AvailabilitySlotsManager(models.Manager):
    """
    Manager for handling the main operations over the availability slots.
    """

    def create(self, groundstation_channel, start, end):
        """
        Creates a new AvailabilitySlot object in the database and associates
        the timestamp for the start of the slot as its identifier.
        :param groundstation_channel Chanel that this slot belongs to.
        :param start Datetime object (UTC localized) with the start of the slot.
        :param end Datetime object (UTC localized) with the end of the slot.
        :return A reference to the new object.
        """
        return super(AvailabilitySlotsManager, self).create(
            identifier=AvailabilitySlot.create_identifier(
                groundstation_channel, start
            ),
            groundstation_channel=groundstation_channel,
            start=start,
            end=end
        )

    def get_applicable(self, groundstation_channel, start=None, end=None):
        """
        This method returns all the availability slots that can be applied
        within the given interval defined by the start and the duration.
        :param groundstation_channel: The channel of the GroundStation.
        :param start: Start of the applicability slot.
        :param end: End of the applicability slot.
        :return: The list of the applicable AvailabilitySlots during the
        defined applicability slot.
        """
        if start is None or end is None:
            start, end = simulation.OrbitalSimulator.get_simulation_window()
        elif start >= end:
            raise TypeError(
                '<start=' + str(start) + '> '
                + 'should occurr sooner than <end=' + str(end) + '>'
            )

        result = []

        for a_i in self.filter(groundstation_channel=groundstation_channel)\
                .filter(start__lt=end).filter(end__gt=start):

            result.append(
                AvailabilitySlotsManager.truncate(a_i, start=start, end=end)
            )

        return result

    def update_slots(self, groundstation_channel, new_slots):
        """
        Updates the table with the availability slots by checking the
        existance of the new ones into the table. If they do not exist,
        it removes them from the database. If they do exist, they are kept in
        the database.
        :param groundstation_channel The GroundStationChannel object that
        generates these new slots.
        :param new_slots List with the new availability slots to be
        cross-checked with the existing ones. The items in this list must be
        tuples of DateTime objects UTC localized.
        """

        # 1) First, slots that do not appear in the current list of available
        # slots, are removed from the database. If the slot is already found
        # in the database, then it will be removed from the given list of
        # availability slots. Therefore, the ones who are left in the list
        # after this first step are those who are available but were not
        # included in the database yet.
        added = []
        removed = []

        for a_slot in self.all():

            s, e = a_slot.start, a_slot.end

            if not (s, e) in new_slots:
                removed.append((s, e))
                a_slot.delete()
            else:
                new_slots.remove((s, e))

        # 2) The remaining slots are added to the database.
        for n_a_slot in new_slots:

            self.create(groundstation_channel, n_a_slot[0], n_a_slot[1])
            added.append((n_a_slot[0], n_a_slot[1]))

        return added, removed

    @staticmethod
    def availability_rule_updated(sender, instance, **kwargs):
        """
        Callback for updating the AvailabilitySlots table whenenver a new
        rule is added to the database.
        :param sender The object that sent the signal.
        :param instance The instance of the object itself.
        """
        new_slots = rules.AvailabilityRule.objects.get_availability_slots(
            instance.gs_channel
        )
        AvailabilitySlot.objects.update_slots(instance.gs_channel, new_slots)

    @staticmethod
    def truncate(slot, start, end):
        """
        Static method that truncates the duration of a given AvailabilitySlot
        to the restrictions of the (start, end) period. This way,
        the AvailabilitySlot can be utilized within that period.
        :param slot: The slot to be truncated.
        :param start: The starting date for the applicability of this slot.
        :param end: The ending date for the applicability of this slot.
        """
        if start is None or end is None:
            start, end = simulation.OrbitalSimulator.get_simulation_window()
        elif start >= end:
            raise TypeError(
                '<start=' + str(start) + '> '
                + 'should occurr sooner than <end=' + str(end) + '>'
            )

        if slot.start >= end:
            return None
        if slot.end <= start:
            return None

        if slot.start < start:
            s = start
        else:
            s = slot.start
        if slot.end > end:
            e = end
        else:
            e = slot.end

        return s, e, slot.identifier


class AvailabilitySlot(models.Model):
    """
    This class models the availability slots for the GroundStations. All of
    them will be stored in this table in the database.
    """
    class Meta:
        app_label = 'configuration'

    ID_FIELDS_SEPARATOR = '-'

    objects = AvailabilitySlotsManager()

    identifier = models.CharField(
        'Unique identifier for this slot',
        max_length=100,
        unique=True
    )
    groundstation_channel = models.ForeignKey(
        channels.GroundStationChannel,
        verbose_name='GroundStationChannel that this slot belongs to'
    )
    start = models.DateTimeField('Slot start')
    end = models.DateTimeField('Slot end')

    @staticmethod
    def create_identifier(groundstation_channel, start):

        gs = groundstation_channel.groundstation_set.all()[0]

        return gs.identifier + AvailabilitySlot.ID_FIELDS_SEPARATOR\
            + groundstation_channel.identifier\
            + AvailabilitySlot.ID_FIELDS_SEPARATOR\
            + str(misc.get_utc_timestamp(start))

    def __unicode__(self):
        """
        Unicode string representation of the contents of this object.
        :return: Unicode string.
        """
        return 'id = ' + str(self.identifier) + ', start = '\
               + self.start.isoformat() + ', end = ' + self.end.isoformat()