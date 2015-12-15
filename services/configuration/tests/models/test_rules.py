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

from services.common import misc
from services.common import helpers as db_tools
from services.configuration.jrpc.views import rules as jrpc_rules


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

    """
    def _test_is_applicable(self):
        #UNIT test: services.configuration: rule interval applicability
        #Validates the method that checks whether a given rule may or may not
        #generate slots during the given interval.
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
    """
