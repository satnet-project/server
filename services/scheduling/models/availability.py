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

from django.db import models as django_models

import logging
logger = logging.getLogger('configuration')

from services.common import misc, simulation
from services.configuration.models import segments as segment_models
from services.configuration.models import rules as rule_models


class AvailabilitySlotsManager(django_models.Manager):
    """
    Manager for handling the main operations over the availability slots.
    """

    def create(self, groundstation, start, end):
        """
        Creates a new AvailabilitySlot object in the database and associates
        the timestamp for the start of the slot as its identifier.
        :param groundstation Chanel that this slot belongs to.
        :param start Datetime object (UTC localized) with the start of the slot.
        :param end Datetime object (UTC localized) with the end of the slot.
        :return A reference to the new object.
        """

        # 1) if there already exists one availability slots for this ground
        #       station ranging from the same start to the same end, then this
        #       slot is not added.
        if self.filter(
            start=start, end=end, groundstation=groundstation
        ).exists():

            logger.warn(
                '@AvailabilitySlotsManager.create(), CONFLICTING SLOT:\n' +
                '\t * slot already exists GS = ' + str(
                    groundstation.identifier
                ) + ', start = <' + start.isoformat() + '>, end = <' +
                end.isoformat() + '>'
            )
            return

        return super(AvailabilitySlotsManager, self).create(
            identifier=AvailabilitySlot.create_identifier(
                groundstation, start
            ),
            groundstation=groundstation,
            start=start,
            end=end
        )

    def get_applicable(self, groundstation, start=None, end=None):
        """
        This method returns all the availability slots that can be applied
        within the given interval defined by the start and the duration.
        :param groundstation: The object of the GroundStation.
        :param start: Start of the applicability slot.
        :param end: End of the applicability slot.
        :return: The list of the applicable AvailabilitySlots during the
        defined applicability slot.
        """
        if start is None or end is None:
            start, end = simulation.OrbitalSimulator.get_simulation_window()
        elif start >= end:
            raise TypeError(
                '<start=' + str(
                    start
                ) + '> should occurr sooner than <end=' + str(end) + '>'
            )

        result = []

        for a_i in self.filter(
            groundstation=groundstation
        ).filter(
            start__lt=end
        ).filter(
            end__gt=start
        ):

            result.append(
                AvailabilitySlotsManager.truncate(a_i, start=start, end=end)
            )

        return result

    def add_slots(self, groundstation, slot_list):
        """Adds a list of slots.
        This method adds a list of slots to the AvailabilitySlot's table.
        :param groundstation: The GroundStation that all these slots will be
        associated with.
        :param slot_list: List of slots to be added to the table.
        """
        for slot_i in slot_list:

            self.create(
                groundstation=groundstation,
                start=slot_i[0],
                end=slot_i[1]
            )

    def update_slots(self, groundstation, slot_list):
        """
        Updates the table with the availability slots by checking the
        existance of the new ones into the table. If they do not exist,
        it removes them from the database. If they do exist, they are kept in
        the database.
        :param groundstation The groundstation object that generates these
        new slots.
        :param slot_list List with the new availability slots to be
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

        for slot_i in self.filter(groundstation=groundstation):

            s, e = slot_i.start, slot_i.end

            if not (s, e) in slot_list:

                removed.append((s, e))
                slot_i.delete()

            else:

                slot_list.remove((s, e))

        # 2) The remaining slots are added to the database.
        for n_a_slot in slot_list:

            self.create(groundstation, n_a_slot[0], n_a_slot[1])
            added.append((n_a_slot[0], n_a_slot[1]))

        return added, removed

    def propagate_slots(self):
        """Method for slot population.
        This method generates the future slots to be populated in the
        database for future operations.
        """
        logger.info(
            '[POPULATE] s_window = ' + str(
                simulation.OrbitalSimulator.get_simulation_window()
            )
        )
        update_window = simulation.OrbitalSimulator.get_update_window()
        logger.info('[POPULATE] p_window = ' + str(update_window))

        for gs_i in segment_models.GroundStation.objects.all():

            logger.info('[POPULATE] (1/2) Ground Station = ' + str(gs_i))

            slots_i = rule_models.AvailabilityRule.objects\
                .get_availability_slots(gs_i, interval=update_window)

            logger.info(
                '[POPULATE] (2/2) New slots = ' + misc.list_2_string(slots_i)
            )
            self.add_slots(gs_i, slots_i)

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
                '<start=' + str(start) + '> should occur sooner than <end=' +
                str(end) + '>'
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


class AvailabilitySlot(django_models.Model):
    """
    This class models the availability slots for the GroundStations. All of
    them will be stored in this table in the database.
    """
    class Meta:
        app_label = 'scheduling'

    ID_FIELDS_SEPARATOR = '-'

    objects = AvailabilitySlotsManager()

    identifier = django_models.CharField(
        'Unique identifier for this slot',
        max_length=100,
        unique=True
    )

    groundstation = django_models.ForeignKey(
        segment_models.GroundStation,
        verbose_name='GroundStation that this slot belongs to',
        default=1
    )

    start = django_models.DateTimeField('Slot start')
    end = django_models.DateTimeField('Slot end')

    @staticmethod
    def create_identifier(groundstation, start):
        """
        Creates the identifier for the given availability slot.
        :param groundstation: Reference to the Ground Station that owns this
                                availability slot
        :param start: Starting time for the availability slot
        :return: Unicode string with the identifier
        """
        return groundstation.identifier + AvailabilitySlot.ID_FIELDS_SEPARATOR\
            + str(misc.get_utc_timestamp(start))

    def __str__(self):
        """
        Unicode string representation of the contents of this object.
        :return: Unicode string.
        """
        return 'id = ' + str(self.identifier) + \
            ', start = ' + self.start.isoformat() + \
            ', end = ' + self.end.isoformat()
