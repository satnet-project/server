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

from django import test
import logging
from services.common import misc
from services.common.testing import helpers as db_tools
from services.simulation.jrpc.views import simulation as jrpc_sim


class JRPCSimulationTest(test.TestCase):
    """Test class (JRPC).
    This class tests the services related with the Simulation objects.
    """

    def setUp(self):
        """
        This method populates the database with some information to be used
        only for this test.
        """
        self.__verbose_testing = False

        if not self.__verbose_testing:
            logging.getLogger('common').setLevel(level=logging.CRITICAL)
            logging.getLogger('configuration').setLevel(level=logging.CRITICAL)
            logging.getLogger('scheduling').setLevel(level=logging.CRITICAL)
            logging.getLogger('simulation').setLevel(level=logging.CRITICAL)

        self.__user_profile = db_tools.create_user_profile()
        self.__sc_1_id = 'humd-sc'
        self.__sc_1_tle_id = 'HUMSAT-D'
        self.__sc_1 = db_tools.create_sc(
            user_profile=self.__user_profile,
            identifier=self.__sc_1_id,
            tle_id=self.__sc_1_tle_id,
        )

    def test_get_groundtrack(self):
        """UNIT test (JRPC Method).
        Tests the generation of the GroundTracks for registered spacecraft.
        """
        # TODO Improve the verificaton method (right now is by INSPECTION).
        gt = jrpc_sim.get_groundtrack(self.__sc_1_id)
        if self.__verbose_testing:
            misc.print_list(gt)
            print 'gt.length = ' + str(len(gt))