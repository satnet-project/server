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

import datetime
import logging

from django import test
from services.common import mocks as sn_mocks


class MocksTest(test.TestCase):
    """
    Class with the UNIT tests for validating the mocks.
    """

    def setUp(self):

        self.__verbose_testing = False

        if not self.__verbose_testing:
            logging.getLogger('configuration').setLevel(level=logging.CRITICAL)
            logging.getLogger('scheduling').setLevel(level=logging.CRITICAL)
            logging.getLogger('simulation').setLevel(level=logging.CRITICAL)

    def test_mock__calculate_pass_slot(self):
        """UNIT Test: services.common.mocks - mock__calculate_pass_slot
        """

        p = datetime.datetime.now()
        start = p + datetime.timedelta(hours=1)
        end = p + datetime.timedelta(hours=2)
        x_0 = p + datetime.timedelta(hours=1, seconds=1800)
        x_1 = p + datetime.timedelta(hours=1, seconds=1860)
        x = [(x_0, x_1)]

        z = sn_mocks.mock__OrbitalSimulator().calculate_pass_slot(start, end)
        self.assertEquals(x, z)
