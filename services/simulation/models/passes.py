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
from services.common import simulation
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
                    spacecraft=spacecraft,
                    groundstation=groundstation,
                    start=s[0],
                    end=s[1]
                )

            all_slots += slots

        except Exception as ex:

            logger.warning(
                'Error while creating pass slots, context = '
                + 'sc.id = ' + str(spacecraft.identifier) + '\n'
                + 'tle.id = ' + str(spacecraft.tle.identifier) + '\n'
                + 'ex = ' + str(ex)
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

    def propagate(self):
        """Manager method
        Propagates the pass slots for all the registered groundstation and
        spacecraft pairs.
        """
        all_slots = []
        window = simulation.OrbitalSimulator.get_update_window()

        for groundstation in segment_models.GroundStation.objects.all():

            self._simulator.set_groundstation(groundstation)

            for spacecraft in segment_models.Spacecraft.objects.all():

                self.set_spacecraft(spacecraft)
                all_slots += self._calculate_passes(
                    spacecraft, groundstation, window
                )

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

    def __unicode__(self):
        """Unicode string
        :return: Unicode string
        """
        return u'>>> pass: ' + str(self.start) + u', ' + str(self.end)
