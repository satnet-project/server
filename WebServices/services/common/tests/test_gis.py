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

from django.test import TestCase

from services.common.gis import get_altitude, get_region


class TestGis(TestCase):

    def test_get_region(self):
        """
        Tests the usage of the Google Web Service for retrieving the altitude
        associated with the coordinates of a given point.
        """
        location_1 = (42.6000, -8.9333)
        expected_country = 'ES'
        expected_region = 'GA'
        (actual_country_l, actual_country_s, actual_region_l, actual_region_s)\
            = get_region(location_1[0], location_1[1])
        self.assertEquals(
            expected_country, actual_country_s,
            'Altitudes differ, expected = ' + str(expected_country)
            + ', actual = ' + str(actual_country_s)
        )
        self.assertEquals(
            expected_region, actual_region_s,
            'Resolutions differ, expected = ' + str(expected_region)
            + ', actual = ' + str(actual_region_s)
        )

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