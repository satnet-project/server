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

from pytz import utc as pytz_utc
from datetime import date, time, datetime, timedelta
from django.test import TestCase
import logging

from common import misc
from common import testing as db_tools
from configuration.jrpc import rules as jrpc_rules_if,\
    serialization as jrpc_serial
from configuration.models.availability import AvailabilitySlot,\
    AvailabilitySlotsManager
from configuration.models.rules import AvailabilityRule


class TestAvailability(TestCase):

    def setUp(self):

        self.__verbose_testing = False

        if not self.__verbose_testing:
            logging.getLogger('configuration').setLevel(level=logging.CRITICAL)

        self.__gs_1_id = 'gs-castrelos'
        self.__gs_1_ch_1_id = 'chan-cas-1'

        db_tools.init_available()
        self.__band = db_tools.create_band()
        self.__user_profile = db_tools.create_user_profile()
        self.__gs = db_tools.create_gs(
            user_profile=self.__user_profile, identifier=self.__gs_1_id,
        )
        self.__gs_1_ch_1 = db_tools.gs_add_channel(
            self.__gs, self.__band, self.__gs_1_ch_1_id
        )

    def test_add_slots_no_rules(self):
        """
        This method tests the addition of new availability slots to the
        AvailabilitySlots table in the database, when no rule has still been
        defined. Therefore, no slot should be generated or added.
        """
        if self.__verbose_testing:
            print '##### test_add_slots: no rules'

        a_slots = AvailabilityRule.objects.get_availability_slots(
            self.__gs_1_ch_1
        )
        self.assertEquals(
            len(a_slots), 0, 'No new available slots should\'ve been generated.'
        )
        self.assertEquals(
            len(AvailabilitySlot.objects.all()), 0,
            'No AvailabilitySlots expected.'
        )

    def test_add_slots_once_rule(self):
        """
        This method tests the addition of new availability slots when there
        is only a single applicable ONCE-type rule in the database.
        Therefore, a single slot should be generated and added to the database.
        """
        if self.__verbose_testing:
            print '##### test_add_slots: single once rule'

        jrpc_rules_if.add_rule(
            self.__gs_1_id, self.__gs_1_ch_1_id,
            db_tools.create_jrpc_once_rule()
        )

        a_slots = AvailabilityRule.objects.get_availability_slots(
            self.__gs_1_ch_1
        )
        self.assertEquals(
            len(a_slots), 1, '1 slot expected, got = ' + str(len(a_slots))
        )
        self.assertEquals(
            len(AvailabilitySlot.objects.all()), 1,
            '1 AvailabilitySlot was expected.'
        )

    def test_slots_several_rules_1(self):
        """
        This method tests the addition of new availability slots when there
        are several availability rules in the database.
        """
        if self.__verbose_testing:
            print '##### test_add_slots: several rules (1)'

        # R1) ADD+ONCE (+1 slot)
        rule_1_id = jrpc_rules_if.add_rule(
            self.__gs_1_id, self.__gs_1_ch_1_id,
            db_tools.create_jrpc_once_rule()
        )
        a_slots = AvailabilityRule.objects.get_availability_slots(
            self.__gs_1_ch_1
        )
        self.assertEquals(
            len(a_slots), 1, 'Only 1 slot expected, got = ' + str(len(a_slots))
        )
        av_slots = AvailabilitySlot.objects.all()
        self.assertEquals(
            len(av_slots), 1, '1 slot expected, got = ' + str(len(av_slots))
        )

        # R2) ADD+DAILY (+7 slots)
        rule_2_id = jrpc_rules_if.add_rule(
            self.__gs_1_id, self.__gs_1_ch_1_id,
            db_tools.create_jrpc_daily_rule()
        )
        a_slots = AvailabilityRule.objects.get_availability_slots(
            self.__gs_1_ch_1
        )
        self.assertEquals(
            len(a_slots), 7, '7 slots expected, got = ' + str(len(a_slots))
        )
        av_slots = AvailabilitySlot.objects.all()
        self.assertEquals(
            len(av_slots), 7, '7 slots expected, got = ' + str(len(av_slots))
        )

        # R3) ADD-ONCE (-1 slot)
        rule_3_id = jrpc_rules_if.add_rule(
            self.__gs_1_id, self.__gs_1_ch_1_id,
            db_tools.create_jrpc_once_rule(
                operation=jrpc_serial.RULE_OP_REMOVE
            )
        )
        a_slots = AvailabilityRule.objects.get_availability_slots(
            self.__gs_1_ch_1
        )
        self.assertEquals(
            len(a_slots), 6, '6 slots expected, got = ' + str(len(a_slots))
        )
        av_slots = AvailabilitySlot.objects.all()
        self.assertEquals(
            len(av_slots), 6, '6 slots expected, got = ' + str(len(av_slots))
        )

        # R4) ADD-DAILY (-7 slots)
        rule_4_id = jrpc_rules_if.add_rule(
            self.__gs_1_id, self.__gs_1_ch_1_id,
            db_tools.create_jrpc_daily_rule(
                operation=jrpc_serial.RULE_OP_REMOVE
            )
        )
        a_slots = AvailabilityRule.objects.get_availability_slots(
            self.__gs_1_ch_1
        )
        self.assertEquals(
            len(a_slots), 0, '0 slots expected, got = ' + str(len(a_slots))
        )
        av_slots = AvailabilitySlot.objects.all()
        self.assertEquals(
            len(av_slots), 0, '0 slots expected, got = ' + str(len(av_slots))
        )

        # REMOVE R#4 (+6 slots)
        jrpc_rules_if.remove_rule(
            ground_station_id=self.__gs_1_id,
            channel_id=self.__gs_1_ch_1_id,
            rule_id=rule_4_id
        )
        a_slots = AvailabilityRule.objects.get_availability_slots(
            self.__gs_1_ch_1
        )
        self.assertEquals(
            len(a_slots), 6, '6 slots expected, got = ' + str(len(a_slots))
        )
        av_slots = AvailabilitySlot.objects.all()
        self.assertEquals(
            len(av_slots), 6, '6 slots expected, got = ' + str(len(av_slots))
        )

        # REMOVE R#3 (+1 slot)
        jrpc_rules_if.remove_rule(
            ground_station_id=self.__gs_1_id,
            channel_id=self.__gs_1_ch_1_id,
            rule_id=rule_3_id
        )
        a_slots = AvailabilityRule.objects.get_availability_slots(
            self.__gs_1_ch_1
        )
        self.assertEquals(
            len(a_slots), 7, '7 slots expected, got = ' + str(len(a_slots))
        )
        av_slots = AvailabilitySlot.objects.all()
        self.assertEquals(
            len(av_slots), 7, '7 slots expected, got = ' + str(len(av_slots))
        )

        # REMOVE R#2 (-7 slots)
        jrpc_rules_if.remove_rule(
            ground_station_id=self.__gs_1_id,
            channel_id=self.__gs_1_ch_1_id,
            rule_id=rule_2_id
        )
        a_slots = AvailabilityRule.objects.get_availability_slots(
            self.__gs_1_ch_1
        )
        self.assertEquals(
            len(a_slots), 1, 'Only 1 slot expected, got = ' + str(len(a_slots))
        )
        av_slots = AvailabilitySlot.objects.all()
        self.assertEquals(
            len(av_slots), 1, '1 slots expected, got = ' + str(len(av_slots))
        )

        # REMOVE R#1 (-1 slot)
        jrpc_rules_if.remove_rule(
            ground_station_id=self.__gs_1_id,
            channel_id=self.__gs_1_ch_1_id,
            rule_id=rule_1_id
        )
        a_slots = AvailabilityRule.objects.get_availability_slots(
            self.__gs_1_ch_1
        )
        self.assertEquals(
            len(a_slots), 0, 'None slots expected, got = ' + str(len(a_slots))
        )
        av_slots = AvailabilitySlot.objects.all()
        self.assertEquals(
            len(av_slots), 0, '0 slots expected, got = ' + str(len(av_slots))
        )

    def test_get_availability_slots(self):
        """
        Validates the method that gathers the AvailabilitySlots that are
        applicable within a defined interval.
        """
        if self.__verbose_testing:
            print '##### test_get_availability_slots:'

        # 0) Stability with None...
        self.assertEquals(
            AvailabilitySlotsManager.get_availability_slots(None), [],
            '[] should be the result!'
        )

        # 1) Stability with []...
        self.assertEquals(
            AvailabilitySlotsManager.get_availability_slots(
                groundstation_channel=self.__gs_1_ch_1,
            ), [],
            '[] should be the result!'
        )

        # 2) Single daily rule, adds +7 availability slots...
        rule_1_id = jrpc_rules_if.add_rule(
            self.__gs_1_id, self.__gs_1_ch_1_id,
            db_tools.create_jrpc_daily_rule()
        )
        a_slots = AvailabilitySlotsManager.get_availability_slots(
            groundstation_channel=self.__gs_1_ch_1,
            start=misc.get_midnight()+timedelta(days=1),
        )
        x_slots = [(
            pytz_utc.localize(
                datetime.combine(
                    date.today() + timedelta(days=1),
                    time(hour=11, minute=15)
                )
            ),
            pytz_utc.localize(
                datetime.combine(
                    date.today() + timedelta(days=1),
                    time(hour=11, minute=45)
                )
            )
        )]
        self.assertEquals(
            a_slots, x_slots,
            'Wrong slots! expected = ' + misc.list_2_string(x_slots)
            + '\n, actual = ' + misc.list_2_string(a_slots)
        )

        # 3) Period ending in the middle of an AvailabilitySlot, should
        # return the applicable half of that slot...
        a_slots = AvailabilitySlotsManager.get_availability_slots(
            groundstation_channel=self.__gs_1_ch_1,
            start=misc.get_midnight()+timedelta(days=1),
            duration=timedelta(hours=11, minutes=30)
        )
        x_slots = [(
            pytz_utc.localize(
                datetime.combine(
                    date.today() + timedelta(days=1),
                    time(hour=11, minute=15)
                )
            ),
            pytz_utc.localize(
                datetime.combine(
                    date.today() + timedelta(days=1),
                    time(hour=11, minute=30)
                )
            )
        )]
        self.assertEquals(
            a_slots, x_slots,
            'Wrong slots! expected = ' + misc.list_2_string(x_slots)
            + '\n, actual = ' + misc.list_2_string(a_slots)
        )

        # 4) Period starting in the middle of an AvailabilitySlot, should
        # return the applicable half of that slot...
        a_slots = AvailabilitySlotsManager.get_availability_slots(
            groundstation_channel=self.__gs_1_ch_1,
            start=misc.get_midnight()+timedelta(days=1, hours=11, minutes=30),
            duration=timedelta(hours=4)
        )
        x_slots = [(
            pytz_utc.localize(
                datetime.combine(
                    date.today() + timedelta(days=1),
                    time(hour=11, minute=30)
                )
            ),
            pytz_utc.localize(
                datetime.combine(
                    date.today() + timedelta(days=1),
                    time(hour=11, minute=45)
                )
            )
        )]
        self.assertEquals(
            a_slots, x_slots,
            'Wrong slots! expected = ' + misc.list_2_string(x_slots)
            + '\n, actual = ' + misc.list_2_string(a_slots)
        )

        # 5) Period starting after an AvailabilitySlot, should not return any
        #  slot at all...
        a_slots = AvailabilitySlotsManager.get_availability_slots(
            groundstation_channel=self.__gs_1_ch_1,
            start=misc.get_midnight()+timedelta(days=1, hours=11, minutes=46),
            duration=timedelta(hours=3)
        )
        self.assertEquals(
            a_slots, [],
            'Wrong slots! expected = ' + misc.list_2_string([])
            + '\n, actual = ' + misc.list_2_string(a_slots)
        )

        # 6) Period starting JUST after an AvailabilitySlot, should not return
        #  any slot at all...
        a_slots = AvailabilitySlotsManager.get_availability_slots(
            groundstation_channel=self.__gs_1_ch_1,
            start=misc.get_midnight()+timedelta(days=1, hours=11, minutes=45),
            duration=timedelta(hours=3)
        )
        self.assertEquals(
            a_slots, [],
            'Wrong slots! expected = ' + misc.list_2_string([])
            + '\n, actual = ' + misc.list_2_string(a_slots)
        )

        # 7) Period ending after an AvailabilitySlot, should not return any
        #  slot at all...
        a_slots = AvailabilitySlotsManager.get_availability_slots(
            groundstation_channel=self.__gs_1_ch_1,
            start=misc.get_midnight()+timedelta(days=1, hours=7, minutes=00),
            duration=timedelta(hours=3)
        )
        self.assertEquals(
            a_slots, [],
            'Wrong slots! expected = ' + misc.list_2_string([])
            + '\n, actual = ' + misc.list_2_string(a_slots)
        )

        # 8) Period starting JUST before an AvailabilitySlot, should not return
        #  any slot at all...
        a_slots = AvailabilitySlotsManager.get_availability_slots(
            groundstation_channel=self.__gs_1_ch_1,
            start=misc.get_midnight()+timedelta(days=1, hours=8, minutes=15),
            duration=timedelta(hours=3)
        )
        self.assertEquals(
            a_slots, [],
            'Wrong slots! expected = ' + misc.list_2_string([])
            + '\n, actual = ' + misc.list_2_string(a_slots)
        )