"""
   Copyright 2016 Ricardo Tubio-Pardavila

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
import mock

from django import test
from services.common import helpers as db_tools
from services.common import mocks as sn_mocks


class OperationalSlotsBugTest(test.TestCase):
    """
    Class with the UNIT tests for reproducing and fixing the bug that happens
    when filtering the pass slots to generate operational slots.
    """

    def setUp(self):

        self.__verbose_testing = False

        if not self.__verbose_testing:
            logging.getLogger('configuration').setLevel(level=logging.CRITICAL)
            logging.getLogger('scheduling').setLevel(level=logging.CRITICAL)
            logging.getLogger('simulation').setLevel(level=logging.CRITICAL)

    @mock.patch(
        'services.common.simulation.OrbitalSimulator',
        sn_mocks.mock__OrbitalSimulator
    )
    def test_bug_1(self):
        """INTR test: services.scheduling - operational slot generation
        """

        # 1) create vigo gs
        self.__gs_1_id = 'gs-vigo'
        self.__gs_1_ch_1_id = 'chan-cas-1'

        self.__band = db_tools.create_band()
        self.__user_profile = db_tools.create_user_profile()
        self.__gs = db_tools.create_gs(
            user_profile=self.__user_profile, identifier=self.__gs_1_id
        )

        # 2) serpens spacecraft
        self.__sc_1_id = 'sc-serpens'
        self.__sc_1_ch_1_id = 'xatco-fm-1'
        self.__sc_1_ch_1_f = 437500000

        self.__sc = db_tools.create_sc(
            user_profile=self.__user_profile, identifier=self.__sc_1_id
        )
