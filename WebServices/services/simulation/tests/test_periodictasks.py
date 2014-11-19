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
from services.configuration.models import segments as segment_models
from services.simulation.models import simulation as simulation_models


class PeriodicSimulationTest(test.TestCase):

    def setUp(self):
        """Test setup.
        This method populates the database with some information to be used
        only for this test.
        """
        self.__verbose_testing = False

        if not self.__verbose_testing:
            logging.getLogger('configuration').setLevel(level=logging.CRITICAL)
            logging.getLogger('simulation').setLevel(level=logging.CRITICAL)

    def test_propagate_groundtracks(self):
        """Periodic task test.
        Test that validates the periodical propagation of the groundtracks. It
        uses the spacecraft created when the database was initialized some
        time ago at the beginning of the test.
        """
        sc = segment_models.Spacecraft.objects.get(identifier='sc-canx-2')
        gt_i = simulation_models.GroundTrack.objects.get(spacecraft=sc)

        self.assertNotEquals(
            len(gt_i.timestamp), 0, 'Initial GroundTrack should not be empty'
        )

        simulation_models.GroundTrack.objects.propagate_groundtracks()
        gt_f = simulation_models.GroundTrack.objects.get(spacecraft=sc)

        self.assertNotEquals(
            len(gt_f.timestamp), 0, 'Final GroundTrack should not be empty'
        )

        self.assertNotEquals(
            len(gt_i.timestamp), len(gt_f.timestamp),
            'Final and initial GroundTracks should have different lengths'
        )