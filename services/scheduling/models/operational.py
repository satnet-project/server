
import logging

from django.db import models as django_models
from django.db.models import Q

from services.common import misc as sn_misc, slots as sn_slots
from services.scheduling.models import availability as availability_models
from services.scheduling.models import compatibility as compatibility_models
from services.simulation.models import passes as pass_models

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


logger = logging.getLogger('scheduling')

TEST_O_SLOT_ID = 'Test, SLOT -1'

# Possible states for the slots.
STATE_FREE = str('FREE')
STATE_SELECTED = str('SELECTED')
STATE_RESERVED = str('RESERVED')
STATE_DENIED = str('DENIED')
STATE_CANCELED = str('CANCELED')
STATE_REMOVED = str('REMOVED')


class OperationalSlotsManager(django_models.Manager):
    """
    Manager for handling all the operations associated with the objects from
    the OperationalSlots table.
    """
    _test_mode = False
    _test_last_id = 0

    def set_debug(self, on=True):
        """
        This method sets the OrbitalSimulator debug mode ON (on=True) or OFF
        (on=False). Default: on=True

        :param on: Flag that enables/disables the internal debug mode
        """
        self._test_mode = on

    def reset_ids_counter(self):
        """
        Resets to 0 the identifier used when in debug mode for creating the
        IDS in a predictable manner.
        """
        self._test_last_id = 0

    def create_identifier(self, groundstation, spacecraft, start):
        """
        This method creates a unique identifier for this OperationalSlot
        based on the information of the channels related with the slot itself.
        :param groundstation: The GroundStation that owns this OperationalSlot.
        :param spacecraft: The Spacecraft that owns this  OperationalSlot.
        :param start: Datetime object that designates the start of the slot.
        :return: The just created identifier as a String.
        """
        if self._test_mode:
            self._test_last_id += 1
            return str(self._test_last_id)
        else:
            return str(
                groundstation.identifier
            ) + OperationalSlot.ID_FIELDS_SEPARATOR + str(
                spacecraft.identifier
            ) + OperationalSlot.ID_FIELDS_SEPARATOR + str(
                sn_misc.get_utc_timestamp(start)
            )

    def create_test_slot(self):
        """
        Creates a new OperationalSlot in the database.

        :return: The just created object in the database
        """
        today = sn_misc.get_today_utc()
        return super(OperationalSlotsManager, self).create(
            identifier=TEST_O_SLOT_ID, start=today, end=today
        )

    def create(self, pass_slot, availability_slot, start, end):
        """
        Creates a new OperationalSlot in the database.

        :param pass_slot: Pass slot
        :param availability_slot: The availability slot during which the
            channel of the GroundStation can be operated
        :param start: The start of the operational slot
        :param end: The end of the operational slot
        :return: The just created object in the database
        """
        return super(OperationalSlotsManager, self).create(
            identifier=self.create_identifier(
                pass_slot.groundstation, pass_slot.spacecraft, start
            ),
            start=start,
            end=end,
            pass_slot=pass_slot,
            availability_slot=availability_slot
        )

    def update_state(
        self, state=STATE_FREE, slots=None
    ):
        """
        Updates the state of the OperationalSlots implementing the policy for
        the change in the state of the OperationalSlots should be included
        before updating the slots themselves, together with setting/unsetting
        the flag for the notification of changes.

        :param state: The new state requested for the OperationalSlots
        :param slots: List with all the OperationalSlots whose state must be
        changed
        :return: List with the final state of the OperationalSlots whose
        update was requested
        """
        if slots is None:
            slots = self.all()

        result = []

        for slot_i in slots:

            try:
                slot_i.change_state(new=state)
                result.append(slot_i)
            except ValueError as e:
                logger.warning(str(e))
                continue

        return result

    @staticmethod
    def _slots_query(start, end):
        """Private method
        Returns the Q() expression to properly filter the applicable slots for
        the given window. This expression selects the following set of slots:
            1) all the slots that completely occur within the window,
            2) all the slots that starts before the window and end after it
                starts,
            3) all the slots that end after the window and start before it ends,
            4) all the slots that start before the window and end after it ends.

        IMPORTANT: It does not truncate slots selected with criterions
        {2, 3, 4}, being this an issue left for further steps if it is
        strictly require to meet the restrictions of the window.

        NOTE: This Q() expression can be either used with Availability or with
        Operational slots.

        :param start: Start of the window
        :param end: End of the window
        :return: Q() expression to be used together with filter()
        """
        return \
            Q(start__gte=start) & Q(end__lte=end) | \
            Q(start__lt=start) & Q(end__gt=start) & Q(end__lte=end) | \
            Q(end__gt=end) & Q(start__lt=start) & Q(end__lte=end) | \
            Q(start__lte=start) & Q(end__gte=end)

    def availability_generates_slots(self, availability_slot):
        """
        Method that generates the Operational slots corresponding to the given
        Availability slot.

        :param availability_slot: reference to the Availability object
        """
        logger.info(
            '>>> @availability_generates_slots.availability_slot = ' + str(
                availability_slot
            )
        )

        # 1) Pass slots for all the spacecraft that:
        #   (a) are compatible with the GroundStation whose rules update
        #       provoked the generation of this Availability slot,
        #   (b) occur within the applicability range of the Availability slot

        compatible_p_slots = pass_models.PassSlots.objects.filter(
            groundstation=availability_slot.groundstation,
            spacecraft__in=[
                c.spacecraft for c in
                compatibility_models.ChannelCompatibility.objects.filter(
                    groundstation=availability_slot.groundstation
                )
            ]
        )

        p_slots = compatible_p_slots.filter(
            OperationalSlotsManager._slots_query(
                availability_slot.start,
                availability_slot.end
            )
        )

        logger.info(
            '>>> @availability_generates_slots.compatible_p_slots = ' +
            sn_misc.list_2_string(compatible_p_slots)
        )
        logger.info(
            '>>> @availability_generates_slots.p = ' + sn_misc.list_2_string(
                p_slots
            )
        )

        # 2) we filter the pass slots that are applicable to the window of this
        #       availability slot; truncating the first and the last one if
        #       necessary

        for p in p_slots:

            start, end = sn_slots.cutoff(
                (availability_slot.start, availability_slot.end),
                (p.start, p.end)
            )

            self.create(
                availability_slot=availability_slot,
                pass_slot=p, start=start, end=end
            )

    def pass_generates_slots(self, pass_slot):
        """
        Method that generates all the Operational slots related to the newly
        created pass slot.

        :param pass_slot: reference to the Pass slot
        """

        # 0) Check compatibility... if not compatible, no slot
        if not compatibility_models.ChannelCompatibility.objects.filter(
            groundstation=pass_slot.groundstation,
            spacecraft=pass_slot.spacecraft
        ).exists():

            logger.warn('No compatibility for pass slot = ' + str(pass_slot))
            return

        # 1) Availability slots for all the spacecraft that:
        #   (a) are owned by the GroundStation over which the Spacecraft passes,
        #   (b) occur within the applicability range of the Availability slot
        a_slots = availability_models.AvailabilitySlot.objects.filter(
            groundstation=pass_slot.groundstation
        ).filter(
            OperationalSlotsManager._slots_query(
                pass_slot.start,
                pass_slot.end
            )
        )

        # 2) we filter the pass slots that are applicable to the window of this
        #       availability slot; truncating the first and the last one if
        #       necessary
        for a in a_slots:

            start, end = sn_slots.cutoff(
                (a.start, a.end), (pass_slot.start, pass_slot.end)
            )

            self.create(
                availability_slot=a, pass_slot=pass_slot, start=start, end=end
            )

    def compatibility_generates_slots(self, compatibility):
        """
        Method that generates the operational slots whenever a compatibility
        object is added to the table.

        :param compatibility: The added compatibilty object
        """

        if compatibility_models.ChannelCompatibility.objects.exclude(
            pk=compatibility.pk
        ).filter(
            groundstation=compatibility.groundstation,
            spacecraft=compatibility.spacecraft
        ).count() != 0:

            logger.info('Compatibility object created but it is a duplicate')
            return

        for a_slot in availability_models.AvailabilitySlot.objects.filter(
            groundstation=compatibility.groundstation
        ):

            self.availability_generates_slots(a_slot)


