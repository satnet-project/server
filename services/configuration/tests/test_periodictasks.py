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

from django import test
import datadiff
import datetime
import logging
from services.common import misc
from services.common.testing import helpers as db_tools
from services.configuration import periodictasks
from services.configuration.signals import models as model_signals
from services.configuration.models import availability
from services.configuration.jrpc.views import rules as jrpc_rules_if
from services.scheduling.models import operational


class TestSlotPropagation(test.TestCase):
    """Unit test class.
    This test validates the slot propagation within the database for the
    following future passes.
    """

    def setUp(self):

        self.__verbose_testing = False

        if not self.__verbose_testing:
            logging.getLogger('configuration').setLevel(level=logging.CRITICAL)

        self.__gs_1_id = 'gs-castrelos'
        self.__gs_1_ch_1_id = 'chan-cas-1'
        self.__sc_1_id = 'sc-xatcobeo'
        self.__sc_1_ch_1_id = 'xatco-fm-1'
        self.__sc_1_ch_1_f = 437000000

        model_signals.connect_availability_2_operational()
        model_signals.connect_channels_2_compatibility()
        model_signals.connect_compatibility_2_operational()
        model_signals.connect_rules_2_availability()

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
        operational.OperationalSlot.objects.get_simulator().set_debug()

        if not self.__verbose_testing:
            logging.getLogger('configuration').setLevel(level=logging.CRITICAL)
            logging.getLogger('simulation').setLevel(level=logging.CRITICAL)

    def test_propagate_empty_db(self):
        """Unit test.
        This test validates the propagation of the slots throughout the
        database when no rules are available (empty database stability check).
        """
        if self.__verbose_testing:
            print('>>> test_propagate_empty_db:')

        periodictasks.populate_slots()
        self.assertEqual(
            len(availability.AvailabilitySlot.objects.all()),
            0,
            'No slots should have been created!'
        )

    def test_propagate_simple(self):
        """Unit test.
        This test validates the propagation of the slots with a simple set of
        rules.
        """
        if self.__verbose_testing:
            print('>>> test_propagate_simple:')

        now = misc.get_now_utc()
        r_1_s_time = now + datetime.timedelta(minutes=10)
        r_1_e_time = now + datetime.timedelta(hours=5)

        r_cfg = db_tools.create_jrpc_daily_rule(
            starting_time=r_1_s_time,
            ending_time=r_1_e_time
        )
        r_1_id = jrpc_rules_if.add_rule(
            self.__gs_1_id, self.__gs_1_ch_1_id, r_cfg
        )

        expected_pre = [
            (
                r_1_s_time + datetime.timedelta(days=1),
                r_1_e_time + datetime.timedelta(days=1),
            ),
            (
                r_1_s_time + datetime.timedelta(days=2),
                r_1_e_time + datetime.timedelta(days=2),
            ),
        ]
        actual_pre = list(
            operational.OperationalSlot.objects.values_list('start', 'end')
        )

        self.assertEqual(
            actual_pre, expected_pre, 'Wrong OperationalSlots (pre-propagate)'
        )

        periodictasks.populate_slots()

        expected_post = [
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
            ),
        ]
        actual_post = list(
            operational.OperationalSlot.objects.values_list('start', 'end')
        )

        self.assertEqual(
            actual_post, expected_post,
            'Wrong OperationalSlots (post-propagate), diff = ' + str(
                datadiff.diff(actual_post, expected_post)
            )
        )

        self.assertTrue(
            jrpc_rules_if.remove_rule(
                self.__gs_1_id, self.__gs_1_ch_1_id, r_1_id
            ),
            'Could not remove rule with ID = ' + str(r_1_id)
        )