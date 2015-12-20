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

from services.common import misc, helpers as db_tools
from services.configuration.jrpc.views import rules as jrpc_rules_if
from services.scheduling.models import operational, availability
from services.scheduling import periodictasks as scheduling_tasks


class TestSlotPropagation(test.TestCase):
    """Unit test class.
    This test validates the slot propagation within the database for the
    following future passes.
    """

    # noinspection PyUnresolvedReferences
    def setUp(self):

        self.__verbose_testing = False

        if not self.__verbose_testing:
            logging.getLogger('configuration').setLevel(level=logging.CRITICAL)
            logging.getLogger('simulation').setLevel(level=logging.CRITICAL)

        self.__gs_1_id = 'gs-castrelos'
        self.__gs_1_ch_1_id = 'chan-cas-1'
        self.__sc_1_id = 'sc-xatcobeo'
        self.__sc_1_ch_1_id = 'xatco-fm-1'
        self.__sc_1_ch_1_f = 437000000

        from services.configuration.signals import tle
        from services.scheduling.signals import compatibility
        from services.scheduling.signals import availability

        self.__band = db_tools.create_band()
        self.__user_profile = db_tools.create_user_profile()
        self.__gs_1 = db_tools.create_gs(
            user_profile=self.__user_profile, identifier=self.__gs_1_id,
        )
        self.__gs_1_ch_1 = db_tools.gs_add_channel(
            self.__gs_1, self.__band, self.__gs_1_ch_1_id
        )
        self.__sc_1 = db_tools.create_sc(
            user_profile=self.__user_profile, identifier=self.__sc_1_id
        )
        self.__sc_1_ch_1 = db_tools.sc_add_channel(
            self.__sc_1, self.__sc_1_ch_1_f, self.__sc_1_ch_1_id,
        )

    def test_propagate_empty_db(self):
        """INTR test: services.scheduling - initial slot propagation
        This test validates the propagation of the slots throughout the
        database when no rules are available (empty database stability check).
        """
        if self.__verbose_testing:
            print('>>> test_propagate_empty_db:')

        scheduling_tasks.populate_slots()
        self.assertEqual(len(availability.AvailabilitySlot.objects.all()), 0)

    def test_propagate_simple(self):
        """INTR test: services.scheduling - slot propagation
        This test validates the propagation of the slots with a simple set of
        rules.
        """
        if self.__verbose_testing:
            print('>>> test_propagate_simple:')

        r_1_s_time = misc.get_next_midnight() - datetime.timedelta(hours=12)
        r_1_e_time = r_1_s_time + datetime.timedelta(hours=10)

        r_cfg = db_tools.create_jrpc_daily_rule(
            starting_time=r_1_s_time,
            ending_time=r_1_e_time
        )

        self.assertEquals(list(availability.AvailabilitySlot.objects.all()), [])

        r_1_id = jrpc_rules_if.add_rule(self.__gs_1_id, r_cfg)

        x_pre = [
            (
                r_1_s_time,
                r_1_e_time,
            ),
            (
                r_1_s_time + datetime.timedelta(days=1),
                r_1_e_time + datetime.timedelta(days=1),
            ),
            (
                r_1_s_time + datetime.timedelta(days=2),
                r_1_e_time + datetime.timedelta(days=2),
            )
        ]
        a_pre = list(
            availability.AvailabilitySlot.objects.values_list('start', 'end')
        )
        self.assertEqual(a_pre, x_pre)

        scheduling_tasks.populate_slots()

        expected_post = [
            (
                r_1_s_time,
                r_1_e_time,
            ),
            (
                r_1_s_time + datetime.timedelta(days=1),
                r_1_e_time + datetime.timedelta(days=1),
            ),
            (
                r_1_s_time + datetime.timedelta(days=2),
                r_1_e_time + datetime.timedelta(days=2),
            ),
            (
                r_1_s_time + datetime.timedelta(days=3),
                r_1_e_time + datetime.timedelta(days=3),
            )
        ]
        actual_post = list(
            availability.AvailabilitySlot.objects.values_list('start', 'end')
        )

        self.assertEqual(actual_post, expected_post)
        self.assertTrue(jrpc_rules_if.remove_rule(self.__gs_1_id, r_1_id))

        self.assertListEqual(
            list(availability.AvailabilitySlot.objects.all()), []
        )
        self.assertListEqual(
            list(operational.OperationalSlot.objects.all()), []
        )