class OperationalSlot(django_models.Model):
    """
    Database table to store all the information related to the slots and its
    operational state.
    """
    class Meta:
        app_label = 'scheduling'
        ordering = ['identifier']

    ID_FIELDS_SEPARATOR = '-'

    objects = OperationalSlotsManager()

    identifier = django_models.CharField(
        'Unique identifier for this slot',
        max_length=150,
        unique=True
    )

    availability_slot = django_models.ForeignKey(
        availability_models.AvailabilitySlot,
        verbose_name='Availability slot related with this OperationalSlot',
        null=True
    )

    pass_slot = django_models.ForeignKey(
        pass_models.PassSlots,
        verbose_name='Pass slots related with this OperationalSlot',
        null=True
    )

    start = django_models.DateTimeField('Slot start')
    end = django_models.DateTimeField('Slot end')

    STATE_CHOICES = (
        (STATE_FREE, 'Slot not assigned for operation'),
        (STATE_SELECTED, 'Slot chosen for reservation'),
        (STATE_RESERVED, 'Slot confirmed by GroundStation'),
        (STATE_DENIED, 'Slot petition denied'),
        (STATE_CANCELED, 'Slot reservation canceled'),
        (STATE_REMOVED, 'Slot removed due to a policy change')
    )

    STATE_CHANGE = {
        STATE_FREE: {
            STATE_FREE: True,
            STATE_SELECTED: True,
            STATE_RESERVED: False,
            STATE_DENIED: False,
            STATE_CANCELED: False,
            STATE_REMOVED: True,
        },
        STATE_SELECTED: {
            STATE_FREE: True,
            STATE_SELECTED: True,
            STATE_RESERVED: True,
            STATE_DENIED: True,
            STATE_CANCELED: False,
            STATE_REMOVED: True,
        },
        STATE_RESERVED: {
            STATE_FREE: True,
            STATE_SELECTED: False,
            STATE_RESERVED: True,
            STATE_DENIED: False,
            STATE_CANCELED: True,
            STATE_REMOVED: True,
        },
        STATE_DENIED: {
            STATE_FREE: True,
            STATE_SELECTED: True,
            STATE_RESERVED: False,
            STATE_DENIED: True,
            STATE_CANCELED: False,
            STATE_REMOVED: True,
        },
        STATE_CANCELED: {
            STATE_FREE: True,
            STATE_SELECTED: True,
            STATE_RESERVED: False,
            STATE_DENIED: False,
            STATE_CANCELED: True,
            STATE_REMOVED: True,
        },
        STATE_REMOVED: {
            STATE_FREE: False,
            STATE_SELECTED: False,
            STATE_RESERVED: False,
            STATE_DENIED: False,
            STATE_CANCELED: False,
            STATE_REMOVED: True,
        },
    }

    state = django_models.CharField(
        'String that indicates the current state of the slot',
        max_length=10,
        choices=STATE_CHOICES,
        default=STATE_FREE
    )

    def change_state(self, new):
        """
        Static method that returns 'True' in case the state change from
        'current' to 'new' can be performed; otherwise, it returns 'False'.
        :param new: The new state for this slot.
        :raises TypeError: any of the states (either current or new) is not
        valid.
        """
        if self.STATE_CHANGE[self.state][new]:
            self.state = new
            self.save()
        else:
            raise ValueError(
                'Change from <' + str(
                    self.state
                ) + '> to <' + str(new) + ' is forbidden.'
            )

    def __str__(self):
        """
        Unicode string representation of the contents of this object.
        :return: Unicode string.
        """
        return 'id = ' + str(
            self.identifier
        ) + ', start = ' + str(
            self.start
        ) + ', end = ' + str(
            self.end
        ) + ', state = ' + str(
            self.state
        )
