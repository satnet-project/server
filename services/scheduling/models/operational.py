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
import logging
from django.db import models
from django.db.models import Q
from services.common import misc, simulation
from services.configuration.models import availability, channels, compatibility
from services.configuration.models import tle


logger = logging.getLogger('scheduling')

# Possible states for the slots.
STATE_FREE = str('FREE')
STATE_SELECTED = str('SELECTED')
STATE_RESERVED = str('RESERVED')
STATE_DENIED = str('DENIED')
STATE_CANCELED = str('CANCELED')
STATE_REMOVED = str('REMOVED')


class OperationalSlotsManager(models.Manager):
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
        """
        self._test_mode = on

    def reset_ids_counter(self):
        """
        Resets to 0 the identifier used when in debug mode for creating the
        IDS in a predictable manner.
        """
        self._test_last_id = 0

    def create_identifier(
            self, groundstation_channel, spacecraft_channel, start
    ):
        """
        This method creates a unique identifier for this OperationalSlot
        based on the information of the channels related with the slot itself.
        :param groundstation_channel: The channel of the GroundStation that
        owns this OperationalSlot.
        :param spacecraft_channel: The channel of the Spacecraft that is
        compatible with this OperationalSlot.
        :param start: Datetime object that designates the start of the slot.
        :return: The just created identifier as a String.
        """
        if self._test_mode:
            self._test_last_id += 1
            return str(self._test_last_id)
        else:
            return groundstation_channel.identifier\
                + OperationalSlot.ID_FIELDS_SEPARATOR\
                + spacecraft_channel.identifier\
                + OperationalSlot.ID_FIELDS_SEPARATOR\
                + str(misc.get_utc_timestamp(start))

    # Embedded OrbitalSimulator object.
    _simulator = None

    def get_simulator(self):
        """
        The embedded simulator should be accessed always through this
        function, since it is the responsible for creating it in case it does
        not exist. Several problems while including the creation of the
        embedded simulator within this class forced the implementation of
        this solution.
        """
        if self._simulator is None:

            self._simulator = simulation.OrbitalSimulator()
            tle.TwoLineElementsManager.load_tles()

        return self._simulator

    def set_spacecraft(self, spacecraft):
        """
        Sets the Spacecraft for which the embeded simulator will calculate
        the OperationalSlot set.
        :param spacecraft: The Spacecraft object as read from the Spacecraft
        database.
        """
        simulator = self.get_simulator()
        simulator.set_spacecraft(spacecraft.tle)

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
            identifier=self.create_identifier(
                groundstation_channel, spacecraft_channel, start
            ),
            groundstation_channel=groundstation_channel,
            spacecraft_channel=spacecraft_channel,
            start=start,
            end=end,
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

    def get_spacecraft_changes(self, spacecraft):
        """
        Returns the list of OperationalSlots that have suffered changes for
        the given Spacecraft. After returning that list, it changes the flag
        "sc_notified" to True.
        :param spacecraft: The Spacecraft for which the OperationalSlots are
        requested.
        :return: List with all the OperationalSlots.
        """
        result = []

        for sc_ch_i in channels.SpacecraftChannel.objects.filter(
            enabled=True, spacecraft=spacecraft
        ):

            o_slots_i = self\
                .filter(spacecraft_channel=sc_ch_i)\
                .filter(sc_notified=False)
            result += o_slots_i
            o_slots_i.update(sc_notified=True)

        if len(result) == 0:
            raise Exception(
                'No OperationalSlots available for Spacecraft <' + str(
                    spacecraft.identifier
                ) + '>'
            )

        # Once notified, 'CANCELED' and 'DENIED' slots have to be
        # automatically changed to 'FREE'.
        ids_i = [s_i.identifier for s_i in result]
        OperationalSlot.objects\
            .filter(identifier__in=ids_i)\
            .filter(
                Q(state=STATE_CANCELED) | Q(state=STATE_DENIED)
            )\
            .update(state=STATE_FREE)

        return result

    def get_groundstation_changes(self, groundstation):
        """
        Returns the list of OperationalSlots that have suffered changes for
        the given Spacecraft. After returning that list, it changes the flag
        "gs_notified" to True.
        :param groundstation: The GroundStation for which the
        OperationalSlots are requested.
        :return: List with all the OperationalSlots.
        """
        result = []

        for gs_ch_i in channels.GroundStationChannel.objects.filter(
            enabled=True, groundstation=groundstation
        ):

            o_slots_i = self\
                .filter(groundstation_channel=gs_ch_i)\
                .filter(gs_notified=False)
            result += o_slots_i
            o_slots_i.update(gs_notified=True)

        if len(result) == 0:
            raise Exception(
                'No OperationalSlots available for GroundStation <' + str(
                    groundstation.identifier
                ) + '>'
            )

        return result

    def update_state(
        self, state=STATE_FREE, slots=None, notify_sc=True, notify_gs=True
    ):
        """
        Updates the state of the OperationalSlots implementing the policy for
        the change in the state of the OperationalSlots should be included
        before updating the slots themselves, together with setting/unsetting
        the flag for the notification of changes.
        :param state: The new state requested for the OperationalSlots.
        :param slots: List with all the OperationalSlots whose state must be
        changed.
        :return: List with the final state of the OperationalSlots whose
        update was requested.
        """
        if slots is None:
            slots = self.all()

        result = []

        for slot_i in slots:

            try:

                slot_i.change_state(
                    new=state, notify_sc=notify_sc, notify_gs=notify_gs
                )
                result.append(slot_i)

            except ValueError as e:

                logger.warning(str(e))
                continue

        return result

    # noinspection PyUnusedLocal
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
        OperationalSlotsManager.populate_spacecraft_channel_slots(
            instance, compatible_channels
        )

    # noinspection PyUnusedLocal
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

        OperationalSlot.objects.get_simulator().set_groundstation(
            instance.groundstation_set.all()[0]
        )

        start = misc.get_today_utc()
        end = start + datetime.timedelta(days=2)

        a_slots = availability.AvailabilitySlot.objects.get_applicable(
            groundstation_channel=instance, start=start, end=end
        )

        for sc_ch_i in compatible_channels:

            OperationalSlot.objects.set_spacecraft(
                sc_ch_i.spacecraft_set.all()[0]
            )

            operational_s = OperationalSlot.objects.get_simulator()\
                .calculate_passes(a_slots)

            OperationalSlot.objects.create_list(
                instance, sc_ch_i, operational_s
            )

    # noinspection PyUnusedLocal
    @staticmethod
    def compatibility_sc_channel_deleted(sender, instance, **kwargs):
        """
        Handles the removal of a new SpacecraftChannel.
        :param sender: The database object that sent the signal.
        :param instance: The Channel affected by the event.
        """
        OperationalSlot.objects.filter(spacecraft_channel=instance).update(
            state=STATE_REMOVED
        )

    # noinspection PyUnusedLocal
    @staticmethod
    def compatibility_gs_channel_deleted(sender, instance, **kwargs):
        """
        Handles the removal of a new GroundStationChannel.
        :param sender: The database object that sent the signal.
        :param instance: The Channel affected by the event.
        """
        OperationalSlot.objects.filter(groundstation_channel=instance).update(
            state=STATE_REMOVED
        )

    # noinspection PyUnusedLocal
    @staticmethod
    def availability_slot_added(sender, instance, **kwargs):
        """
        Callback for updating the OperationalSlots table when an
        AvailabilitySlot has just been added.
        :param sender The object that sent the signal.
        :param instance The instance of the object itself.
        """

        print('@availability_slot_added, instance = ' + str(instance))
        print('@availability_slot_added, 1')

        gs_ch = instance.groundstation_channel
        # start, end = simulation.OrbitalSimulator.get_simulation_window()
        print('@availability_slot_added, 2, gs_ch = ' + str(gs_ch.identifier))

        for comp_i in compatibility.ChannelCompatibility.objects.filter(
            groundstation_channels=gs_ch
        ):

            print('@availability_slot_added, 3, comp_sc_ch = ' + str(
                comp_i.spacecraft_channel.identifier
            ))

            misc.print_list(comp_i.spacecraft_channel.spacecraft_set.all())

            OperationalSlot.objects.set_spacecraft(
                comp_i.spacecraft_channel.spacecraft_set.all()[0]
            )
            print('@availability_slot_added, 4')
            OperationalSlot.objects.get_simulator().set_groundstation(
                gs_ch.groundstation_set.all()[0]
            )

            # t_slot = availability.AvailabilitySlotsManager.truncate(
            #     instance, start=start, end=end
            # )
            # if t_slot is None:
            #     continue

            operational_s = OperationalSlot.objects\
                .get_simulator().calculate_passes([
                    (instance.start, instance.end, instance.identifier)
                ])

            print('@availability_slot_added, operational_s = ' + str(
                operational_s
            ))

            OperationalSlot.objects.create_list(
                gs_ch, comp_i.spacecraft_channel, operational_s
            )

    # noinspection PyUnusedLocal
    @staticmethod
    def availability_slot_removed(sender, instance, **kwargs):
        """
        Callback for updating the OperationalSlots table when an
        AvailabilitySlot has just been removed.
        :param sender The object that sent the signal.
        :param instance The instance of the object itself.
        """
        OperationalSlot.objects.filter(availability_slot=instance).update(
            state=STATE_REMOVED
        )

    @staticmethod
    def populate_spacecraft_channel_slots(
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
            start, end = simulation.OrbitalSimulator.get_simulation_window()
        elif start >= end:
            raise TypeError(
                '<start=' + str(start) + '> '
                + 'should occurr sooner than <end=' + str(end) + '>'
            )

        OperationalSlot.objects.set_spacecraft(
            spacecraft_channel.spacecraft_set.all()[0]
        )

        for gs_ch_i in groundstation_channels:

            OperationalSlot.objects.get_simulator().set_groundstation(
                gs_ch_i.groundstation_set.all()[0]
            )

            a_slots = availability.AvailabilitySlot.objects.get_applicable(
                groundstation_channel=gs_ch_i,
                start=start, end=end
            )

            operational_s = OperationalSlot.objects.get_simulator()\
                .calculate_passes(a_slots)

            OperationalSlot.objects.create_list(
                gs_ch_i, spacecraft_channel, operational_s
            )

    @staticmethod
    def populate_slots(duration=datetime.timedelta(days=1)):
        """
        Static method that populates the slots for all the compatible
        channels during an interval of lenght 'duration', after the
        simulation window.
        :param duration: Time length for which the slots will be populated.
        """
        s_start, s_end = simulation.OrbitalSimulator.get_simulation_window()
        start = s_end
        end = start + duration

        for compatible_i in compatibility.ChannelCompatibility.objects.all():

            OperationalSlotsManager.populate_spacecraft_channel_slots(
                compatible_i.spacecraft_channel,
                compatible_i.groundstation_channels,
                start, end
            )


class OperationalSlot(models.Model):
    """
    Database table to store all the information related to the slots and its
    operational state.
    """
    class Meta:
        app_label = 'scheduling'
        ordering = ['identifier']

    ID_FIELDS_SEPARATOR = '-'

    objects = OperationalSlotsManager()

    identifier = models.CharField(
        'Unique identifier for this slot',
        max_length=150,
        unique=True
    )

    groundstation_channel = models.ForeignKey(
        channels.GroundStationChannel,
        verbose_name='GroundStationChannel that this slot belongs to',
        blank=True, null=True, on_delete=models.SET_NULL
    )
    spacecraft_channel = models.ForeignKey(
        channels.SpacecraftChannel,
        verbose_name='SpacecraftChannel that this slot belongs to',
        blank=True, null=True, on_delete=models.SET_NULL
    )

    start = models.DateTimeField('Slot start')
    end = models.DateTimeField('Slot end')

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

    state = models.CharField(
        'String that indicates the current state of the slot',
        max_length=10,
        choices=STATE_CHOICES,
        default=STATE_FREE
    )

    gs_notified = models.BooleanField(
        'Flag that indicates whether the changes in the status of the slot '
        'need already to be notified to the compatible GroundStation.',
        default=False
    )
    sc_notified = models.BooleanField(
        'Flag that indicates whether the changes in the status of the slot '
        'need already to be notified to the compatible Spacecraft.',
        default=False
    )

    # Deleting the related AvailabilitySlot will not provoke the removal of
    # the related rows in this table.
    availability_slot = models.ForeignKey(
        availability.AvailabilitySlot,
        verbose_name='Availability slot that generates this OperationalSlot',
        blank=True,
        null=True,
        on_delete=models.SET_NULL
    )

    def change_state(self, new, notify_sc=True, notify_gs=True):
        """
        Static method that returns 'True' in case the state change from
        'current' to 'new' can be performed; otherwise, it returns 'False'.
        :param new: The new state for this slot.
        :param notify_sc: Flag that defines whether Spacecraft should be
        notified about this change or not.
        :param notify_gs: Flag that defines whether GroundStations should be
        notified about this change or not.
        :raises TypeError: any of the states (either current or new) is not
        valid.
        """
        if self.STATE_CHANGE[self.state][new]:

            self.state = new
            self.gs_notified = not notify_gs
            self.sc_notified = not notify_sc

            self.save()

        else:

            raise ValueError('Change from <' + str(self.state) + '> to <' +
                             str(new) + ' is forbidden.')

    def __unicode__(self):
        """
        Unicode string representation of the contents of this object.
        :return: Unicode string.
        """
        return 'id = ' + str(self.identifier)\
               + ', start = ' + str(self.start)\
               + ', end = ' + str(self.end)\
               + ', state = ' + str(self.state)\
               + ', sc_notified = ' + str(self.sc_notified)\
               + ', gs_notified = ' + str(self.gs_notified)
