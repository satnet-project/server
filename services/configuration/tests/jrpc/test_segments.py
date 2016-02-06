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

from django import test

from services.common import misc, helpers as db_tools
from services.configuration.jrpc.serializers import \
    segments as segment_serializaers
from services.configuration.jrpc.views.segments import groundstations as jrpc_gs
from services.configuration.jrpc.views.segments import spacecraft as jrpc_sc
from services.configuration.models import segments


class JRPCSegmentsTest(test.TestCase):

    def setUp(self):
        """Test setup
        This method populates the database with some information to be used
        only for this test.
        """
        self.__verbose_testing = False

        self.__gs_1_id = 'gs-castrelos'
        self.__gs_1_callsign = 'GS1GSGS'
        self.__gs_1_contact_elevation = 10.30
        self.__gs_1_longitude = -8.9330
        self.__gs_1_latitude = 42.6000
        self.__gs_1_configuration = (
            self.__gs_1_callsign,
            10.3,
            self.__gs_1_latitude,
            self.__gs_1_longitude
        )
        self.__gs_2_id = 'gs-calpoly'
        self.__gs_1_ch_1_id = 'fm-1'
        self.__gs_1_ch_2_id = 'afsk-2'

        self.__sc_1_id = 'sc-xatcobeo'
        self.__sc_1_callsign = 'BABA00'
        self.__sc_1_tle_id = str('HUMSAT-D')
        self.__sc_1_ch_1_id = 'xatcobeo-qpsk-1'
        self.__sc_1_ch_2_id = 'xatcobeo-gmsk-2'
        self.__sc_1_ch_1_f = 437000000
        self.__sc_1_configuration = (
            self.__sc_1_callsign,
            self.__sc_1_tle_id
        )

        self.__sc_2_id = 'sc-swisscube'
        self.__sc_2_tle_id = str('SWISSCUBE')

        self.__sc_3_id = 'sc-somp'
        self.__sc_3_tle_id = str('SOMP')

        self.__sc_4_id = 'sc-test'
        self.__sc_4_callsign = 'GOXX5'
        self.__sc_4_tle_id = 'GOES 4 [-]'

        self.__band = db_tools.create_band()
        self.__user_profile = db_tools.create_user_profile()
        self.__http_request = db_tools.create_request(
            user_profile=self.__user_profile
        )
        self.__gs_1 = db_tools.create_gs(
            user_profile=self.__user_profile,
            identifier=self.__gs_1_id,
            callsign=self.__gs_1_callsign,
            contact_elevation=self.__gs_1_contact_elevation,
            latitude=self.__gs_1_latitude,
            longitude=self.__gs_1_longitude,
        )
        self.__gs_1_ch_1 = db_tools.gs_add_channel(
            self.__gs_1, self.__band, self.__gs_1_ch_1_id,
        )
        self.__gs_2 = db_tools.create_gs(
            user_profile=self.__user_profile,
            identifier=self.__gs_2_id
        )

        self.__sc_1 = db_tools.create_sc(
            user_profile=self.__user_profile,
            identifier=self.__sc_1_id,
            callsign=self.__sc_1_callsign,
            tle_id=self.__sc_1_tle_id
        )
        self.__sc_1_ch_1 = db_tools.sc_add_channel(
            self.__sc_1, self.__sc_1_ch_1_f, self.__sc_1_ch_1_id,
        )
        self.__sc_2 = db_tools.create_sc(
            user_profile=self.__user_profile,
            identifier=self.__sc_2_id,
            tle_id=self.__sc_2_tle_id
        )

        if not self.__verbose_testing:
            logging.getLogger('configuration').setLevel(level=logging.CRITICAL)
            logging.getLogger('simulation').setLevel(level=logging.CRITICAL)
            logging.getLogger('common').setLevel(level=logging.CRITICAL)

    def test_gs_create(self):
        """JRPC test: configuration.gs.create (1)
        This test validates the creation of a new GroundStation through the
        JRPC interface.
        NOTE: test specifically created for issue #3 on GitHub server's
        repository. Parameters that triggered that bug:
        "params":["gs-kam","kam88xx","15.00","56.559482","-199.687500"]
        """
        if self.__verbose_testing:
            print('>>> TEST (test_gs_create)')

        gs_id = jrpc_gs.create(
            identifier='gs-kam',
            callsign='kam88xx',
            elevation='15.00',
            latitude='56.559482',
            longitude='-169.687500',
            request=self.__http_request
        )

        self.assertIsNotNone(gs_id, 'Wrong GS identifier')
        self.assertIsNotNone(
            segments.GroundStation.objects.get(identifier='gs-kam'),
            'GroundStation object has not been created'
        )

    # noinspection PyBroadException
    def test_gs_create_2(self):
        """JRPC test: configuration.gs.create (2)
        This test validates the creation of a new GroundStation through the
        JRPC interface.
        NOTE: test specifically create for issue (bug-2) manually reported. The
        paramters that triggered this bug were:
            "params":["afdasf","asdfafd","15.00","34.786739","-120.997925"]
        """
        if self.__verbose_testing:
            print('>>> TEST (test_gs_create_2)')

        try:
            jrpc_gs.create(
                identifier='afdasf',
                callsign='asdfafd',
                elevation='15.00',
                latitude='34.786739',
                longitude='-120.997925',
                request=self.__http_request
            )
            self.fail('Exception should have been thrown!')
        except Exception:
            pass

    def test_gs_list(self):
        """JRPC test: configuration.gs.list
        This test validates the list of configuration objects returned through
        the JRPC method.
        """
        if self.__verbose_testing:
            print('>>> TEST (test_gs_list)')
        self.assertListEqual(
            jrpc_gs.list_groundstations(request=self.__http_request), [
                self.__gs_1_id, self.__gs_2_id
            ]
        )

    def test_gs_list_mine(self):
        """JRPC test: configuration.gs.list.mine
        This test validates the list of GroundStation objects
        returned through the JRPC method.
        """
        if self.__verbose_testing:
            print('>>> TEST (test_sc_list_mine)')

        self.assertListEqual(
            jrpc_gs.list_groundstations_mine(request=self.__http_request), [
                self.__gs_1_id, self.__gs_2_id
            ]
        )

        user_profile_2 = db_tools.create_user_profile(
            username='fake222'
        )
        request_2 = db_tools.create_request(user_profile=user_profile_2)
        self.assertListEqual(
            jrpc_gs.list_groundstations_mine(request=request_2), []
        )

    def test_gs_list_others(self):
        """JRPC test: configuration.gs.list.others
        This test validates the list of GroundStation objects
        returned through the JRPC method.
        """
        if self.__verbose_testing:
            print('>>> TEST (test_sc_list_others)')

        self.assertListEqual(
            jrpc_gs.list_groundstations_others(request=self.__http_request), []
        )

        user_profile_2 = db_tools.create_user_profile(
            username='fake222'
        )
        request_2 = db_tools.create_request(user_profile=user_profile_2)
        self.assertListEqual(
            jrpc_gs.list_groundstations_others(request=request_2), [
                self.__gs_1_id, self.__gs_2_id
            ]
        )

    def test_sc_list(self):
        """JRPC test: configuration.sc.list
        This test validates the list of SpacecraftConfiguration objects
        returned through the JRPC method.
        """
        if self.__verbose_testing:
            print('>>> TEST (test_sc_list)')
        sc_list = jrpc_sc.list_spacecraft(request=self.__http_request)
        self.assertCountEqual(
            sc_list, [
                'sc-canx-2', self.__sc_1_id, self.__sc_2_id
            ]
        )

    def test_sc_list_mine(self):
        """JRPC test: configuration.sc.list.mine
        This test validates the list of SpacecraftConfiguration objects
        returned through the JRPC method.
        """
        if self.__verbose_testing:
            print('>>> TEST (test_sc_list_mine)')

        self.assertEquals(
            jrpc_sc.list_spacecraft_mine(request=self.__http_request), [
                self.__sc_1_id, self.__sc_2_id
            ]
        )

        user_profile_2 = db_tools.create_user_profile(
            username='fake222'
        )
        request_2 = db_tools.create_request(user_profile=user_profile_2)
        self.assertListEqual(
            jrpc_sc.list_spacecraft_mine(request=request_2), []
        )

    def test_sc_list_others(self):
        """JRPC test: configuration.sc.list.others
        This test validates the list of SpacecraftConfiguration objects
        returned through the JRPC method.
        """
        if self.__verbose_testing:
            print('>>> TEST (test_sc_list_others)')

        self.assertEquals(
            jrpc_sc.list_spacecraft_others(request=self.__http_request), [
                'sc-canx-2'
            ]
        )

        user_profile_2 = db_tools.create_user_profile(
            username='fake222'
        )
        request_2 = db_tools.create_request(user_profile=user_profile_2)
        self.assertListEqual(
            jrpc_sc.list_spacecraft_others(request=request_2), [
                'sc-canx-2', self.__sc_1_id, self.__sc_2_id
            ]
        )

    def test_sc_create(self):
        """JRPC test: configuration.sc.create (1)
        This test validates the addition of a new Spacecraft through the
        correspondent JRPC method.
        """
        if self.__verbose_testing:
            print('>>> TEST (test_sc_add)')

        result = jrpc_sc.create(
            self.__sc_3_id, 'xxxcs', self.__sc_3_tle_id,
            request=self.__http_request
        )

        self.assertEqual(
            result['spacecraft_id'], self.__sc_3_id,
            'Error creating the SC, expected id = ' + str(self.__sc_3_id) +
            ', actual id = ' + str(result['spacecraft_id'])
        )

        self.assertNotEqual(
            segments.Spacecraft.objects.get(identifier=self.__sc_3_id), None,
            'SC id = <' + str(self.__sc_3_id) + '>, should have been found'
        )

    def test_sc_create_2(self):
        """JRPC test: configuration.sc.create (2)
        Test for validating the creation of a given spacecraft. Although the
        creation of the spacecraft calls directly to the create helper method
        from the Django framework, some problems have appeared depending on
        the identifier of the associated TLE. Therefore, the main purpose of
        this test is to validate the functioning of the system with TLE's whose
        identifiers contain symbols, blanks and other types of non common
        characters.
        """
        self.__verbose_testing = False
        if self.__verbose_testing:
            print('>>> TEST (test_sc_create_2):')

        self.assertEquals(
            jrpc_sc.create(
                self.__sc_4_id, self.__sc_4_callsign, self.__sc_4_tle_id,
                request=self.__http_request
            ), {
                'spacecraft_id': self.__sc_4_id
            },
            'Spacecraft should have been created'
        )

    def test_gs_get_configuration(self):
        """JRPC test: configuration.gs.getConfiguration
        This test validates the returned configuration by the proper JRPC
        method.
        """
        if self.__verbose_testing:
            print('>>> TEST (test_gs_get_configuration):')

        cfg = segment_serializaers.deserialize_gs_configuration(
            jrpc_gs.get_configuration(self.__gs_1_id)
        )

        if self.__verbose_testing:
            misc.print_dictionary(cfg)
            misc.print_dictionary(self.__gs_1_configuration)

        self.assertEqual(cfg, self.__gs_1_configuration)

    def test_gs_set_configuration(self):
        """JRPC test: configuration.gs.setConfiguration
        This test validates how to set the configuration with the JRPC method,
        by comparing the one sent with the one obtained through the
        get_configuration JRPC method of the same interface.
        """
        if self.__verbose_testing:
            print('>>> TEST (test_gs_get_configuration):')

        cfg = segment_serializaers.serialize_gs_configuration(
            segments.GroundStation.objects.get(identifier=self.__gs_1_id)
        )

        cfg[segment_serializaers.GS_CALLSIGN_K] = 'CHANGED'
        cfg[segment_serializaers.GS_ELEVATION_K] = 0.00
        cfg[segment_serializaers.GS_LATLON_K] = [
            39.73915360, -104.98470340
        ]
        cfg[segment_serializaers.GS_ALTITUDE_K] = 1608.63793945312

        self.assertEqual(
            jrpc_gs.set_configuration(self.__gs_1_id, cfg),
            self.__gs_1_id,
            'The <set_configuration> JPRC method should have returned <True>'
        )
        actual_cfg = jrpc_gs.get_configuration(self.__gs_1_id)
        self.assertEqual(actual_cfg, cfg)

    def test_sc_get_configuration(self):
        """JRPC test: configuration.sc.getConfiguration
        This test validates the returned configuration by the proper JRPC
        method.
        """
        if self.__verbose_testing:
            print('>>> TEST (test_sc_get_configuration):')
        cfg = segment_serializaers.deserialize_sc_configuration(
            jrpc_sc.get_configuration(self.__sc_1_id)
        )
        self.assertEqual(
            cfg, self.__sc_1_configuration, 'Wrong configuration returned'
        )

    def test_sc_set_configuration(self):
        """JRPC test: configuration.gs.setConfiguration
        This test validates how to set the configuration with the JRPC method,
        by comparing the one sent with the one obtained through the
        get_configuration JRPC method of the same interface.
        """
        if self.__verbose_testing:
            print('>>> TEST (test_sc_get_configuration):')
        cfg = segment_serializaers.serialize_sc_configuration(
            segments.Spacecraft.objects.get(identifier=self.__sc_1_id)
        )
        old_callsign = cfg[segment_serializaers.SC_CALLSIGN_K]
        old_tle_id = cfg[segment_serializaers.SC_TLE_ID_K]
        cfg[segment_serializaers.SC_CALLSIGN_K] = 'CHANGED'
        cfg[segment_serializaers.SC_TLE_ID_K] = 'HUMSAT-D'
        self.assertEqual(
            jrpc_sc.set_configuration(self.__sc_1_id, cfg),
            self.__sc_1_id,
            'The <set_configuration> JPRC method should have returned <True>'
        )
        actual_cfg = jrpc_sc.get_configuration(self.__sc_1_id)
        self.assertEqual(
            actual_cfg, cfg,
            'Configurations differ' + ', e = ' + str(cfg) + ', a = ' + str(
                actual_cfg
            )
        )
        cfg[segment_serializaers.SC_CALLSIGN_K] = old_callsign
        cfg[segment_serializaers.SC_TLE_ID_K] = old_tle_id
        self.assertEqual(
            jrpc_sc.set_configuration(self.__sc_1_id, cfg),
            self.__sc_1_id,
            'The <set_configuration> JPRC method should have returned <True>'
        )
        actual_cfg = jrpc_sc.get_configuration(self.__sc_1_id)
        self.assertEqual(
            actual_cfg, cfg,
            'Configurations differ' + ', e = ' + str(cfg) + ', a = ' + str(
                actual_cfg
            )
        )
