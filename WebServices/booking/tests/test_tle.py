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

import ephem
from django.core.exceptions import ObjectDoesNotExist
from django.test import TestCase

import common.testing as db_tools
import configuration.signals as cfg_signals
from booking.models.tle import TwoLineElementsManager, TwoLineElement


class TestTle(TestCase):
    """
    Test for the TLE's class model.
    """

    def setUp(self):

        self.__verbose_testing = False

        self.__sc_1_id = 'fake-xatcobeo'
        self.__sc_1_tle_id = 'XATCOBEOXX'

        self.__sc_2_id = 'sc-xatcobeo'
        self.__sc_2_tle_id = 'XATCOBEO'

        self.__band = db_tools.create_band()
        db_tools.init_tles_database()
        self.__user_profile = db_tools.create_user_profile()

        if not self.__verbose_testing:
            logging.getLogger('booking').setLevel(level=logging.CRITICAL)

        cfg_signals.connect_segments_2_booking_tle()

    def test_load_tles(self):
        """
        Test for validating that the TLE's are read correctly from the remote
        source. This test uses the PyEphem library so that all the read TLE's
        are transformed into an object with this library. In case the TLE is
        not correct, an Exception is throXwn and the test is aborted.
        """
        if self.__verbose_testing:
            print '>>> test_load_tles'

        TwoLineElementsManager.load_tles()

        for tle_i in TwoLineElement.objects.all():
            ephem.readtle(
                str(tle_i.identifier),
                str(tle_i.first_line),
                str(tle_i.second_line)
            )

    def test_spacecraft_database_signaling(self):
        """
        This test is oriented to test the execution of the callbacks invoked
        by the creation of a new Spacecraft object in the database.
        """
        if self.__verbose_testing:
            print '>>> spacecraft_database_signaling'

        self.__sc_1 = db_tools.create_sc(
            user_profile=self.__user_profile,
            identifier=self.__sc_1_id,
            tle_id=self.__sc_1_tle_id
        )
        try:
            TwoLineElement.objects.get(identifier=self.__sc_1_tle_id)
            self.fail(
                'Object should NOT be found!, tle_id = ' + str(
                    self.__sc_1_tle_id
                )
            )
        except ObjectDoesNotExist:
            pass

        self.__sc_2 = db_tools.create_sc(
            user_profile=self.__user_profile,
            identifier=self.__sc_2_id,
            tle_id=self.__sc_2_tle_id
        )
        tle_o = None
        try:
            tle_o = TwoLineElement.objects.get(identifier=self.__sc_2_tle_id)
        except ObjectDoesNotExist:
            self.fail(
                'Object should have been found!, tle_id = ' + str(
                    self.__sc_2_tle_id
                )
            )
        self.assertNotEquals(
            tle_o.spacecraft, None,
            'No Spacecraft linked with this TLE!'
        )
        self.assertEquals(
            tle_o.spacecraft.identifier, self.__sc_2_id,
            'Wrong Spacecraft linked with this TLE! tle_o.sc.id = ' + str(
                tle_o.spacecraft.identifier
            ) + ', expected = ' + str(
                self.__sc_2_id
            )
        )

        db_tools.remove_sc(self.__sc_1_id)
        tle_o = None
        try:
            tle_o = TwoLineElement.objects.get(identifier=self.__sc_2_tle_id)
        except ObjectDoesNotExist:
            self.fail(
                'Object should have been found!, tle_id = ' + str(
                    self.__sc_2_tle_id
                )
            )
        self.assertNotEquals(
            tle_o.spacecraft.identifier,
            None,
            'No Spacecraft linked with this TLE!'
        )
        self.assertEquals(
            tle_o.spacecraft.identifier,
            self.__sc_2_id,
            'Wrong Spacecraft linked with this TLE! sc_id = ' + str(
                tle_o.spacecraft.identifier
            ) + ', tle_id = ' + str(tle_o.identifier)
        )

        db_tools.remove_sc(self.__sc_2_id)
        try:
            TwoLineElement.objects.get(identifier=self.__sc_1_tle_id)
            self.fail(
                'Object should NOT be found!, tle_id = ' + str(
                    self.__sc_1_tle_id
                )
            )
        except ObjectDoesNotExist:
            pass

    def test_update_slots(self):
        """
        Validates the whole process of slots update within the TLE database.
        """
        pass