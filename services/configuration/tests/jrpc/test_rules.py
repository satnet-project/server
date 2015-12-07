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

import datetime
import logging

from django import test

from services.common import misc
from services.common import serialization as common_serial
from services.common import helpers as db_tools
from services.configuration.jrpc.serializers import rules as jrpc_serial
from services.configuration.jrpc.views import rules as jrpc_rules
from services.configuration.models import rules


class JRPCRulesTest(test.TestCase):

    def setUp(self):
        """Test setup
        Initial database configuration for the tests.
        """
        self.__verbose_testing = False

        if not self.__verbose_testing:
            logging.getLogger('common').setLevel(level=logging.CRITICAL)
            logging.getLogger('configuration').setLevel(level=logging.CRITICAL)

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
        self.__gs_1_ch_1_id = 'fm-1'
        self.__gs_1_ch_2_id = 'afsk-2'

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

    def test_add_once_rule(self):
        """JRPC test: (O) cfg.gs.channel.addRule, cfg.gs.channel.removeRule
        Should correctly add a ONCE rule to the system.
        """
        if self.__verbose_testing:
            print('>>> TEST (test_gs_channel_add_rule)')

        # 1) add new rule to the database
        starting_time = misc.get_next_midnight() - datetime.timedelta(hours=12)
        ending_time = starting_time + datetime.timedelta(hours=4)

        rule_cfg = db_tools.create_jrpc_once_rule(
            starting_time=starting_time,
            ending_time=ending_time
        )
        rule_id_1 = jrpc_rules.add_rule(self.__gs_1_id, rule_cfg)

        # 2) get the rule back through the JRPC interface
        rules_g1c1 = jrpc_rules.list_channel_rules(self.__gs_1_id)
        expected_r = {
            jrpc_serial.RULE_PK_K: rule_id_1,
            jrpc_serial.RULE_PERIODICITY: jrpc_serial.RULE_PERIODICITY_ONCE,
            jrpc_serial.RULE_OP: jrpc_serial.RULE_OP_ADD,
            jrpc_serial.RULE_DATES: {
                jrpc_serial.RULE_ONCE_S_TIME: starting_time.isoformat(),
                jrpc_serial.RULE_ONCE_E_TIME: ending_time.isoformat()
            }
        }

        if self.__verbose_testing:
            misc.print_list(rules_g1c1, name='DATABASE')
            misc.print_dictionary(expected_r)

        self.assertEqual(rules_g1c1[0], expected_r)

        jrpc_rules.remove_rule(self.__gs_1_id, rule_id_1)
        self.__verbose_testing = False

    def test_add_daily_rule(self):
        """JRPC test: (D) cfg.gs.channel.addRule, cfg.gs.channel.removeRule
        Should correctly add a DAILY rule to the system.
        """
        if self.__verbose_testing:
            print('>>> TEST (test_gs_channel_add_rule)')

        now = misc.get_now_utc()
        r_1_s_time = now + datetime.timedelta(minutes=30)
        r_1_e_time = now + datetime.timedelta(minutes=45)

        # 1) A daily rule is inserted in the database:
        rule_cfg = db_tools.create_jrpc_daily_rule(
            starting_time=r_1_s_time,
            ending_time=r_1_e_time
        )
        rule_pk = jrpc_rules.add_rule(self.__gs_1_id, rule_cfg)

        # 2) get the rule back through the JRPC interface
        rules_g1c1 = jrpc_rules.list_channel_rules(self.__gs_1_id)
        expected_r = {
            jrpc_serial.RULE_PK_K: rule_pk,
            jrpc_serial.RULE_PERIODICITY: jrpc_serial.RULE_PERIODICITY_DAILY,
            jrpc_serial.RULE_OP: jrpc_serial.RULE_OP_ADD,
            jrpc_serial.RULE_DATES: {
                jrpc_serial.RULE_DAILY_I_DATE: common_serial
                .serialize_iso8601_date(
                    misc.get_today_utc() + datetime.timedelta(days=1)
                ),
                jrpc_serial.RULE_DAILY_F_DATE: common_serial
                .serialize_iso8601_date(
                    misc.get_today_utc() + datetime.timedelta(days=366)
                ),
                jrpc_serial.RULE_S_TIME: common_serial
                .serialize_iso8601_time(
                    r_1_s_time
                ),
                jrpc_serial.RULE_E_TIME: common_serial
                .serialize_iso8601_time(
                    r_1_e_time
                )
            }
        }

        if self.__verbose_testing:
            print('>>> rules from JRPC[' + str(len(rules_g1c1)) + ']:')
            for r in rules_g1c1:
                misc.print_dictionary(r)
            print('>>> expected_r:')
            misc.print_dictionary(expected_r)

        self.assertEqual(rules_g1c1[0], expected_r)

    def test_remove_rule(self):
        """JRPC test: cfg.gs.channel.removeRule
        Should correctly remove any rule to the system.
        """
        if self.__verbose_testing:
            print('>>> TEST (test_gs_channel_add_rule)')

        rule_cfg = db_tools.create_jrpc_once_rule()
        rule_id = jrpc_rules.add_rule(self.__gs_1_id, rule_cfg)
        jrpc_rules.remove_rule(self.__gs_1_id, rule_id)

        self.assertRaises(
            rules.AvailabilityRule.DoesNotExist,
            rules.AvailabilityRule.objects.get, id=rule_id
        )
