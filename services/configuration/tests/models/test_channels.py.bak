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
from services.configuration.jrpc.serializers import serialization as jrpc_keys
from services.configuration.jrpc.views import rules as jrpc_rules
from services.configuration.models import rules


class TestModels(test.TestCase):
    """
    Test class for the channel model testing process. It helps in managing the
    required testing database.

    The 'create' method is not tested since it is utilized for populating the
    testing database. Therefore, the correct exectuion of the rest of the tests
    involves a correct functioning of this method.
    """

    def setUp(self):
        """
        Populates the initial database with a set of objects required to run
        the following tests.
        """
        self.__verbose_testing = False

        if not self.__verbose_testing:
            logging.getLogger('configuration').setLevel(level=logging.CRITICAL)

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
        if not self.__verbose_testing:
            logging.getLogger('configuration').setLevel(level=logging.CRITICAL)
            logging.getLogger('simulation').setLevel(level=logging.CRITICAL)

    def test_1_get_availability_slots(self):
        """
        This test validates the generation of slots by the different rules
        supported by the configuration service.
        """
        if self.__verbose_testing:
            print '>>>>> get_availability_slots'

        self.__gs_1_ch_1 = db_tools.gs_add_channel(
            self.__gs, self.__band, self.__gs_1_ch_1_id
        )

        rule_1 = db_tools.create_jrpc_once_rule(
            operation=jrpc_keys.RULE_OP_REMOVE,
            date=misc.get_today_utc() + datetime.timedelta(days=2)
        )
        jrpc_rules.add_rule(self.__gs_1_id, self.__gs_1_ch_1_id, rule_1)
        if self.__verbose_testing:
            print 'slots = ' + str(len(
                rules.AvailabilityRule.objects.get_availability_slots(
                    self.__gs_1_ch_1
                )
            ))

        rule_2 = db_tools.create_jrpc_daily_rule()
        jrpc_rules.add_rule(self.__gs_1_id, self.__gs_1_ch_1_id, rule_2)
        if self.__verbose_testing:
            print 'slots = ' + str(len(
                rules.AvailabilityRule.objects.get_availability_slots(
                    self.__gs_1_ch_1
                )
            ))

        rule_3 = db_tools.create_jrpc_once_rule(
            operation=jrpc_keys.RULE_OP_REMOVE,
            date=misc.get_today_utc() + datetime.timedelta(days=3)
        )
        jrpc_rules.add_rule(self.__gs_1_id, self.__gs_1_ch_1_id, rule_3)
        if self.__verbose_testing:
            print 'slots = ' + str(len(
                rules.AvailabilityRule.objects.get_availability_slots(
                    self.__gs_1_ch_1
                )
            ))

        rule_4 = db_tools.create_jrpc_once_rule(
            operation=jrpc_keys.RULE_OP_REMOVE,
            date=misc.get_today_utc() + datetime.timedelta(days=3)
        )
        jrpc_rules.add_rule(self.__gs_1_id, self.__gs_1_ch_1_id, rule_4)
        if self.__verbose_testing:
            print 'slots = ' + str(len(
                rules.AvailabilityRule.objects.get_availability_slots(
                    self.__gs_1_ch_1
                )
            ))

        rules_n = len(rules.AvailabilityRule.objects.all())
        self.assertEquals(
            rules_n, 4,
            'Incorrect number of rules, expected = 4, actual = ' + str(rules_n)
        )

        actual_s = rules.AvailabilityRule.objects.get_availability_slots(
            self.__gs_1_ch_1
        )
        if self.__verbose_testing:
            print '>>> today_utc = ' + str(misc.get_today_utc())
            print '>>> window = ' + str(
                simulation.OrbitalSimulator.get_simulation_window()
            )
            misc.print_list(
                rules.AvailabilityRule.objects.all(), name='RULES'
            )
            misc.print_list(actual_s, name='AVAILABLE')

        self.assertEquals(
            len(actual_s), 1,
            'Wrong number of available slots, e = 2, actual = ' + str(len(
                actual_s
            ))
        )