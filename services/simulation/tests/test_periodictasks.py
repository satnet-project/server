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

import logging
from django import test
from services.common.testing import helpers as db_tools
from services.common import simulation as simulator
from services.configuration.models import segments as segment_models
from services.simulation.models import groundtracks as groundtrack_models
from services.simulation.models import passes as pass_models


class PeriodicSimulationTest(test.TestCase):
    """UNIT tests
    Tests for the validation of the periodic simulations.
    """

    def setUp(self):
        """Test setup.
        This method populates the database with some information to be used
        only for this test.
        """
        self.__verbose_testing = False

        if not self.__verbose_testing:
            logging.getLogger('configuration').setLevel(level=logging.CRITICAL)
            logging.getLogger('simulation').setLevel(level=logging.CRITICAL)

    def test_simulation_error(self):
        """Error test
        Validates the fail mode for the simulator.
        """
        sim = simulator.OrbitalSimulator()
        sim.set_debug(fail=True)
        sc = segment_models.Spacecraft.objects.get(identifier='sc-canx-2')
        try:
            sim.calculate_groundtrack(sc.tle)
            self.fail('Should have thrown an exception')
        except Exception:
            pass

    def test_propagate_groundtracks(self):
        """Periodic task test
        Test that validates the periodical propagation of the groundtracks. It
        uses the spacecraft created when the database was initialized some
        time ago at the beginning of the test.
        """
        sc = segment_models.Spacecraft.objects.get(identifier='sc-canx-2')
        gt_i = groundtrack_models.GroundTrack.objects.get(spacecraft=sc)

        self.assertNotEqual(
            len(gt_i.timestamp), 0, 'Initial GroundTrack should not be empty'
        )

        groundtrack_models.GroundTrack.objects.propagate()
        gt_f = groundtrack_models.GroundTrack.objects.get(spacecraft=sc)

        self.assertNotEqual(
            len(gt_f.timestamp), 0, 'Final GroundTrack should not be empty'
        )

        self.assertNotEqual(
            len(gt_i.timestamp), len(gt_f.timestamp),
            'Final and initial GroundTracks should have different lengths'
        )

    def test_propagate_passes(self):
        """Periodict task test
        Test that validates the periodical propagation of the pass slots.
        """
        pass_models.PassSlots.objects.propagate()

        self.assertEqual(
            len(pass_models.PassSlots.objects.all()), 0, 'No pass slots'
        )

        db_tools.create_gs()
        initial_p_slots = len(pass_models.PassSlots.objects.all())
        self.assertNotEqual(
            initial_p_slots, 0, 'There should be some pass slots available'
        )

        pass_models.PassSlots.objects.propagate()
        propagated_p_slots = len(pass_models.PassSlots.objects.all())

        self.assertNotEqual(
            propagated_p_slots, initial_p_slots,
            'Propagation should have added more pass slots'
        )