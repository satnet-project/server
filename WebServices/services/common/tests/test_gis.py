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

from services.common import gis


class TestGis(TestCase):

    def test_get_region(self):
        """
        Tests the usage of the Google Web Service for retrieving the altitude
        associated with the coordinates of a given point.
        """
        location_1 = (42.6000, -8.9333)
        expected_country = 'ES'
        expected_region = 'GA'
        result = gis.get_region(location_1[0], location_1[1])
        actual_country = result[gis.COUNTRY_SHORT_NAME]
        actual_region = result[gis.REGION_SHORT_NAME]
        self.assertEquals(
            expected_country, actual_country,
            'Altitudes differ, expected = ' + str(expected_country)
            + ', actual = ' + str(actual_country)
        )
        self.assertEquals(
            expected_region, actual_region,
            'Resolutions differ, expected = ' + str(expected_region)
            + ', actual = ' + str(actual_region)
        )

    def test_get_altitude(self):
        """
        Tests the usage of the Google Web Service for retrieving the altitude
        associated with the coordinates of a given point.
        """
        location_1 = (39.73915360, -104.98470340)
        expected_h_1 = 1608.637939453125
        expected_r_1 = 4.771975994110107
        (actual_h_1, actual_r_1) = gis.get_altitude(
            location_1[0], location_1[1]
        )
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

    def test_get_altitude_bug_3(self):
        """UNIT test for BUG#3 (Kamchatka bug).
        This test validates the utilization of the GIS method for obtaining
        the altitude of a given location, for the case of the Kamchatka
        peninsula. This case triggers an error while invoking this method.
        Parameters for the invocation of this method that trigger the bug are
        the following:
            { latitude='56.559482', longitude='-199.687500' }
        """
        location = ('56.559482', '-199.687500')
        print '>>> location = ' + str(location)
        (actual_h, actual_r) = gis.get_altitude(
            location[0], location[1]
        )
        print 'results: h = ' + str(actual_h) + ', r = ' + str(actual_r)

    def test_dms2dec(self):
        """DMS2Decimal test.
        Test to validate the method that transforms a DMS coordinate into a
        decimal value.
        """
        pobra_dms = '42:35:15'
        e_pobra_dec = 42.0 + 35.0 / 60 + 15.0 / 3600
        a_pobra_dec = gis.degrees_2_decimal(pobra_dms)

        self.assertEquals(
            e_pobra_dec, a_pobra_dec, 'Decimal coordinates differ, e = ' +
            str(e_pobra_dec) + ', a = ' + str(a_pobra_dec)
        )