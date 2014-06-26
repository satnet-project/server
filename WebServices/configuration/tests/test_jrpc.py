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

from datadiff import diff
from datetime import time, timedelta
import logging

from django.test import TestCase

from common import misc, testing as db_tools
from configuration.jrpc import groundstations as jrpc_gs,\
    spacecraft as jrpc_sc, rules as jrpc_rules, serialization as jrpc_serial
from configuration.models.rules import AvailabilityRule
from configuration.models.segments import GroundStation, Spacecraft


class JRPCRulesTest(TestCase):

    def setUp(self):
        """
        This method populates the database with some information to be used
        only for this test.
        """
        self.__verbose_testing = False

        if not self.__verbose_testing:
            logging.getLogger('configuration').setLevel(level=logging.CRITICAL)

        self.__gs_1_id = 'gs-castrelos'
        self.__gs_1_callsign = 'GS1GSGS'
        self.__gs_1_contact_elevation = 10.30
        self.__gs_1_longitude = 25.0
        self.__gs_1_latitude = 40.0
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
        self.__sc_1_tle_id = 'XaTcobeo'
        self.__sc_1_ch_1_id = 'xatcobeo-qpsk-1'
        self.__sc_1_ch_2_id = 'xatcobeo-gmsk-2'
        self.__sc_1_ch_1_f = 437000000
        self.__sc_1_configuration = (
            self.__sc_1_callsign,
            self.__sc_1_tle_id
        )

        self.__sc_2_id = 'sc-humsat'

        db_tools.init_available()
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
            user_profile=self.__user_profile, identifier=self.__sc_2_id,
        )

    def test_gs_list(self):
        """
        This test validates the list of configuration objects returned through
        the JRPC method.
        """
        if self.__verbose_testing:
            print '>>> TEST (test_gs_list)'
        gs_list = jrpc_gs.list_groundstations(request=self.__http_request)
        self.assertItemsEqual(
            gs_list, [self.__gs_1_id, self.__gs_2_id], 'Wrong GS identifiers'
        )

    def test_sc_list(self):
        """
        This test validates the list of SpacecraftConfiguration objects
        returned through the JRPC method.
        """
        if self.__verbose_testing:
            print '>>> TEST (test_sc_list)'
        sc_list = jrpc_sc.list_spacecraft(request=self.__http_request)
        self.assertItemsEqual(
            sc_list, [self.__sc_1_id, self.__sc_2_id], 'Wrong SC identifiers'
        )

    def test_gs_list_channels(self):
        """
        This test validates the list of channels returned throught the JRPC
        method.
        """
        if self.__verbose_testing:
            print '>>> TEST (test_gs_channels)'
        ch_list = jrpc_gs.list_channels(self.__gs_1_id)
        self.assertItemsEqual(
            ch_list[jrpc_serial.CHANNEL_LIST_K], [self.__gs_1_ch_1_id],
            'Wrong channel identifiers, actual = ' + str(ch_list)
        )

    def test_sc_list_channels(self):
        """
        This test validates the list of channels returned throught the JRPC
        method.
        """
        if self.__verbose_testing:
            print '>>> TEST (test_sc_channels)'
        ch_list = jrpc_sc.list_channels(self.__sc_1_id)
        self.assertItemsEqual(
            ch_list[jrpc_serial.CHANNEL_LIST_K], [self.__sc_1_ch_1_id],
            'Wrong channel identifiers, actual = ' + str(ch_list)
        )

    def test_gs_get_configuration(self):
        """
        This test validates the returned configuration by the proper JRPC
        method.
        """
        if self.__verbose_testing:
            print '>>> TEST (test_gs_get_configuration):'
        cfg = jrpc_serial.deserialize_gs_configuration(
            jrpc_gs.get_configuration(self.__gs_1_id)
        )
        if self.__verbose_testing:
            misc.print_dictionary(cfg)
            misc.print_dictionary(self.__gs_1_configuration)
        self.assertEquals(
            cfg, self.__gs_1_configuration,
            'Wrong configuration returned, diff = \n'
            + str(diff(cfg, self.__gs_1_configuration))
        )

    def test_gs_set_configuration(self):
        """
        This test validates how to set the configuration with the JRPC method,
        by comparing the one sent with the one obtained through the
        get_configuration JRPC method of the same interface.
        """
        if self.__verbose_testing:
            print '>>> TEST (test_gs_get_configuration):'

        cfg = jrpc_serial.serialize_gs_configuration(
            GroundStation.objects.get(identifier=self.__gs_1_id)
        )

        cfg[jrpc_serial.GS_CALLSIGN_K] = 'CHANGED'
        cfg[jrpc_serial.GS_ELEVATION_K] = 0.00
        cfg[jrpc_serial.GS_LATLON_K] = [
            39.73915360, -104.98470340
        ]
        cfg[jrpc_serial.GS_ALTITUDE_K] = 1608.63793945312

        self.assertEquals(
            jrpc_gs.set_configuration(self.__gs_1_id, cfg),
            True,
            'The <set_configuration> JPRC method should have returned <True>'
        )
        actual_cfg = jrpc_gs.get_configuration(self.__gs_1_id)
        self.assertEquals(
            actual_cfg, cfg,
            'Wrong configuration returned, diff = \n'
            + str(diff(actual_cfg, cfg))
        )

    def test_sc_get_configuration(self):
        """
        This test validates the returned configuration by the proper JRPC
        method.
        """
        if self.__verbose_testing:
            print '>>> TEST (test_sc_get_configuration):'
        cfg = jrpc_serial.deserialize_sc_configuration(
            jrpc_sc.get_configuration(self.__sc_1_id)
        )
        self.assertEquals(
            cfg, self.__sc_1_configuration, 'Wrong configuration returned'
        )

    def test_sc_set_configuration(self):
        """
        This test validates how to set the configuration with the JRPC method,
        by comparing the one sent with the one obtained through the
        get_configuration JRPC method of the same interface.
        """
        if self.__verbose_testing:
            print '>>> TEST (test_sc_get_configuration):'
        cfg = jrpc_serial.serialize_sc_configuration(
            Spacecraft.objects.get(identifier=self.__sc_1_id)
        )
        old_callsign = cfg[jrpc_serial.SC_CALLSIGN_K]
        old_tle_id = cfg[jrpc_serial.SC_TLE_ID_K]
        cfg[jrpc_serial.SC_CALLSIGN_K] = 'CHANGED'
        cfg[jrpc_serial.SC_TLE_ID_K] = 'BLUR'
        self.assertEquals(
            jrpc_sc.set_configuration(self.__sc_1_id, cfg),
            True,
            'The <set_configuration> JPRC method should have returned <True>'
        )
        actual_cfg = jrpc_sc.get_configuration(self.__sc_1_id)
        self.assertEquals(
            actual_cfg, cfg, 'Configurations differ'
            + ', e = ' + str(cfg)
            + ', a = ' + str(actual_cfg)
        )
        cfg[jrpc_serial.SC_CALLSIGN_K] = old_callsign
        cfg[jrpc_serial.SC_TLE_ID_K] = old_tle_id
        self.assertEquals(
            jrpc_sc.set_configuration(self.__sc_1_id, cfg),
            True,
            'The <set_configuration> JPRC method should have returned <True>'
        )
        actual_cfg = jrpc_sc.get_configuration(self.__sc_1_id)
        self.assertEquals(
            actual_cfg, cfg, 'Configurations differ'
            + ', e = ' + str(cfg)
            + ', a = ' + str(actual_cfg)
        )

    def test_add_once_rule(self):
        """
        This test validates that the system correctly adds a new rule to the
        set of rules for a given channel of a ground station.
        """
        if self.__verbose_testing:
            print '>>> TEST (test_gs_channel_add_rule)'

        # 1) add new rule to the database
        rule_cfg = db_tools.create_jrpc_once_rule()
        rule_id_1 = jrpc_rules.add_rule(
            self.__gs_1_id, self.__gs_1_ch_1_id, rule_cfg
        )
        jrpc_rules.add_rule(self.__gs_1_id, self.__gs_1_ch_1_id, rule_cfg)

        # 2) get the rule back through the JRPC interface
        rules_g1c1 = jrpc_rules.get_rules(self.__gs_1_id, self.__gs_1_ch_1_id)
        expected_r = {
            jrpc_serial.RULE_PERIODICITY: jrpc_serial.RULE_PERIODICITY_ONCE,
            jrpc_serial.RULE_OP: jrpc_serial.RULE_OP_ADD,
            jrpc_serial.RULE_DATES: {
                jrpc_serial.RULE_ONCE_DATE: misc.get_midnight() + timedelta(
                    days=1
                ),
                jrpc_serial.RULE_ONCE_S_TIME: misc.localize_time_utc(
                    time(hour=11, minute=15)
                ),
                jrpc_serial.RULE_ONCE_E_TIME: misc.localize_time_utc(
                    time(hour=11, minute=45)
                )
            }
        }

        if self.__verbose_testing:
            print '>>> rules from JRPC[' + str(len(rules_g1c1)) + ']:'
            for r in rules_g1c1:
                print str(r)
            print '>>> expected_r:'
            print str(expected_r)

        self.assertEquals(
            expected_r, rules_g1c1[0], 'Wrong ONCE rule!, diff = ' + str(
                diff(expected_r, rules_g1c1[0])
            )
        )

    def test_add_daily_rule(self):
        """
        This test validates that the system correctly adds a new rule to the
        set of rules for a given channel of a ground station.
        """
        if self.__verbose_testing:
            print '>>> TEST (test_gs_channel_add_rule)'

        # 1) A daily rule is inserted in the database:
        rule_cfg = db_tools.create_jrpc_daily_rule()
        jrpc_rules.add_rule(self.__gs_1_id, self.__gs_1_ch_1_id, rule_cfg)

        # 2) get the rule back through the JRPC interface
        rules_g1c1 = jrpc_rules.get_rules(self.__gs_1_id, self.__gs_1_ch_1_id)
        expected_r = {
            jrpc_serial.RULE_PERIODICITY: jrpc_serial.RULE_PERIODICITY_DAILY,
            jrpc_serial.RULE_OP: jrpc_serial.RULE_OP_ADD,
            jrpc_serial.RULE_DATES: {
                jrpc_serial.RULE_DAILY_I_DATE: misc.get_midnight() + timedelta(
                    days=1
                ),
                jrpc_serial.RULE_DAILY_F_DATE: misc.get_midnight() + timedelta(
                    days=366
                ),
                jrpc_serial.RULE_S_TIME: misc.localize_time_utc(
                    time(hour=11, minute=15)
                ),
                jrpc_serial.RULE_E_TIME: misc.localize_time_utc(
                    time(hour=11, minute=45)
                )
            }
        }

        if self.__verbose_testing:
            print '>>> rules from JRPC[' + str(len(rules_g1c1)) + ']:'
            for r in rules_g1c1:
                misc.print_dictionary(r)
            print '>>> expected_r:'
            misc.print_dictionary(expected_r)

        self.assertEquals(
            expected_r, rules_g1c1[0], 'Wrong DAILY rule!, diff = ' + str(
                diff(expected_r, rules_g1c1[0])
            )
        )

    def test_remove_rule(self):
        """
        This test validates that the system correctly adds a new rule to the
        set of rules for a given channel of a ground station.
        """
        if self.__verbose_testing:
            print '>>> TEST (test_gs_channel_add_rule)'

        rule_cfg = db_tools.create_jrpc_once_rule()
        rule_id = jrpc_rules.add_rule(
            self.__gs_1_id, self.__gs_1_ch_1_id, rule_cfg
        )
        jrpc_rules.remove_rule(self.__gs_1_id, self.__gs_1_ch_1_id, rule_id)

        try:
            rule = AvailabilityRule.objects.get(id=rule_id)
            self.fail(
                'Object should not have been found, rule_id = ' + str(rule.pk)
            )
        except AvailabilityRule.DoesNotExist as e:

            if self.__verbose_testing:
                print e.message