"""
   Copyright 2016 Ricardo Tubio-Pardavila

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
from services.configuration.jrpc.views import rules as rules_jrpc
from services.common import helpers as db_tools
from services.common import misc as sn_misc
from services.simulation.models import passes as pass_models
from services.scheduling.models import availability as availability_models
from services.scheduling.models import operational as operational_models


class OperationalSlotsBugTest(test.TestCase):
    """
    Class with the UNIT tests for reproducing and fixing the bug that happens
    when filtering the pass slots to generate operational slots.
    """

    def setUp(self):

        self.__verbose_testing = False

        if not self.__verbose_testing:
            logging.getLogger('configuration').setLevel(level=logging.CRITICAL)
            logging.getLogger('scheduling').setLevel(level=logging.CRITICAL)
            logging.getLogger('simulation').setLevel(level=logging.CRITICAL)

#    @mock.patch(
#        'services.common.simulation.OrbitalSimulator',
#        sn_mocks.mock__OrbitalSimulator
#    )
    def test_bug_1(self):
        """INTR test: services.scheduling - operational slot generation
        """

        self.__gs_1_id = 'gs-vigo'
        self.__gs_1_ch_1_id = 'chan-cas-1'
        self.__sc_1_id = 'sc-serpens'
        self.__sc_1_ch_1_id = 'xatco-fm-1'
        self.__sc_1_ch_1_f = 437500000

        self.__band = db_tools.create_band()
        self.__user_profile = db_tools.create_user_profile()

        # 1) create vigo gs
        self.__gs = db_tools.create_gs(
            user_profile=self.__user_profile, identifier=self.__gs_1_id
        )

        # CHECK A: NO ADDITIONAL pass slots, no operational slots
        # ### There are pass slots for the already-propagated spacecraft
        p_slots_0 = pass_models.PassSlots.objects.filter(
            groundstation__identifier=self.__gs_1_id,
            spacecraft__identifier=self.__sc_1_id
        )

        self.assertEqual(len(p_slots_0), 0)
        o_slots_0 = operational_models.OperationalSlot.objects.filter(
            pass_slot__in=p_slots_0
        )
        self.assertEqual(len(o_slots_0), 0)

        # 2) serpens spacecraft
        self.__sc = db_tools.create_sc(
            user_profile=self.__user_profile, identifier=self.__sc_1_id
        )

        # CHECK B: MORE pass slots, no operational slots
        # ### There are pass slots for the already-propagated spacecraft
        p_slots_1 = pass_models.PassSlots.objects.filter(
            groundstation__identifier=self.__gs_1_id,
            spacecraft__identifier=self.__sc_1_id
        )
        self.assertGreater(len(p_slots_1), len(p_slots_0))
        o_slots_0 = operational_models.OperationalSlot.objects.filter(
            pass_slot__in=p_slots_0
        )
        self.assertEqual(len(o_slots_0), 0)

        # 3) we add channels and, therefore, compatibility matches
        #       without availability rules, no operational slots
        self.__sc_1_ch_1 = db_tools.sc_add_channel(
            self.__sc, self.__sc_1_ch_1_f, self.__sc_1_ch_1_id
        )
        self.__gs_1_ch_1 = db_tools.gs_add_channel(
            self.__gs, self.__band, self.__gs_1_ch_1_id
        )

        # CHECK C: SAME pass slots, no operational slots
        # ### There are pass slots for the already-propagated spacecraft
        p_slots_2 = pass_models.PassSlots.objects.filter(
            groundstation__identifier=self.__gs_1_id,
            spacecraft__identifier=self.__sc_1_id
        )
        self.assertEqual(len(p_slots_2), len(p_slots_1))
        o_slots_0 = operational_models.OperationalSlot.objects.filter(
            pass_slot__in=p_slots_0
        )
        self.assertEqual(len(o_slots_0), 0)

        # 4) we add a daily rule 12 hours, 00:00:01am to 11:59:59pm UTC
        #       all pass slots should became operational slots.
        self.__rule_1 = rules_jrpc.add_rule(
            self.__gs_1_id,
            db_tools.create_jrpc_daily_rule(
                date_i=sn_misc.get_today_utc(),
                date_f=sn_misc.get_today_utc() + datetime.timedelta(days=50),
                starting_time=sn_misc.get_next_midnight() + datetime.timedelta(
                    seconds=1
                ),
                ending_time=sn_misc.get_next_midnight() + datetime.timedelta(
                    hours=23, minutes=59, seconds=59
                )
            )
        )

        # CHECK D: 3 availability slots (1 per day, almost 24 hours)
        #           should transform all pass slots into operational slots
        a_slots = availability_models.AvailabilitySlot.objects.values_list(
            'start', 'end'
        )
        x_slots = [
            (
                sn_misc.get_today_utc() + datetime.timedelta(
                    seconds=1
                ),
                sn_misc.get_today_utc() + datetime.timedelta(
                    hours=23, minutes=59, seconds=59
                )
            ),
            (
                sn_misc.get_today_utc() + datetime.timedelta(
                    days=1, seconds=1
                ),
                sn_misc.get_today_utc() + datetime.timedelta(
                    days=1, hours=23, minutes=59, seconds=59
                )
            ),
            (
                sn_misc.get_today_utc() + datetime.timedelta(
                    days=2, seconds=1
                ),
                sn_misc.get_today_utc() + datetime.timedelta(
                    days=2, hours=23, minutes=59, seconds=59
                )
            )
        ]

        self.assertCountEqual(a_slots, x_slots)

        p_slots_applicable_objs = pass_models.PassSlots.objects.filter(
            groundstation__identifier=self.__gs_1_id,
            spacecraft__identifier=self.__sc_1_id,
            start__gte=sn_misc.get_now_utc()
        )
        p_slots_applicable = p_slots_applicable_objs.values_list('start', 'end')

        self.assertGreaterEqual(len(p_slots_2), len(p_slots_applicable))

        o_slots_1 = operational_models.OperationalSlot.objects.filter(
            pass_slot__in=p_slots_applicable_objs,
            state=operational_models.STATE_FREE
        ).values_list('start', 'end')

        self.assertCountEqual(p_slots_applicable, o_slots_1)
