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
from django import test
import logging
from services.common import misc, simulation
from services.common.testing import helpers as db_tools
from services.configuration.signals import models as model_signals
from services.configuration.jrpc.views import rules as jrpc_rules_if
from services.configuration.models import rules as rule_models


class TestChannelRules(test.TestCase):
    """
    This class includes all the tests for the critical points of how to manage
    the rules that are referred only to certain channels and that are not part
    of any group of rules.
    """

    def setUp(self):
        """
        Populates the initial database with a set of objects required to run
        the following tests.
        """
        self.__verbose_testing = False

        if not self.__verbose_testing:
            logging.getLogger('configuration').setLevel(level=logging.CRITICAL)
            logging.getLogger('simulation').setLevel(level=logging.CRITICAL)

        self.__gs_1_id = 'gs-castrelos'
        self.__gs_1_ch_1_id = 'chan-cas-1'

        model_signals.connect_rules_2_availability()

        self.__band = db_tools.create_band()
        self.__user_profile = db_tools.create_user_profile()
        self.__gs_1 = db_tools.create_gs(
            user_profile=self.__user_profile, identifier=self.__gs_1_id,
        )
        self.__gs_1_ch_1 = db_tools.gs_add_channel(
            self.__gs_1, self.__band, self.__gs_1_ch_1_id
        )

    def test_1_a_slots_daily(self):
        """services.configuration: generate available slots (DAILY rule, 1)
        Validates the generation of slots by a daily rule.
        """
        if self.__verbose_testing:
            print('>>> test_1_generate_available_slots_daily:')

        now = misc.get_now_utc()
        r_1_s_time = now + datetime.timedelta(minutes=30)
        r_1_e_time = now + datetime.timedelta(minutes=45)

        r_cfg = db_tools.create_jrpc_daily_rule(
            starting_time=r_1_s_time,
            ending_time=r_1_e_time
        )
        r_1_id = jrpc_rules_if.add_rule(self.__gs_1_id, r_cfg)

        rs = rule_models.AvailabilityRuleManager.get_applicable_rule_values(
            self.__gs_1
        )
        if self.__verbose_testing:
            misc.print_list(rs, name='Rules')

        expected = [
            (
                r_1_s_time + datetime.timedelta(days=1),
                r_1_e_time + datetime.timedelta(days=1),
            ),
            (
                r_1_s_time + datetime.timedelta(days=2),
                r_1_e_time + datetime.timedelta(days=2),
            ),
        ]
        actual = rule_models.AvailabilityRuleManager\
            .generate_available_slots_daily(rs[0][0],)

        if self.__verbose_testing:
            print('>>> window = ' + str(
                simulation.OrbitalSimulator.get_simulation_window()
            ))
            misc.print_list(actual, name='Generated Slots')

        self.assertEqual(actual, expected, 'Wrong slots')

        jrpc_rules_if.remove_rule(self.__gs_1_id, r_1_id)