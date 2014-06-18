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

from datetime import datetime, timedelta
from django.test import TestCase

from common.misc import localize_date_utc, get_utc_timestamp, get_altitude


class TestMisc(TestCase):

    def test_get_utc_timestamp(self):
        """
        Basic test for the generation of UTC timestamps.
        """
        test_datetime = localize_date_utc(datetime(year=1970, month=1, day=2))
        actual_stamp = get_utc_timestamp(test_datetime)
        expected_stamp = timedelta(days=1).days*24*3600 * 10**3
        self.assertEquals(expected_stamp, actual_stamp, 'Wrong timestamp!')

    def test_get_altitude(self):
        """
        Tests the usage of the Google Web Service for retrieving the altitude
        associated with the coordinates of a given point.
        """
        location_1 = (39.73915360, -104.98470340)
        expected_h_1 = 1608.637939453125
        expected_r_1 = 4.771975994110107
        (actual_h_1, actual_r_1) = get_altitude(location_1[0], location_1[1])
        self.assertEquals(
            expected_h_1, actual_h_1,
            'Altitudes differ, expected = ' + str(expected_h_1)
            + ', actual = ' + str(actual_h_1)
        )
        self.assertEquals(
            expected_r_1, actual_r_1,
            'Resolutions differ, expected = ' + str(expected_r_1)
            + ', actual = ' + str(actual_r_1)
        )