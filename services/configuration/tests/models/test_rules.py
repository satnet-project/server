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

import pytz
from django import test

from services.common import misc, simulation
from services.common import helpers as db_tools
from services.configuration.jrpc.serializers import rules as jrpc_keys
from services.configuration.jrpc.views import rules as jrpc_rules
from services.configuration.models import rules as rule_models


class TestRulesAvailability(test.TestCase):
    """
    Test class for the channel model testing process. It helps in managing the
    required testing database.
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

        # noinspection PyUnresolvedReferences
        from services.scheduling.signals import availability

        self.__gs_1_id = 'gs-castrelos'
        self.__gs_1_ch_1_id = 'chan-cas-1'

        self.__sc_1_id = 'sc-xatcobeo'
        self.__sc_1_ch_1_id = 'xatco-fm-1'
        self.__sc_1_ch_2_id = 'xatco-fm-2'
        self.__sc_1_ch_3_id = 'xatco-fm-3'
        self.__sc_1_ch_4_id = 'xatco-afsk-1'

        self.__band = db_tools.create_band()
        self.__test_user_profile = db_tools.create_user_profile()
        self.__gs = db_tools.create_gs(
            user_profile=self.__test_user_profile, identifier=self.__gs_1_id,
        )
        self.__sc = db_tools.create_sc(
            user_profile=self.__test_user_profile, identifier=self.__sc_1_id
        )

    def test_slot_once_time_ranges(self):
        """UNIT test: services.configuration - ONCE rule configuration
        """
        if self.__verbose_testing:
            print('>>> test_slot_once_time_ranges:')

        s_time = misc.get_next_midnight() - datetime.timedelta(hours=3)
        e_time = s_time + datetime.timedelta(hours=6)
        tz_la = pytz.timezone('America/Los_Angeles')
        s_time = s_time.astimezone(tz_la)
        e_time = e_time.astimezone(tz_la)

        cfg = db_tools.create_jrpc_once_rule(
            starting_time=s_time, ending_time=e_time
        )

        if self.__verbose_testing:
            misc.print_dictionary(cfg)

        jrpc_rules.add_rule(self.__gs_1_id, cfg)

    def test_is_applicable(self):
        """services.configuration: rule interval applicability
        Validates the method that checks whether a given rule may or may not
        generate slots during the given interval.
        """
        if self.__verbose_testing:
            print('>>> test_is_applicable:')

        s_window = simulation.OrbitalSimulator.get_simulation_window()
        p_window = simulation.OrbitalSimulator.get_update_window()

        if self.__verbose_testing:
            print('>>> s_window = ' + str(s_window))
            print('>>> p_window = ' + str(p_window))

        # 1) inside the simulation, outside the propagation
        s_time = s_window[0] + datetime.timedelta(minutes=1)
        e_time = s_window[1] - datetime.timedelta(minutes=1)
        r = {
            'starting_date': s_time.date(),
            'ending_date': e_time.date(),
            'starting_time': s_time,
            'ending_time': e_time
        }

        self.assertIsNotNone(
            rule_models.AvailabilityRule.objects.is_applicable(r, s_window)
        )
        self.assertRaises(
            Exception,
            rule_models.AvailabilityRule.objects.is_applicable, r, p_window
        )

        # 1) starts before the simulation, ends within it
        # 1) outside the propagation
        s_time = s_window[0] - datetime.timedelta(minutes=1)
        e_time = s_window[1] - datetime.timedelta(minutes=1)
        r = {
            'starting_date': s_time.date(),
            'ending_date': e_time.date(),
            'starting_time': s_time,
            'ending_time': e_time
        }

        self.assertIsNotNone(
            rule_models.AvailabilityRule.objects.is_applicable(r, s_window)
        )
        self.assertRaises(
            Exception,
            rule_models.AvailabilityRule.objects.is_applicable, r, p_window
        )

        # 2) starts within the simulation, ends after it
        # 2) starts before the propagation, ends within it
        s_time = s_window[0] + datetime.timedelta(minutes=1)
        e_time = s_window[1] + datetime.timedelta(minutes=1)
        r = {
            'starting_date': s_time.date(),
            'ending_date': e_time.date(),
            'starting_time': s_time,
            'ending_time': e_time
        }

        self.assertIsNotNone(
            rule_models.AvailabilityRule.objects.is_applicable(r, s_window)
        )
        self.assertIsNotNone(
            rule_models.AvailabilityRule.objects.is_applicable(r, p_window)
        )

        # 3) outside the simulation window
        # 3) starts and ends within the propagation window
        s_time = p_window[0] + datetime.timedelta(minutes=1)
        e_time = p_window[1] - datetime.timedelta(minutes=1)
        r = {
            'starting_date': s_time.date(),
            'ending_date': e_time.date(),
            'starting_time': s_time,
            'ending_time': e_time
        }

        self.assertRaises(
            Exception,
            rule_models.AvailabilityRule.objects.is_applicable, r, s_window
        )
        self.assertIsNotNone(
            rule_models.AvailabilityRule.objects.is_applicable(r, p_window)
        )

        # 4) outside the simulation window
        # 4) starts within the propagation window, ends outside of it
        s_time = p_window[0] + datetime.timedelta(minutes=1)
        e_time = p_window[1] + datetime.timedelta(minutes=1)
        r = {
            'starting_date': s_time.date(),
            'ending_date': e_time.date(),
            'starting_time': s_time,
            'ending_time': e_time
        }

        self.assertRaises(
            Exception,
            rule_models.AvailabilityRule.objects.is_applicable, r, s_window
        )
        self.assertIsNotNone(
            rule_models.AvailabilityRule.objects.is_applicable(r, p_window)
        )

        # 5) outside the simulation window
        # 5) outside the propagation window
        s_time = p_window[1] + datetime.timedelta(minutes=1)
        e_time = p_window[1] + datetime.timedelta(minutes=2)
        r = {
            'starting_date': s_time.date(),
            'ending_date': e_time.date(),
            'starting_time': s_time,
            'ending_time': e_time
        }

        self.assertRaises(
            Exception,
            rule_models.AvailabilityRule.objects.is_applicable, r, s_window
        )
        self.assertRaises(
            Exception,
            rule_models.AvailabilityRule.objects.is_applicable, r, p_window
        )

    def _test_1_a_slots_daily(self):
        """services.configuration: generate available slots (DAILY rule, 1)
        Validates the generation of slots by a daily rule.
        """
        if self.__verbose_testing:
            print('>>> test_1_generate_available_slots_daily:')

        now = misc.get_next_midnight()
        r_1_s_time = now - datetime.timedelta(hours=12)
        r_1_e_time = r_1_s_time + datetime.timedelta(hours=4)

        r_cfg = db_tools.create_jrpc_daily_rule(
            starting_time=r_1_s_time,
            ending_time=r_1_e_time
        )
        r_1_id = jrpc_rules.add_rule(self.__gs_1_id, r_cfg)

        rs = rule_models.AvailabilityRuleManager.get_applicable_rule_values(
            self.__gs
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

        jrpc_rules.remove_rule(self.__gs_1_id, r_1_id)

    def _test_1_get_availability_slots(self):
        """services.configuration: get availability slots
        This test validates the generation of slots by the different rules
        supported by the configuration service.
        """
        if self.__verbose_testing:
            print('>>>>> get_availability_slots')

        self.__gs_1_ch_1 = db_tools.gs_add_channel(
            self.__gs, self.__band, self.__gs_1_ch_1_id
        )

        rule_1 = db_tools.create_jrpc_once_rule(
            operation=jrpc_keys.RULE_OP_REMOVE
        )
        jrpc_rules.add_rule(self.__gs_1_id, rule_1)
        if self.__verbose_testing:
            print('slots = ' + str(len(
                rule_models.AvailabilityRule.objects.get_availability_slots(
                    self.__gs
                )
            )))

        rule_2 = db_tools.create_jrpc_daily_rule()
        jrpc_rules.add_rule(self.__gs_1_id, rule_2)
        if self.__verbose_testing:
            print('slots = ' + str(len(
                rule_models.AvailabilityRule.objects.get_availability_slots(
                    self.__gs
                )
            )))

        rule_3 = db_tools.create_jrpc_once_rule(
            operation=jrpc_keys.RULE_OP_REMOVE
        )
        jrpc_rules.add_rule(self.__gs_1_id, rule_3)

        if self.__verbose_testing:
            print('slots = ' + str(len(
                rule_models.AvailabilityRule.objects.get_availability_slots(
                    self.__gs
                )
            )))

        rule_4 = db_tools.create_jrpc_once_rule(
            operation=jrpc_keys.RULE_OP_REMOVE
        )
        jrpc_rules.add_rule(self.__gs_1_id, rule_4)

        if self.__verbose_testing:
            print('slots = ' + str(len(
                rule_models.AvailabilityRule.objects.get_availability_slots(
                    self.__gs
                )
            )))

        rules_n = len(rule_models.AvailabilityRule.objects.all())
        self.assertEqual(
            rules_n, 4,
            'Incorrect number of rules, expected = 4, actual = ' + str(rules_n)
        )

        actual_s = rule_models.AvailabilityRule.objects.get_availability_slots(
            self.__gs
        )

        if self.__verbose_testing:
            print('>>> today_utc = ' + str(misc.get_today_utc()))
            print('>>> window = ' + str(
                simulation.OrbitalSimulator.get_simulation_window()
            ))
            misc.print_list(
                rule_models.AvailabilityRule.objects.all(), name='RULES'
            )
            misc.print_list(actual_s, name='AVAILABLE')

        self.assertEqual(
            len(actual_s), 1,
            'Wrong number of available slots, e = 1, actual = ' + str(len(
                actual_s
            ))
        )
