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
    """UNIT tests
    Test methods for the GIS module.
    """

    def test_get_remote_user_location(self):
        """UNIT test: services.common.gis.get_remote_user_location
        Tests for the validation of how to get the location of a remote user
        """
        self.assertEquals(
            gis.get_remote_user_location(), (35.347099, -120.455299)
        )
        self.assertEquals(
            gis.get_remote_user_location('127.0.0.1'), (35.347099, -120.455299)
        )

    def test_get_region(self):
        """UNIT test: services.common.gis.get_region
        Tests the usage of the Google Web Service for retrieving the altitude
        associated with the coordinates of a given point.
        """
        location_1 = (42.6000, -8.9333)
        expected_country = 'ES'
        # expected_region = 'GA'
        result = gis.get_region(location_1[0], location_1[1])
        actual_country = result[gis.COUNTRY_SHORT_NAME]
        # actual_region = result[gis.REGION_SHORT_NAME]
        self.assertEqual(
            expected_country, actual_country,
            'Altitudes differ, expected = ' + str(expected_country) +
            ', actual = ' + str(actual_country)
        )
        # self.assertEqual(
        #     expected_region, actual_region,
        #     'Resolutions differ, expected = ' + str(expected_region) +
        #     ', actual = ' + str(actual_region)
        # )

    def test_get_altitude(self):
        """UNIT test: services.common.gis.get_altitude
        Tests the usage of the Google Web Service for retrieving the altitude
        associated with the coordinates of a given point.
        """
        loc_1 = (39.73915360, -104.98470340)
        expected_h_1 = 1608.637939453125
        expected_r_1 = 4.771975994110107
        (actual_h_1, actual_r_1) = gis.get_altitude(loc_1[0], loc_1[1])
        self.assertEqual(
            expected_h_1, actual_h_1,
            'Altitudes differ, expected = ' + str(expected_h_1) +
            ', actual = ' + str(actual_h_1)
        )
        self.assertEqual(
            expected_r_1, actual_r_1,
            'Resolutions differ, expected = ' + str(expected_r_1) +
            ', actual = ' + str(actual_r_1)
        )

    def test_get_altitude_bug_3(self):
        """UNIT test: BUG#3 (Kamchatka bug).
        This test validates the utilization of the GIS method for obtaining
        the altitude of a given location, for the case of the Kamchatka
        peninsula. This case triggers an error while invoking this method.
        Parameters for the invocation of this method that trigger the bug are
        the following:
            { latitude='56.559482', longitude='-199.687500' }
        """
        self.assertRaises(
            Exception, gis.get_altitude, '56.559482', '-199.687500'
        )

    def test_decimal_2_degrees(self):
        """UNIT test: services.common.gis.decimal_2_degrees
        Validates the method for converting from decimal degrees (float) to a
        DMS-formatted string.
        """
        test_array = [
            {  # Zeroland
                'input': (0, 0),
                'expected': ('0:0:0.00', '0:0:0.00')
            },
            {  # Zeroland
                'input': (0, -0),
                'expected': ('0:0:0.00', '0:0:0.00')
            },
            {  # Zeroland
                'input': (-0, 0),
                'expected': ('0:0:0.00', '0:0:0.00')
            },
            {  # Zeroland
                'input': (-0, -0),
                'expected': ('0:0:0.00', '0:0:0.00')
            },
            {  # Casa (Pobra)
                'input': (42.600, -8.933),
                'expected': ('42:36:0.00', '-8:55:58.80')
            },
            {  # Reichstag (Berlin)
                'input': (52.518623, 13.376198),
                'expected': ('52:31:7.04', '13:22:34.31')
            },
            {  # Capetown
                'input': (-33.918861, 18.423300),
                'expected': ('-33:55:7.90', '18:25:23.88')
            },
            {  # Buenos Aires
                'input': (-34.603722, -58.381592),
                'expected': ('-34:36:13.40', '-58:22:53.73')
            }
        ]

        for t in test_array:
            self.assertEqual(gis.latlng_2_degrees(t['input']), t['expected'])

    def test_get_latitude_direction(self):
        """UNIT test: services.common.gis.test_get_latitude_direction
        Tests the extraction of the direction from a latitude
        """
        self.assertRaises(ValueError, gis.get_latitude_direction, None)
        self.assertEquals(gis.get_latitude_direction(-180), 'S')
        self.assertEquals(gis.get_latitude_direction(180), 'N')
        self.assertEquals(gis.get_latitude_direction(0), '')

    def test_get_longitude_direction(self):
        """UNIT test: services.common.gis.test_get_latitude_direction
        Tests the extraction of the direction from a latitude
        """
        self.assertRaises(ValueError, gis.get_longitude_direction, None)
        self.assertEquals(gis.get_longitude_direction(-180), 'W')
        self.assertEquals(gis.get_longitude_direction(180), 'E')
        self.assertEquals(gis.get_longitude_direction(0), '')

    def test_latlng_2_degrees_latitude_direction(self):
        """UNIT test: services.common.gis.decimal_2_degrees (latitude/dir)
        Validates the method for converting from decimal degrees (float) to a
        DMS-formatted string.
        """
        test_array = [
            {  # Zeroland
                'input': (0, 0),
                'expected': ('0:0:0.00', '0:0:0.00')
            },
            {  # Zeroland
                'input': (0, -0),
                'expected': ('0:0:0.00', '0:0:0.00')
            },
            {  # Zeroland
                'input': (-0, 0),
                'expected': ('0:0:0.00', '0:0:0.00')
            },
            {  # Zeroland
                'input': (-0, -0),
                'expected': ('0:0:0.00', '0:0:0.00')
            },
            {  # Casa (Pobra)
                'input': (42.600, -8.933),
                'expected': ('42:36:0.00N', '-8:55:58.80W')
            },
            {  # Reichstag (Berlin)
                'input': (52.518623, 13.376198),
                'expected': ('52:31:7.04N', '13:22:34.31E')
            },
            {  # Capetown
                'input': (-33.918861, 18.423300),
                'expected': ('-33:55:7.90S', '18:25:23.88E')
            },
            {  # Buenos Aires
                'input': (-34.603722, -58.381592),
                'expected': ('-34:36:13.40S', '-58:22:53.73W')
            }
        ]

        for t in test_array:
            self.assertEqual(
                gis.latlng_2_degrees(t['input'], add_direction=True),
                t['expected']
            )
