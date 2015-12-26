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

from datetime import timedelta as py_timedelta
from django.db import models as django_models
import logging

from services.common import simulation, misc as sn_misc, slots as sn_slots
from services.configuration.models import segments as segment_models
from services.simulation import push as simulation_push

logger = logging.getLogger('simulation')


class PassManager(django_models.Manager):
    """Database manager
    Manager that contains the helper methods to handle the Pass objects within
    the database.
    """

    # Embedded OrbitalSimulator object.
    _simulator = None

    def __init__(self):
        """Overriden constructor
        It sets upt the initial orbital simulator.
        """
        self._simulator = simulation.OrbitalSimulator()
        super(PassManager, self).__init__()

    def create(self, spacecraft, groundstation, start, end, **kwargs):
        """Overriden method
        Overriden method that creates the provided pass slot in case a similar
        one does not exist.
        :param spacecraft: The spacecraft involved in the operational slot
        :param groundstation: The groundstation for the pass
        :param start: The start datetime object of the pass
        :param end: The end datetime object of the pass
        :param kwargs: Additional parameters
        :return: A reference to the just created object
        """
        s_range = (
            start - py_timedelta(seconds=30),
            start + py_timedelta(seconds=30)
        )
        e_range = (
            end - py_timedelta(seconds=30),
            end + py_timedelta(seconds=30)
        )

        if self.filter(
            groundstation=groundstation, spacecraft=spacecraft,
            start__range=s_range, end__range=e_range
        ).exists():

            logger.warn(
                '@PassManager.create(), CONFLICTING SLOT:\n' +
                '\t * slot already exists GS = ' + str(
                    groundstation.identifier
                ) + ', start = <' + start.isoformat() + '>, end = <' +
                end.isoformat() + '>'
            )
            return None

        return super(PassManager, self).create(
            spacecraft=spacecraft, groundstation=groundstation,
            start=start, end=end, **kwargs
        )

    def set_spacecraft(self, spacecraft):
        """
        Sets the Spacecraft for which the embeded simulator will calculate
        the OperationalSlot set.
        :param spacecraft: The Spacecraft object as read from the Spacecraft
        database.
        """
        self._simulator.set_spacecraft(spacecraft.tle)

    def _calculate_passes(self, spacecraft, groundstation, window=None):
        """Private method
        Calculates all the pass slots for the given spacecraft, groundstation
        pair during the simulation window returned by the simulator.
        :param spacecraft: The spacecraft object
        :param groundstation: The groundstation object
        :param window: Start, end tuple that define the simulation window
        :return: Array with the pass slots
        """
        all_slots = []

        if not window:
            window = simulation.OrbitalSimulator.get_simulation_window()

        try:

            slots = self._simulator.calculate_pass_slot(window[0], window[1])

            for s in slots:

                self.create(
                    spacecraft=spacecraft, groundstation=groundstation,
                    start=s[0], end=s[1]
                )

            all_slots += slots

        except Exception as ex:

            logger.exception(
                'Error while creating pass slots, context = ' +
                'sc.id = ' + str(spacecraft.identifier) + '\n' +
                'tle.id = ' + str(spacecraft.tle.identifier) + '\n' +
                'ex = ' + str(ex),
                ex
            )

        return all_slots

    def create_pass_slots_sc(self, spacecraft):
        """Manager method
        Creates all the passes in the table for this spacecraft with all the
        registered GroundStations.
        :param spacecraft: Spacecraft object
        """
        all_slots = []
        self.set_spacecraft(spacecraft)

        for groundstation in segment_models.GroundStation.objects.all():

            self._simulator.set_groundstation(groundstation)
            all_slots += self._calculate_passes(spacecraft, groundstation)

        simulation_push.SimulationPush.trigger_passes_updated_event()
        return all_slots

    def create_pass_slots_gs(self, groundstation):
        """Manager method
        Creates all the passes in the table for this groundstation with all the
        registered Spacecraft.
        :param groundstation: Groundstation object
        """
        all_slots = []
        self._simulator.set_groundstation(groundstation)

        for spacecraft in segment_models.Spacecraft.objects.all():

            self.set_spacecraft(spacecraft)
            all_slots += self._calculate_passes(spacecraft, groundstation)

        simulation_push.SimulationPush.trigger_passes_updated_event()
        return all_slots

    def is_duplicated(self, interval, groundstation, spacecraft):
        """Manager method
        Checks whether the on-going propagation of the passes is a duplicated
        one in the sense that the system has reloaded within the propagation.
        This situation has to be avoided since the generated slot passes will
        be duplicated. This check is done in a pair sc/gs basis so that in case
        the slots where not propagated for this given pair, they do have to get
        propagated now.

        :param interval: Interval for the propagation of the slots
        :param groundstation: Groundstation object
        :param spacecraft: Spacecraft object
        :return: 'True' in case this interval has already been propagated.
        """
        last_pass = self.filter(
            groundstation=groundstation, spacecraft=spacecraft
        ).latest('start')

        if not last_pass:
            return False

        if last_pass.end > interval[0]:
            return True
        else:
            return False

    def propagate(
        self, interval=simulation.OrbitalSimulator.get_update_window()
    ):
        """Manager method
        Propagates the pass slots for all the registered groundstation and
        spacecraft pairs.

        @param interval: interval for the propagation
        """
        all_slots = []

        logger.info(
            '>>> @passes.propagate.window = ' + sn_slots.string(interval)
        )

        for gs in segment_models.GroundStation.objects.all():
            logger.info('>>> @passes.propagate, gs = ' + str(gs.identifier))
            self._simulator.set_groundstation(gs)

            for sc in segment_models.Spacecraft.objects.all():
                logger.info(
                    '>>> @passes.propagate, sc = ' + str(sc.identifier)
                )
                if not self.is_duplicated(interval, gs, sc):
                    self.set_spacecraft(sc)
                    all_slots += self._calculate_passes(sc, gs, interval)
                    logger.info(
                        sn_misc.list_2_string(
                            all_slots, name='@passes.propagate.all_slots'
                        )
                    )
                else:
                    logger.info('>>> @passes.propagate, DUPLICATED')

        if all_slots:
            simulation_push.SimulationPush.trigger_passes_updated_event()

        return all_slots

    def remove_pass_slots_sc(self, spacecraft):
        """Manager method
        Removes all the pass slots related to this spacecraft.
        :param spacecraft: Spacecraft object
        """
        self.filter(spacecraft=spacecraft).delete()
        simulation_push.SimulationPush.trigger_passes_updated_event()

    def remove_pass_slots_gs(self, groundstation):
        """Manager method
        Removes all the pass slots related to this groundstation.
        :param groundstation: Groundstation object
        """
        self.filter(groundstation=groundstation).delete()
        simulation_push.SimulationPush.trigger_passes_updated_event()


class PassSlots(django_models.Model):
    """Database model
    Model that contains the passes in between the available Spacecraft and
    GroundStations.
    """
    class Meta:
        app_label = 'simulation'

    objects = PassManager()

    spacecraft = django_models.ForeignKey(
        segment_models.Spacecraft,
        verbose_name='Spacecraft linked to this pass'
    )
    groundstation = django_models.ForeignKey(
        segment_models.GroundStation,
        verbose_name='GroundStation linked to this pass'
    )

    start = django_models.DateTimeField('Slot start')
    end = django_models.DateTimeField('Slot end')

    def __str__(self):
        """Unicode string
        :return: Unicode string
        """
        return u'>>> pass: ' + str(self.start) + u', ' + str(self.end)
