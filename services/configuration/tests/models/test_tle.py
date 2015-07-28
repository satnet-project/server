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
from services.configuration.models import tle

__author__ = 'rtubiopa@calpoly.edu'

from django.core.exceptions import ObjectDoesNotExist
from django.test import TestCase
import logging
# noinspection PyPackageRequirements
import ephem
from services.common.testing import helpers as db_tools


class TestTle(TestCase):
    """Unit test.
    Test for the TLE's class model.
    """

    def setUp(self):

        super(TestTle, self).setUp()

        self.__verbose_testing = False
        self.__sc_1_id = 'sc-humsat'
        self.__sc_1_tle_id = 'HUMSAT-D'
        self.__user_profile = None

        self.__sc_2_id = 'fake-sat'
        self.__sc_2_tle_id = 'XXX99X9X'

        self.__band = db_tools.create_band()
        self.__user_profile = db_tools.create_user_profile()

        if not self.__verbose_testing:
            logging.getLogger('simulation').setLevel(level=logging.CRITICAL)

    def test_load_tles(self):
        """services.configuration: TLE initialization
        Test for validating that the TLE's are read correctly from the remote
        source. This test uses the PyEphem library so that all the read TLE's
        are transformed into an object with this library. In case the TLE is
        not correct, an Exception is throXwn and the test is aborted.
        """
        if self.__verbose_testing:
            print('>>> test_load_tles')

        tle.TwoLineElementsManager.load_tles()

        for tle_i in tle.TwoLineElement.objects.all():
            ephem.readtle(
                str(tle_i.identifier),
                str(tle_i.first_line),
                str(tle_i.second_line)
            )

    def _load_celestrak(self):
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
        """services.configuration: spacecraft database creation
        Tests the usage of the database by an external user.
        """
        if self.__verbose_testing:
            print('>>> spacecraft_database')

        tle.TwoLineElementsManager.load_tles()

        try:
            tle.TwoLineElement.objects.get(identifier=self.__sc_2_tle_id)
            self.fail(
                'Object should have NOT been found!, tle_id = ' + str(
                    self.__sc_2_tle_id
                )
            )
        except ObjectDoesNotExist:
            pass

        try:
            tle.TwoLineElement.objects.get(identifier=self.__sc_1_tle_id)
        except ObjectDoesNotExist:
            self.fail(
                'Object should have been found!, tle_id = ' + str(
                    self.__sc_1_tle_id
                )
            )
