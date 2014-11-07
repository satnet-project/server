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

from django.core.exceptions import ObjectDoesNotExist
from django.test import TestCase
import logging
import ephem
from services.common.testing import helpers as db_tools
from services.simulation.models import tle


class TestTle(TestCase):
    """Unit test.
    Test for the TLE's class model.
    """

    def setUp(self):

        self.__verbose_testing = False

        self.__sc_1_id = 'fake-xatcobeo'
        self.__sc_1_tle_id = 'XATCOBEOXX'

        self.__sc_2_id = 'sc-xatcobeo'
        self.__sc_2_tle_id = 'HUMSAT-D'

        self.__band = db_tools.create_band()
        # (makes no sense) db_tools.init_tles_database()
        self.__user_profile = db_tools.create_user_profile()

        if not self.__verbose_testing:
            logging.getLogger('scheduling').setLevel(level=logging.CRITICAL)

    def test_load_tles(self):
        """
        Test for validating that the TLE's are read correctly from the remote
        source. This test uses the PyEphem library so that all the read TLE's
        are transformed into an object with this library. In case the TLE is
        not correct, an Exception is throXwn and the test is aborted.
        """
        if self.__verbose_testing:
            print '>>> test_load_tles'

        tle.TwoLineElementsManager.load_tles()

        for tle_i in tle.TwoLineElement.objects.all():
            ephem.readtle(
                str(tle_i.identifier),
                str(tle_i.first_line),
                str(tle_i.second_line)
            )

    def test_load_celestrak(self):
        """
        Test for validating that all the TLE's from celestrak.com are loaded
        correctly.
        """
        tle.TwoLineElementsManager.load_celestrak()

        for tle_i in tle.TwoLineElement.objects.all():
            ephem.readtle(
                str(tle_i.identifier),
                str(tle_i.first_line),
                str(tle_i.second_line)
            )

    def test_spacecraft_database(self):
        """
        Tests the usage of the database by an external user.
        """
        if self.__verbose_testing:
            print '>>> spacecraft_database'

        tle.TwoLineElementsManager.load_tles()

        try:
            tle.TwoLineElement.objects.get(identifier=self.__sc_1_tle_id)
            self.fail(
                'Object should NOT be found!, tle_id = ' + str(
                    self.__sc_1_tle_id
                )
            )
        except ObjectDoesNotExist:
            pass

        tle_o = None
        try:
            tle_o = tle.TwoLineElement.objects.get(
                identifier=self.__sc_2_tle_id
            )
        except ObjectDoesNotExist:
            self.fail(
                'Object should have been found!, tle_id = ' + str(
                    self.__sc_2_tle_id
                )
            )