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

:Author:
    Ricardo Tubio-Pardavila (rtubiopa@calpoly.edu)
"""
__author__ = 'rtubiopa@calpoly.edu'

import datadiff
import datetime
import logging
import pytz

from django import test

from services.common import misc, simulation
from services.common.testing import helpers as db_tools
from services.configuration.jrpc.serializers import serialization as jrpc_serial
from services.configuration.jrpc.views import rules as jrpc_rules_if
from services.configuration.models import rules, availability


class TestAvailability(test.TestCase):

    def setUp(self):

        self.__verbose_testing = False

        if not self.__verbose_testing:
            logging.getLogger('configuration').setLevel(level=logging.CRITICAL)

        self.__gs_1_id = 'gs-castrelos'
        self.__gs_1_ch_1_id = 'chan-cas-1'

        self.__band = db_tools.create_band()
        self.__user_profile = db_tools.create_user_profile()
        self.__gs = db_tools.create_gs(
            user_profile=self.__user_profile, identifier=self.__gs_1_id,
        )
        self.__gs_1_ch_1 = db_tools.gs_add_channel(
            self.__gs, self.__band, self.__gs_1_ch_1_id
        )
        if not self.__verbose_testing:
            logging.getLogger('configuration').setLevel(level=logging.CRITICAL)
            logging.getLogger('simulation').setLevel(level=logging.CRITICAL)

    def test_0_add_slots_no_rules(self):
        """services.configuration: add slots without rules
        This method tests the addition of new availability slots to the
        AvailabilitySlots table in the database, when no rule has still been
        defined. Therefore, no slot should be generated or added.
        """
        if self.__verbose_testing:
            print('##### test_add_slots: no rules')

        a_slots = rules.AvailabilityRule.objects.get_availability_slots(
            self.__gs_1_ch_1
        )
        self.assertEqual(
            len(a_slots), 0, 'No new available slots should\'ve been generated.'
        )
        self.assertEqual(
            len(availability.AvailabilitySlot.objects.all()), 0,
            'No AvailabilitySlots expected.'
        )

    def test_1_add_slots_once_rule(self):
        """services.configuration: add slots with a single ONCE rule
        This method tests the addition of new availability slots when there
        is only a single applicable ONCE-type rule in the database.
        Therefore, a single slot should be generated and added to the database.
        """
        if self.__verbose_testing:
            print('##### test_add_slots: single once rule')

        jrpc_rules_if.add_rule(
            self.__gs_1_id, self.__gs_1_ch_1_id,
            db_tools.create_jrpc_once_rule()
        )

        a_slots = rules.AvailabilityRule.objects.get_availability_slots(
            self.__gs_1_ch_1
        )
        self.assertEqual(
            len(a_slots), 1, '1 slot expected, got = ' + str(len(a_slots))
        )
        self.assertEqual(
            len(availability.AvailabilitySlot.objects.all()), 1,
            '1 AvailabilitySlot was expected.'
        )

    def test_2_generate_slots_daily_rule(self):
        """services.configuration: add slots with a DAILY rule
        Tests the generation of slots for a given daily rule.
        """
        if self.__verbose_testing:
            print('##### test_generate_slots_daily_rule')

        utc_dt = datetime.datetime.now(pytz.timezone('UTC'))
        utc_i_date = utc_dt
        utc_e_date = utc_dt + datetime.timedelta(days=365)
        utc_s_time = utc_dt - datetime.timedelta(minutes=15)
        utc_e_time = utc_dt + datetime.timedelta(minutes=15)

        jrpc_rules_if.add_rule(
            self.__gs_1_id, self.__gs_1_ch_1_id,
            db_tools.create_jrpc_daily_rule(
                date_i=utc_i_date,
                date_f=utc_e_date,
                starting_time=utc_s_time,
                ending_time=utc_e_time
            )
        )

        a_slots = rules.AvailabilityRule.objects.get_availability_slots(
            self.__gs_1_ch_1
        )

        self.assertEqual(
            len(a_slots), 3, '3 slots expected, got = ' + str(len(a_slots))
        )
        self.assertEqual(
            len(availability.AvailabilitySlot.objects.all()), 3,
            '3 AvailabilitySlots were expected.'
        )

    def test_3_generate_slots_several_rules_1(self):
        """services.configuration: add slots with several rules
        This method tests the addition of new availability slots when there
        are several availability rules in the database.
        """
        if self.__verbose_testing:
            print('##### test_add_slots: several rules (1)')

        # R1) ADD+ONCE (+1 slot)
        rule_1_id = jrpc_rules_if.add_rule(
            self.__gs_1_id, self.__gs_1_ch_1_id,
            db_tools.create_jrpc_once_rule()
        )
        a_slots = rules.AvailabilityRule.objects.get_availability_slots(
            self.__gs_1_ch_1
        )
        self.assertEqual(
            len(a_slots), 1, 'Only 1 slot expected, got = ' + str(len(a_slots))
        )
        av_slots = availability.AvailabilitySlot.objects.all()
        self.assertEqual(
            len(av_slots), 1, '1 slot expected, got = ' + str(len(av_slots))
        )

        if self.__verbose_testing:
            misc.print_list(
                rules.AvailabilityRule.objects.all(),  name='RULES@1'
            )
            misc.print_list(av_slots, name='AVAILABLE@1')

        # R2) ADD+DAILY (+2 slots)
        rule_2_id = jrpc_rules_if.add_rule(
            self.__gs_1_id, self.__gs_1_ch_1_id,
            db_tools.create_jrpc_daily_rule()
        )

        a_slots = rules.AvailabilityRule.objects.get_availability_slots(
            self.__gs_1_ch_1
        )
        av_slots = availability.AvailabilitySlot.objects.all()

        if self.__verbose_testing:
            print('>>> today_utc = ' + str(misc.get_today_utc()))
            print('>>> window = ' + str(
                simulation.OrbitalSimulator.get_simulation_window()
            ))
            misc.print_list(
                rules.AvailabilityRule.objects.all(),  name='RULES@2'
            )
            misc.print_list(av_slots, name='AVAILABLE@2')

        expected_slots = 2

        self.assertEqual(
            len(a_slots), expected_slots,
            'A_SLOTS, expected ' + str(expected_slots)
            + ', got = ' + str(len(a_slots))
        )
        self.assertEqual(
            len(av_slots), expected_slots,
            'AV_SLOTS, expected ' + str(expected_slots)
            + ', got = ' + str(len(a_slots))
        )

        # R3) ADD-ONCE (-1 slot)
        rule_3_id = jrpc_rules_if.add_rule(
            self.__gs_1_id, self.__gs_1_ch_1_id,
            db_tools.create_jrpc_once_rule(
                operation=jrpc_serial.RULE_OP_REMOVE
            )
        )

        a_slots = rules.AvailabilityRule.objects.get_availability_slots(
            self.__gs_1_ch_1
        )
        av_slots = availability.AvailabilitySlot.objects.all()

        if self.__verbose_testing:
            print('>>> today_utc = ' + str(misc.get_today_utc()))
            print('>>> window = ' + str(
                simulation.OrbitalSimulator.get_simulation_window()
            ))
            misc.print_list(
                rules.AvailabilityRule.objects.all(),  name='RULES@3'
            )
            misc.print_list(av_slots, name='AVAILABLE@3')

        expected_slots = 1

        self.assertEqual(
            len(a_slots), expected_slots,
            'A_SLOTS, expected ' + str(expected_slots)
            + ', got = ' + str(len(a_slots))
        )
        self.assertEqual(
            len(av_slots), expected_slots,
            'AV_SLOTS, expected ' + str(expected_slots)
            + ', got = ' + str(len(a_slots))
        )

        # R4) ADD-DAILY (-7 slots)
        rule_4_id = jrpc_rules_if.add_rule(
            self.__gs_1_id, self.__gs_1_ch_1_id,
            db_tools.create_jrpc_daily_rule(
                operation=jrpc_serial.RULE_OP_REMOVE
            )
        )

        a_slots = rules.AvailabilityRule.objects.get_availability_slots(
            self.__gs_1_ch_1
        )
        av_slots = availability.AvailabilitySlot.objects.all()

        if self.__verbose_testing:
            print('>>> today_utc = ' + str(misc.get_today_utc()))
            print('>>> window = ' + str(
                simulation.OrbitalSimulator.get_simulation_window()
            ))
            misc.print_list(
                rules.AvailabilityRule.objects.all(),  name='RULES@4'
            )
            misc.print_list(av_slots, name='AVAILABLE@4')

        expected = 0

        self.assertEqual(
            len(a_slots), expected,
            'A_SLOTS, expected ' + str(expected)
            + ', got = ' + str(len(a_slots))
        )
        self.assertEqual(
            len(av_slots), expected,
            'AV_SLOTS, expected ' + str(expected)
            + ', got = ' + str(len(a_slots))
        )

        # REMOVE R#4 (+6 slots)
        jrpc_rules_if.remove_rule(
            groundstation_id=self.__gs_1_id,
            channel_id=self.__gs_1_ch_1_id,
            rule_id=rule_4_id
        )

        a_slots = rules.AvailabilityRule.objects.get_availability_slots(
            self.__gs_1_ch_1
        )
        av_slots = availability.AvailabilitySlot.objects.all()

        if self.__verbose_testing:
            print('>>> today_utc = ' + str(misc.get_today_utc()))
            print('>>> window = ' + str(
                simulation.OrbitalSimulator.get_simulation_window()
            ))
            misc.print_list(
                rules.AvailabilityRule.objects.all(),  name='RULES@5'
            )
            misc.print_list(av_slots, name='AVAILABLE@5')

        expected = 1

        self.assertEqual(
            len(a_slots), expected,
            'A_SLOTS, expected ' + str(expected)
            + ', got = ' + str(len(a_slots))
        )
        self.assertEqual(
            len(av_slots), expected,
            'AV_SLOTS, expected ' + str(expected)
            + ', got = ' + str(len(a_slots))
        )

        # REMOVE R#3 (+1 slot)
        jrpc_rules_if.remove_rule(
            groundstation_id=self.__gs_1_id,
            channel_id=self.__gs_1_ch_1_id,
            rule_id=rule_3_id
        )

        a_slots = rules.AvailabilityRule.objects.get_availability_slots(
            self.__gs_1_ch_1
        )
        av_slots = availability.AvailabilitySlot.objects.all()

        if self.__verbose_testing:
            print('>>> today_utc = ' + str(misc.get_today_utc()))
            print('>>> window = ' + str(
                simulation.OrbitalSimulator.get_simulation_window()
            ))
            misc.print_list(
                rules.AvailabilityRule.objects.all(),  name='RULES@6'
            )
            misc.print_list(av_slots, name='AVAILABLE@6')

        expected = 2

        self.assertEqual(
            len(a_slots), expected,
            'A_SLOTS, expected ' + str(expected)
            + ', got = ' + str(len(a_slots))
        )
        self.assertEqual(
            len(av_slots), expected,
            'AV_SLOTS, expected ' + str(expected)
            + ', got = ' + str(len(a_slots))
        )

        # REMOVE R#2 (-7 slots)
        jrpc_rules_if.remove_rule(
            groundstation_id=self.__gs_1_id,
            channel_id=self.__gs_1_ch_1_id,
            rule_id=rule_2_id
        )
        a_slots = rules.AvailabilityRule.objects.get_availability_slots(
            self.__gs_1_ch_1
        )
        self.assertEqual(
            len(a_slots), 1, 'Only 1 slot expected, got = ' + str(len(a_slots))
        )
        av_slots = availability.AvailabilitySlot.objects.all()
        self.assertEqual(
            len(av_slots), 1, '1 slots expected, got = ' + str(len(av_slots))
        )

        if self.__verbose_testing:
            misc.print_list(
                rules.AvailabilityRule.objects.all(),  name='RULES@7'
            )
            misc.print_list(av_slots, name='AVAILABLE@7')

        # REMOVE R#1 (-1 slot)
        jrpc_rules_if.remove_rule(
            groundstation_id=self.__gs_1_id,
            channel_id=self.__gs_1_ch_1_id,
            rule_id=rule_1_id
        )
        a_slots = rules.AvailabilityRule.objects.get_availability_slots(
            self.__gs_1_ch_1
        )
        self.assertEqual(
            len(a_slots), 0, 'None slots expected, got = ' + str(len(a_slots))
        )
        av_slots = availability.AvailabilitySlot.objects.all()
        self.assertEqual(
            len(av_slots), 0, '0 slots expected, got = ' + str(len(av_slots))
        )

        if self.__verbose_testing:
            misc.print_list(
                rules.AvailabilityRule.objects.all(),  name='RULES@8'
            )
            misc.print_list(av_slots, name='AVAILABLE@8')

        self.__verbose_testing = False

    def test_4_get_availability_slots(self):
        """services.configuration: availability slot generation
        Validates the method that gathers the AvailabilitySlots that are
        applicable within a defined interval.
        """
        if self.__verbose_testing:
            print('##### test_get_availability_slots:')

        # 0) Stability with None...
        self.assertEqual(
            availability.AvailabilitySlot.objects.get_applicable(None), [],
            '[] should be the result!'
        )
        # 1) Stability with []...
        self.assertEqual(
            availability.AvailabilitySlot.objects.get_applicable(
                groundstation_channel=self.__gs_1_ch_1,
            ), [],
            '[] should be the result!'
        )

        now = misc.get_now_utc()
        starting_time = now + datetime.timedelta(minutes=30)
        ending_time = now + datetime.timedelta(minutes=45)
        # 2) Single daily rule, adds availability slots...
        jrpc_rules_if.add_rule(
            self.__gs_1_id, self.__gs_1_ch_1_id,
            db_tools.create_jrpc_daily_rule(
                starting_time=starting_time,
                ending_time=ending_time
            )
        )

        a_slots = list(
            availability.AvailabilitySlot.objects.values_list(
                'start', 'end'
            )
        )
        # ### the identifier is included as it is obtained from the actual
        # ### execution of the method
        x_slots = [
            (
                starting_time + datetime.timedelta(days=1),
                ending_time + datetime.timedelta(days=1),
            ),
            (
                starting_time + datetime.timedelta(days=2),
                ending_time + datetime.timedelta(days=2),
            ),
        ]

        if self.__verbose_testing:
            print('>>> window = ' + str(
                simulation.OrbitalSimulator.get_simulation_window()
            ))
            misc.print_list(
                rules.AvailabilityRule.objects.all(),  name='RULES@1'
            )
            misc.print_list(a_slots, name='AVAILABLE@1')

        self.assertEqual(
            a_slots, x_slots, 'Wrong slots! diff = ' + str(datadiff.diff(
                a_slots, x_slots
            ))
        )

        # 3) Period ending in the middle of an AvailabilitySlot, should
        # return the applicable half of that slot...
        start = now + datetime.timedelta(days=1, minutes=25)
        end = now + datetime.timedelta(days=1, minutes=35)

        a_slots = availability.AvailabilitySlot.objects.get_applicable(
            groundstation_channel=self.__gs_1_ch_1,
            start=start,
            end=end
        )
        x_slots = [
            (
                now + datetime.timedelta(days=1, minutes=30),
                now + datetime.timedelta(days=1, minutes=35),
                a_slots[0][2]
            )
        ]

        if self.__verbose_testing:
            print('>>> window = ' + str(
                simulation.OrbitalSimulator.get_simulation_window()
            ))
            misc.print_list(x_slots, name='XSLOTS@2')
            misc.print_list(a_slots, name='AVAILABLE@2')

        self.assertEqual(
            a_slots, x_slots, 'Wrong slots! diff = ' + str(datadiff.diff(
                a_slots, x_slots
            ))
        )

        self.assertEqual(
            a_slots, x_slots,
            'Wrong slots! diff = ' + str(datadiff.diff(a_slots, x_slots))
        )

        # 4) Period starting in the middle of an AvailabilitySlot, should
        # return the applicable half of that slot...
        start = now + datetime.timedelta(days=1, minutes=35)
        end = now + datetime.timedelta(days=1, minutes=50)

        a_slots = availability.AvailabilitySlot.objects.get_applicable(
            groundstation_channel=self.__gs_1_ch_1, start=start, end=end
        )
        x_slots = [(
            (
                now + datetime.timedelta(days=1, minutes=35),
                now + datetime.timedelta(days=1, minutes=45),
                a_slots[0][2]
            )
        )]
        self.assertEqual(
            a_slots, x_slots,
            'Wrong slots! diff = ' + str(datadiff.diff(a_slots, x_slots))
        )

        # 5) Period starting after an AvailabilitySlot, should not return any
        #  slot at all...
        start = now + datetime.timedelta(days=1, minutes=50)
        end = now + datetime.timedelta(days=1, minutes=55)

        a_slots = availability.AvailabilitySlot.objects.get_applicable(
            groundstation_channel=self.__gs_1_ch_1, start=start, end=end
        )
        self.assertEqual(
            a_slots, [],
            'Wrong slots! diff = ' + str(datadiff.diff(a_slots, []))
        )

        # 6) Period starting JUST after an AvailabilitySlot, should not return
        #  any slot at all...
        start = now + datetime.timedelta(days=1, minutes=45)
        end = now + datetime.timedelta(days=1, minutes=55)

        a_slots = availability.AvailabilitySlot.objects.get_applicable(
            groundstation_channel=self.__gs_1_ch_1, start=start, end=end
        )
        self.assertEqual(
            a_slots, [],
            'Wrong slots! diff = ' + str(datadiff.diff(a_slots, []))
        )

        # 7) Period ending after an AvailabilitySlot, should not return any
        #  slot at all...
        start = now + datetime.timedelta(days=1, minutes=10)
        end = now + datetime.timedelta(days=1, minutes=15)

        a_slots = availability.AvailabilitySlot.objects.get_applicable(
            groundstation_channel=self.__gs_1_ch_1, start=start, end=end
        )
        self.assertEqual(
            a_slots, [],
            'Wrong slots! diff = ' + str(datadiff.diff(a_slots, []))
        )

        # 8) Period starting JUST before an AvailabilitySlot, should not return
        #  any slot at all...
        start = now + datetime.timedelta(days=1, minutes=10)
        end = now + datetime.timedelta(days=1, minutes=30)

        a_slots = availability.AvailabilitySlot.objects.get_applicable(
            groundstation_channel=self.__gs_1_ch_1, start=start, end=end
        )
        self.assertEqual(
            a_slots, [],
            'Wrong slots! diff = ' + str(datadiff.diff(a_slots, []))
        )
