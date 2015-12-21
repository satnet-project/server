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

from datetime import timedelta as py_timedelta
from django import test

from services.common import misc as sn_misc
from services.common import simulation as simulator
from services.common import helpers as db_tools
from services.configuration.models import segments as segment_models
from services.simulation.models import groundtracks as groundtrack_models
from services.simulation.models import passes as pass_models
from services.simulation import periodictasks as simulation_tasks


class PeriodicSimulationTest(test.TestCase):
    """UNIT tests
    Tests for the validation of the periodic simulations.
    """

    def setUp(self):
        """Test setup
        This method populates the database with some information to be used
        only for this test.
        """
        self.__verbose_testing = False

        if not self.__verbose_testing:
            logging.getLogger('configuration').setLevel(level=logging.CRITICAL)
            logging.getLogger('simulation').setLevel(level=logging.CRITICAL)

        self.__user = db_tools.create_user_profile()
        self.__request_1 = db_tools.create_request(user_profile=self.__user)

        self.__gs_1_id = 'gs-uvigo'
        self.__gs_1 = db_tools.create_gs(
            user_profile=self.__user, identifier=self.__gs_1_id
        )

        self.__sc_1_id = 'xatcobeo-sc'
        self.__sc_1_tle_id = 'CANX-2'
        self.__sc_1 = db_tools.create_sc(
            user_profile=self.__user,
            identifier=self.__sc_1_id, tle_id=self.__sc_1_tle_id,
        )

    def test_simulation_error(self):
        """UNIT test: services.common.simulation - simulation ERROR test
        Validates the fail mode for the simulator.
        """
        sim = simulator.OrbitalSimulator()
        sim.set_debug(fail=True)
        sc = segment_models.Spacecraft.objects.get(identifier='sc-canx-2')

        # noinspection PyBroadException
        try:
            sim.calculate_groundtrack(sc.tle)
            self.fail('Should have thrown an exception')
        except Exception:
            pass

    def test_propagate_groundtracks(self):
        """UNIT test: services.simulation.periodictasks.propagate()
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

    def test_passes_clean(self):
        """UNIT test: services.simulation.models = passes CLEAN UP
        """

        pass_models.PassSlots.objects.propagate()
        sc_passes_n_1 = pass_models.PassSlots.objects.filter(
            spacecraft=self.__sc_1
        ).count()

        simulation_tasks.clean_passes()
        sc_passes_n_2 = pass_models.PassSlots.objects.filter(
            spacecraft=self.__sc_1
        ).count()

        self.assertEquals(sc_passes_n_1, sc_passes_n_2)

        interval_2 = (
            sn_misc.get_next_midnight() + py_timedelta(days=5),
            sn_misc.get_next_midnight() + py_timedelta(days=6)
        )
        pass_models.PassSlots.objects.propagate(interval=interval_2)
        sc_passes_n_3 = pass_models.PassSlots.objects.filter(
            spacecraft=self.__sc_1
        ).count()
        self.assertGreater(sc_passes_n_3, sc_passes_n_2)

        simulation_tasks.clean_passes(
            threshold=sn_misc.get_next_midnight() + py_timedelta(days=10)
        )
        sc_passes_n_4 = pass_models.PassSlots.objects.filter(
            spacecraft=self.__sc_1
        ).count()
        self.assertEquals(sc_passes_n_4, 0)

    def test_groundtracks_clean(self):
        """UNIT test: services.simulation.models = groundtracks CLEAN UP
        """

        groundtrack_models.GroundTrack.objects.propagate()
        sc_gts_n_1 = len(
            groundtrack_models.GroundTrack.objects.get(
                spacecraft=self.__sc_1
            ).timestamp
        )

        simulation_tasks.clean_passes()
        sc_gts_n_2 = len(
            groundtrack_models.GroundTrack.objects.get(
                spacecraft=self.__sc_1
            ).timestamp
        )

        self.assertEquals(sc_gts_n_1, sc_gts_n_2)

        interval_2 = (
            sn_misc.get_next_midnight() + py_timedelta(days=5),
            sn_misc.get_next_midnight() + py_timedelta(days=6)
        )
        groundtrack_models.GroundTrack.objects.propagate(interval=interval_2)
        sc_gts_n_3 = len(
            groundtrack_models.GroundTrack.objects.get(
                spacecraft=self.__sc_1
            ).timestamp
        )
        self.assertGreater(sc_gts_n_3, sc_gts_n_2)

        simulation_tasks.clean_groundtracks(
            threshold=sn_misc.get_next_midnight() + py_timedelta(days=10)
        )
        sc_gts_n_4 = len(
            groundtrack_models.GroundTrack.objects.get(
                spacecraft=self.__sc_1
            ).timestamp
        )
        self.assertEquals(sc_gts_n_4, 0)
