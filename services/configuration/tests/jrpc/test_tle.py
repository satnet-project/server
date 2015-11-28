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

# noinspection PyPackageRequirements
import ephem
import logging
from django import test

from services.common import misc, helpers as db_tools
from services.configuration.models import celestrak
from services.configuration.jrpc.serializers import segments as \
    segment_serializer, tle as tle_serializer
from services.configuration.jrpc.views import tle as tle_jrpc


class JRPCTestTle(test.TestCase):
    """Testing class for the simulation services.
    This class tests the services related with the TLE objects.
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

    def test_get_celestrak_sections(self):
        """JRPC test: configuration.tle.celestrak.getSections
        """

        e_sections = [
            {'section': 'Weather & Earth Resources',
             'subsection': 'Weather'},
            {'section': 'Weather & Earth Resources',
             'subsection': 'NOAA'},
            {'section': 'Weather & Earth Resources',
             'subsection': 'GOES'},
            {'section': 'Weather & Earth Resources',
             'subsection': 'Earth Resources'},
            {'section': 'Weather & Earth Resources',
             'subsection': 'SARSAT'},
            {'section': 'Weather & Earth Resources',
             'subsection': 'Disaster Monitoring'},
            {'section': 'Weather & Earth Resources',
             'subsection': 'Tracking & Data Relay'},
            {'section': 'Weather & Earth Resources',
             'subsection': 'ARGOS'},
            {'section': 'Communications',
             'subsection': 'Geostationary'},
            {'section': 'Communications',
             'subsection': 'Intelsat'},
            {'section': 'Communications',
             'subsection': 'Gorizont'},
            {'section': 'Communications',
             'subsection': 'Raduga'},
            {'section': 'Communications',
             'subsection': 'Molniya'},
            {'section': 'Communications',
             'subsection': 'Iridium'},
            {'section': 'Communications',
             'subsection': 'Orbcomm'},
            {'section': 'Communications',
             'subsection': 'Globalstar'},
            {'section': 'Communications',
             'subsection': 'Amateur Radio'},
            {'section': 'Communications',
             'subsection': 'Experimental'},
            {'section': 'Communications',
             'subsection': 'Others'},
            {'section': 'Navigation', 'subsection': 'GPS Operational'},
            {'section': 'Navigation', 'subsection': 'Glonass Operational'},
            {'section': 'Navigation', 'subsection': 'Galileo'},
            {'section': 'Navigation', 'subsection': 'Beidou'},
            {'section': 'Navigation', 'subsection':
                'Satellite-based Augmentation System'},
            {'section': 'Navigation', 'subsection':
                'Navy Navigation Satellite System'},
            {'section': 'Navigation', 'subsection': 'Russian LEO Navigation'},
            {'section': 'Scientific', 'subsection': 'Space & Earth Science'},
            {'section': 'Scientific', 'subsection': 'Geodetic'},
            {'section': 'Scientific', 'subsection': 'Engineering'},
            {'section': 'Scientific', 'subsection': 'Education'},
            {'section': 'Miscellaneous', 'subsection': 'Military'},
            {'section': 'Miscellaneous', 'subsection': 'Radar Callibration'},
            {'section': 'Miscellaneous', 'subsection': 'CubeSats'},
            {'section': 'Miscellaneous', 'subsection': 'Other'}
        ]
        a_sections = tle_jrpc.get_celestrak_sections()

        self.assertEqual(a_sections, e_sections)

    def test_get_celestrak_resource(self):
        """JRPC test: configuration.tle.celestrak.getResource
        Tests the retrieval of the information contained in one of the
        celestrak resouces.
        """
        if self.__verbose_testing:
            print('>>> get_celestrak_resource')

        for s in list(celestrak.CelestrakDatabase.CELESTRAK_RESOURCES.keys()):

            tle_resource = tle_jrpc.get_celestrak_resource(s)
            if self.__verbose_testing:
                print('>>> resource = ' + misc.dict_2_string(tle_resource))

            for t in tle_resource['tle_list']:

                tle_id = t['spacecraft_tle_id']
                self.assertNotEqual(
                    len(str(tle_id)), 0, "Id for TLE cannot be empty"
                )
                ephem.readtle(
                    str(tle_id), str(t['tle_line_1']), str(t['tle_line_2'])
                )

    # noinspection PyBroadException
    def test_get_spacecraft_tle(self):
        """JRPC test: configuration.tle.celestrak.getTle
        """

        try:
            tle_jrpc.get_spacecraft_tle('non existant sc')
            self.fail(
                'SC does not exist, an exception should have been raised.'
            )
        except Exception:
            pass

        e_result = {
            segment_serializer.SC_ID_K: self.__sc_1_id,
            segment_serializer.SC_TLE_ID_K: self.__sc_1_tle_id,
        }
        a_result = tle_jrpc.get_spacecraft_tle(self.__sc_1_id)

        self.assertEqual(
            a_result[segment_serializer.SC_ID_K],
            e_result[segment_serializer.SC_ID_K],
            'Spacecraft identifiers do not match, a = ' + str(
                a_result[segment_serializer.SC_ID_K]
            ) + ', e = ' + str(e_result[segment_serializer.SC_ID_K])
        )

        self.assertEqual(
            a_result[segment_serializer.SC_TLE_ID_K],
            e_result[segment_serializer.SC_TLE_ID_K],
            'TLE identifiers do not match, a = ' + str(
                a_result[segment_serializer.SC_TLE_ID_K]
            ) + ', e = ' + str(e_result[segment_serializer.SC_TLE_ID_K])
        )

        self.assertEqual(
            len(a_result[tle_serializer.TleSerializer.TLE_LINE_1_K]),
            tle_serializer.TleSerializer.LEN_TLE_LINE_1,
            'Length of TLEs Line 1 does not match!'
        )

        self.assertEqual(
            len(a_result[tle_serializer.TleSerializer.TLE_LINE_2_K]),
            tle_serializer.TleSerializer.LEN_TLE_LINE_2,
            'Length of TLEs Line 2 does not match!'
        )
