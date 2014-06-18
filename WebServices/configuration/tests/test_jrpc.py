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

from datetime import time, timedelta

from django.test import TestCase
from common.misc import get_today_utc, localize_time_utc, print_dictionary
from configuration.jrpc import segments as jrpc_segments,\
    rules as jrpc_rules, serialization as jrpc_serial
from configuration.models.rules import AvailabilityRule
import common.testing as db_tools


class JRPCRulesTest(TestCase):

    def setUp(self):
        """
        This method populates the database with some information to be used
        only for this test.
        """
        self.__verbose_testing = False

        self.__gs_1_id = 'gs-castrelos'
        self.__gs_1_callsign = 'GS1GSGS'
        self.__gs_1_contact_elevation = 10.30
        self.__gs_1_longitude = 25.0
        self.__gs_1_latitude = 40.0
        self.__gs_1_configuration = (
            unicode(self.__gs_1_callsign, 'unicode-escape'),
            '10.30',
            str(self.__gs_1_latitude),
            str(self.__gs_1_longitude)
        )
        self.__gs_2_id = 'gs-calpoly'
        self.__gs_1_ch_1_id = 'fm-1'
        self.__gs_1_ch_2_id = 'afsk-2'

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
            # ### TODO ::  include "altitude" as a configuration parameter
        )
        self.__gs_1_ch_1 = db_tools.gs_add_channel(
            self.__gs_1, self.__band, self.__gs_1_ch_1_id,
        )
        self.__gs_2 = db_tools.create_gs(
            user_profile=self.__user_profile,
            identifier=self.__gs_2_id
        )

    def test_gs_list(self):
        """
        This test validates the list of configuration objects returned through
        the JRPC method.
        """
        if self.__verbose_testing:
            print '>>> TEST (test_gs_list)'
        gs_list = jrpc_segments.gs_list(request=self.__http_request)
        self.assertItemsEqual(
            gs_list, ['gs-castrelos', 'gs-calpoly'], 'Wrong gs identifiers.'
        )

    def test_gs_channels(self):
        """
        This test validates the list of channels returned throught the JRPC
        method.
        """
        if self.__verbose_testing:
            print '>>> TEST (test_gs_channels)'
        ch_list = jrpc_segments.gs_get_channels(self.__gs_1_id)
        self.assertItemsEqual(
            ch_list['groundstation_channels'], [self.__gs_1_ch_1_id],
            'Wrong channel identifiers, ch = ' + str(ch_list)
        )

    def test_gs_get_configuration(self):
        """
        This test validates the returned configuration by the proper JRPC
        method.
        """
        if self.__verbose_testing:
            print '>>> TEST (test_gs_get_configuration):'
        cfg = jrpc_segments.deserialize_gs_configuration(
            jrpc_segments.gs_get_configuration(self.__gs_1_id)
        )
        self.assertEquals(
            cfg, self.__gs_1_configuration, 'Wrong configuration returned.'
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
                jrpc_serial.RULE_ONCE_DATE: get_today_utc().replace(
                    hour=0, minute=0, second=0
                ) + timedelta(days=1),
                jrpc_serial.RULE_ONCE_S_TIME: localize_time_utc(
                    time(hour=11, minute=15)
                ),
                jrpc_serial.RULE_ONCE_E_TIME: localize_time_utc(
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
            expected_r, rules_g1c1[0], 'Wrong ONCE rule!'
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
                jrpc_serial.RULE_DAILY_I_DATE: get_today_utc().replace(
                    hour=0, minute=0, second=0
                ) + timedelta(days=1),
                jrpc_serial.RULE_DAILY_F_DATE: get_today_utc().replace(
                    hour=0, minute=0, second=0
                ) + timedelta(days=366),
                jrpc_serial.RULE_S_TIME: localize_time_utc(
                    time(hour=11, minute=15)
                ),
                jrpc_serial.RULE_E_TIME: localize_time_utc(
                    time(hour=11, minute=45)
                )
            }
        }

        if self.__verbose_testing:
            print '>>> rules from JRPC[' + str(len(rules_g1c1)) + ']:'
            for r in rules_g1c1:
                print_dictionary(r)
            print '>>> expected_r:'
            print_dictionary(expected_r)

        self.assertEquals(
            expected_r, rules_g1c1[0], 'Wrong DAILY rule!'
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