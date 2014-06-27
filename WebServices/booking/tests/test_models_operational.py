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

import logging
import datetime
from django import test

from booking.models import operational
from common import testing as db_tools, misc
from configuration import signals
from configuration.jrpc import channels, rules, serialization


class JRPCRulesTest(test.TestCase):

    def setUp(self):
        """
        This method populates the database with some information to be used
        only for this test.
        """
        self.__verbose_testing = False

        if not self.__verbose_testing:
            logging.getLogger('configuration').setLevel(level=logging.CRITICAL)
            logging.getLogger('booking').setLevel(level=logging.CRITICAL)

        self.__sc_1_id = 'xatcobeo-sc'
        self.__sc_1_tle_id = 'XATCOBEO'
        self.__sc_1_ch_1_id = 'xatcobeo-fm'
        self.__sc_1_ch_1_cfg = {
            serialization.FREQUENCY_K: '437000000',
            serialization.MODULATION_K: 'FM',
            serialization.POLARIZATION_K: 'LHCP',
            serialization.BITRATE_K: '300',
            serialization.BANDWIDTH_K: '12.500000000'
        }
        self.__gs_1_id = 'gs-la'
        self.__gs_1_ch_1_id = 'gs-la-fm'
        self.__gs_1_ch_1_cfg = {
            serialization.BAND_K:
            'UHF / U / 435000000.000000 / 438000000.000000',
            serialization.MODULATIONS_K: ['FM'],
            serialization.POLARIZATIONS_K: ['LHCP'],
            serialization.BITRATES_K: [300, 600, 900],
            serialization.BANDWIDTHS_K: [12.500000000, 25.000000000]
        }

        signals.connect_channels_2_compatibility()
        signals.connect_segments_2_booking_tle()
        signals.connect_availability_2_operational()
        signals.connect_compatibility_2_operational()

        db_tools.init_available()
        db_tools.init_tles_database()
        self.__band = db_tools.create_band()
        self.__user_profile = db_tools.create_user_profile()
        self.__sc_1 = db_tools.create_sc(
            user_profile=self.__user_profile,
            identifier=self.__sc_1_id,
            tle_id=self.__sc_1_tle_id,
        )
        self.__gs_1 = db_tools.create_gs(
            user_profile=self.__user_profile, identifier=self.__gs_1_id,
        )

    def test_operational_case_1(self):
        """
        Validates the update of the OperationalSlots table. In this first
        test, the adding sequence is:

        1) +GS_CH
        2) +SC_CH
        3) +RULE
        4) -RULE
        5) -SC_CH
        6) -GS_CH

        OperationalSlots should be available only in bewteen steps 3 and 4.
        """
        if self.__verbose_testing:
            print '##### test_add_slots: no rules'

        self.assertEquals(
            channels.gs_channel_create(
                ground_station_id=self.__gs_1_id,
                channel_id=self.__gs_1_ch_1_id,
                configuration=self.__gs_1_ch_1_cfg
            ), True, 'Channel should have been created!'
        )

        self.assertEquals(
            channels.sc_channel_create(
                spacecraft_id=self.__sc_1_id,
                channel_id=self.__sc_1_ch_1_id,
                configuration=self.__sc_1_ch_1_cfg
            ), True, 'Channel should have been created!'
        )

        r_1_id = rules.add_rule(
            self.__gs_1_id, self.__gs_1_ch_1_id,
            db_tools.create_jrpc_daily_rule(
                starting_time=misc.localize_time_utc(datetime.time(
                    hour=8, minute=0, second=0
                )),
                ending_time=misc.localize_time_utc(datetime.time(
                    hour=23, minute=55, second=0
                ))
            )
        )
        self.assertIsNot(r_1_id, 0, 'Rule should have been added!')
        self.assertIsNot(
            len(operational.OperationalSlot.objects.all()), 0,
            'Operational slots must be available!'
        )

        self.assertIsNot(
            rules.remove_rule(self.__gs_1_id, self.__gs_1_ch_1_id, r_1_id),
            0, 'Rule should have been added!'
        )
        self.assertEqual(
            len(operational.OperationalSlot.objects.all()), 0,
            'No operational slots must remain available!'
        )

        db_tools.remove_sc_channel(self.__sc_1_ch_1_id)
        db_tools.remove_gs_channel(self.__gs_1_id, self.__gs_1_ch_1_id)

    def test_operational_case_2(self):
        """
        Validates the update of the OperationalSlots table. In this first
        test, the adding sequence is:

        1) +SC_CH
        2) +GS_CH
        3) +RULE
        4) -RULE
        5) -SC_CH
        6) -GS_CH

        OperationalSlots should be available only in bewteen steps 3 and 4.
        """
        if self.__verbose_testing:
            print '##### test_add_slots: no rules'

        self.assertEquals(
            channels.sc_channel_create(
                spacecraft_id=self.__sc_1_id,
                channel_id=self.__sc_1_ch_1_id,
                configuration=self.__sc_1_ch_1_cfg
            ), True, 'Channel should have been created!'
        )

        self.assertEquals(
            channels.gs_channel_create(
                ground_station_id=self.__gs_1_id,
                channel_id=self.__gs_1_ch_1_id,
                configuration=self.__gs_1_ch_1_cfg
            ), True, 'Channel should have been created!'
        )

        r_1_id = rules.add_rule(
            self.__gs_1_id, self.__gs_1_ch_1_id,
            db_tools.create_jrpc_daily_rule(
                starting_time=misc.localize_time_utc(datetime.time(
                    hour=8, minute=0, second=0
                )),
                ending_time=misc.localize_time_utc(datetime.time(
                    hour=23, minute=55, second=0
                ))
            )
        )
        self.assertIsNot(r_1_id, 0, 'Rule should have been added!')
        self.assertIsNot(
            len(operational.OperationalSlot.objects.all()), 0,
            'Operational slots must be available!'
        )

        self.assertIsNot(
            rules.remove_rule(self.__gs_1_id, self.__gs_1_ch_1_id, r_1_id),
            0, 'Rule should have been added!'
        )
        self.assertEqual(
            len(operational.OperationalSlot.objects.all()), 0,
            'No operational slots must remain available!'
        )

        db_tools.remove_sc_channel(self.__sc_1_ch_1_id)
        db_tools.remove_gs_channel(self.__gs_1_id, self.__gs_1_ch_1_id)

    def test_operational_case_3(self):
        """
        Validates the update of the OperationalSlots table. In this first
        test, the adding sequence is:

        1) +SC_CH
        2) +GS_CH
        3) +RULE
        4) -RULE
        5) -GS_CH
        6) -SC_CH

        OperationalSlots should be available only in bewteen steps 3 and 4.
        """
        if self.__verbose_testing:
            print '##### test_add_slots: no rules'

        self.assertEquals(
            channels.sc_channel_create(
                spacecraft_id=self.__sc_1_id,
                channel_id=self.__sc_1_ch_1_id,
                configuration=self.__sc_1_ch_1_cfg
            ), True, 'Channel should have been created!'
        )

        self.assertEquals(
            channels.gs_channel_create(
                ground_station_id=self.__gs_1_id,
                channel_id=self.__gs_1_ch_1_id,
                configuration=self.__gs_1_ch_1_cfg
            ), True, 'Channel should have been created!'
        )

        r_1_id = rules.add_rule(
            self.__gs_1_id, self.__gs_1_ch_1_id,
            db_tools.create_jrpc_daily_rule(
                starting_time=misc.localize_time_utc(datetime.time(
                    hour=8, minute=0, second=0
                )),
                ending_time=misc.localize_time_utc(datetime.time(
                    hour=23, minute=55, second=0
                ))
            )
        )

        self.assertIsNot(r_1_id, 0, 'Rule should have been added!')
        self.assertIsNot(
            len(operational.OperationalSlot.objects.all()), 0,
            'Operational slots must be available!'
        )

        self.assertIsNot(
            rules.remove_rule(self.__gs_1_id, self.__gs_1_ch_1_id, r_1_id),
            0, 'Rule should have been added!'
        )
        self.assertEqual(
            len(operational.OperationalSlot.objects.all()), 0,
            'No operational slots must remain available!'
        )

        db_tools.remove_gs_channel(self.__gs_1_id, self.__gs_1_ch_1_id)
        db_tools.remove_sc_channel(self.__sc_1_ch_1_id)

    def test_operational_case_4(self):
        """
        Validates the update of the OperationalSlots table. In this first
        test, the adding sequence is:

        1) +GS_CH
        2) +RULE
        3) +SC_CH
        4) -RULE
        5) -GS_CH
        6) -SC_CH

        OperationalSlots should be available only in bewteen steps 3 and 4.
        """
        if self.__verbose_testing:
            print '##### test_add_slots: no rules'

        self.assertEquals(
            channels.gs_channel_create(
                ground_station_id=self.__gs_1_id,
                channel_id=self.__gs_1_ch_1_id,
                configuration=self.__gs_1_ch_1_cfg
            ), True, 'Channel should have been created!'
        )

        r_1_id = rules.add_rule(
            self.__gs_1_id, self.__gs_1_ch_1_id,
            db_tools.create_jrpc_daily_rule(
                starting_time=misc.localize_time_utc(datetime.time(
                    hour=8, minute=0, second=0
                )),
                ending_time=misc.localize_time_utc(datetime.time(
                    hour=23, minute=55, second=0
                ))
            )
        )

        self.assertEquals(
            channels.sc_channel_create(
                spacecraft_id=self.__sc_1_id,
                channel_id=self.__sc_1_ch_1_id,
                configuration=self.__sc_1_ch_1_cfg
            ), True, 'Channel should have been created!'
        )
        self.assertIsNot(
            len(operational.OperationalSlot.objects.all()), 0,
            'Operational slots must be available!'
        )

        self.assertIsNot(r_1_id, 0, 'Rule should have been added!')
        self.assertIsNot(
            rules.remove_rule(self.__gs_1_id, self.__gs_1_ch_1_id, r_1_id),
            False, 'Rule should have been removed!'
        )

        self.assertEqual(
            len(operational.OperationalSlot.objects.all()), 0,
            'No operational slots must remain available!'
        )

        db_tools.remove_gs_channel(self.__gs_1_id, self.__gs_1_ch_1_id)
        db_tools.remove_sc_channel(self.__sc_1_ch_1_id)

    def test_operational_case_5(self):
        """
        Validates the update of the OperationalSlots table. In this first
        test, the adding sequence is:

        1) +GS_CH
        2) +RULE
        3) +SC_CH
        4) -RULE
        5) -SC_CH
        6) -GS_CH

        OperationalSlots should be available only in bewteen steps 3 and 4.
        """
        if self.__verbose_testing:
            print '##### test_add_slots: no rules'

        self.assertEquals(
            channels.gs_channel_create(
                ground_station_id=self.__gs_1_id,
                channel_id=self.__gs_1_ch_1_id,
                configuration=self.__gs_1_ch_1_cfg
            ), True, 'Channel should have been created!'
        )

        r_1_id = rules.add_rule(
            self.__gs_1_id, self.__gs_1_ch_1_id,
            db_tools.create_jrpc_daily_rule(
                starting_time=misc.localize_time_utc(datetime.time(
                    hour=8, minute=0, second=0
                )),
                ending_time=misc.localize_time_utc(datetime.time(
                    hour=23, minute=55, second=0
                ))
            )
        )

        self.assertEquals(
            channels.sc_channel_create(
                spacecraft_id=self.__sc_1_id,
                channel_id=self.__sc_1_ch_1_id,
                configuration=self.__sc_1_ch_1_cfg
            ), True, 'Channel should have been created!'
        )
        self.assertIsNot(
            len(operational.OperationalSlot.objects.all()), 0,
            'Operational slots must be available!'
        )

        self.assertIsNot(r_1_id, 0, 'Rule should have been added!')
        self.assertIsNot(
            rules.remove_rule(self.__gs_1_id, self.__gs_1_ch_1_id, r_1_id),
            False, 'Rule should have been removed!'
        )

        self.assertEqual(
            len(operational.OperationalSlot.objects.all()), 0,
            'No operational slots must remain available!'
        )

        db_tools.remove_sc_channel(self.__sc_1_ch_1_id)
        db_tools.remove_gs_channel(self.__gs_1_id, self.__gs_1_ch_1_id)
