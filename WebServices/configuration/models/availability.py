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

from django.db import models

from common.misc import get_utc_timestamp
from configuration.models.rules import AvailabilityRule


class AvailabilitySlotsManager(models.Manager):
    """
    Manager for handling the main operations over the availability slots.
    """

    def create(self, start, end):
        """
        Creates a new AvailabilitySlot object in the database and associates
        the timestamp for the start of the slot as its identifier.
        :param start Datetime object (UTC localized) with the start of the slot.
        :param end Datetime object (UTC localized) with the end of the slot.
        :return A reference to the new object.
        """
        return super(AvailabilitySlotsManager, self).create(
            identifier=get_utc_timestamp(start),
            start=start, end=end
        )

    def update_slots(self, new_slots):
        """
        Updates the table with the availability slots by checking the
        existance of the new ones into the table. If they do not exist,
        it removes them from the database. If they do exist, they are kept in
        the database.
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

            self.create(n_a_slot[0], n_a_slot[1])

        return removed

    @staticmethod
    def availability_rule_updated(sender, instance, **kwargs):
        """
        Callback for updating the AvailabilitySlots table whenenver a new
        rule is added to the database.
        :param sender The object that sent the signal.
        :param instance The instance of the object itself.
        """
        new_slots = AvailabilityRule.objects.get_availability_slots(
            instance.gs_channel
        )
        r_slots = AvailabilitySlots.objects.update_slots(new_slots=new_slots)
        if r_slots:
            # ### TODO ::
            # Create signal for notifying the change in the table of
            # AvailableSlots to all the other tables that depend on its
            # contents.
            print '>>> (UPDATED_RULE_SIGNAL), removed = ' + str(len(r_slots))


class AvailabilitySlots(models.Model):
    """
    This class models the availability slots for the GroundStations. All of
    them will be stored in this table in the database.
    """
    class Meta:
        app_label = 'configuration'

    objects = AvailabilitySlotsManager()

    identifier = models.BigIntegerField(
        'Unique identifier for this slot', unique=True
    )
    start = models.DateTimeField('Slot start')
    end = models.DateTimeField('Slot end')

    def __unicode__(self):
        """
        Unicode string representation of the contents of this object.
        :return: Unicode string.
        """
        return 'id = ' + str(self.identifier) + ', start = '\
               + str(self.start) + ', end = ' + str(self.end)