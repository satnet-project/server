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

import datadiff
import datetime
import logging
from django import test
from django.db import models

from common import testing as db_tools, misc
from configuration import signals
from configuration.jrpc import channels as jrpc_chs
from configuration.jrpc import rules as jrpc_rules
from configuration.jrpc import serialization as jrp_cfg_serial
from scheduling.jrpc import spacecraft as jrpc_sc_scheduling
from scheduling.jrpc import groundstations as jrpc_gs_scheduling
from scheduling.models import operational


class JRPCSpacecraftSchedulingTest(test.TestCase):

    def setUp(self):
        """
        This method populates the database with some information to be used
        only for this test.
        """
        self.__verbose_testing = False

        if not self.__verbose_testing:
            logging.getLogger('configuration').setLevel(level=logging.CRITICAL)
            logging.getLogger('scheduling').setLevel(level=logging.CRITICAL)

        self.__sc_1_id = 'xatcobeo-sc'
        self.__sc_1_tle_id = 'XATCOBEO'
        self.__sc_1_ch_1_id = 'xatcobeo-fm'
        self.__sc_1_ch_1_cfg = {
            jrp_cfg_serial.FREQUENCY_K: '437000000',
            jrp_cfg_serial.MODULATION_K: 'FM',
            jrp_cfg_serial.POLARIZATION_K: 'LHCP',
            jrp_cfg_serial.BITRATE_K: '300',
            jrp_cfg_serial.BANDWIDTH_K: '12.500000000'
        }
        self.__gs_1_id = 'gs-la'
        self.__gs_1_ch_1_id = 'gs-la-fm'
        self.__gs_1_ch_1_cfg = {
            jrp_cfg_serial.BAND_K:
            'UHF / U / 435000000.000000 / 438000000.000000',
            jrp_cfg_serial.MODULATIONS_K: ['FM'],
            jrp_cfg_serial.POLARIZATIONS_K: ['LHCP'],
            jrp_cfg_serial.BITRATES_K: [300, 600, 900],
            jrp_cfg_serial.BANDWIDTHS_K: [12.500000000, 25.000000000]
        }
        self.__gs_1_ch_2_id = 'gs-la-fm-2'
        self.__gs_1_ch_2_cfg = {
            jrp_cfg_serial.BAND_K:
            'UHF / U / 435000000.000000 / 438000000.000000',
            jrp_cfg_serial.MODULATIONS_K: ['FM'],
            jrp_cfg_serial.POLARIZATIONS_K: ['LHCP'],
            jrp_cfg_serial.BITRATES_K: [300, 600, 900],
            jrp_cfg_serial.BANDWIDTHS_K: [12.500000000, 25.000000000]
        }

        signals.connect_availability_2_operational()
        signals.connect_channels_2_compatibility()
        signals.connect_compatibility_2_operational()
        signals.connect_rules_2_availability()
        signals.connect_segments_2_booking_tle()

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
        operational.OperationalSlot.objects.get_simulator().set_debug()
        operational.OperationalSlot.objects.set_debug()

    def test_sc_get_operational_slots(self):
        """
        Validates the JRPC method <sc_get_operational_slots>
        """
        if self.__verbose_testing:
            print '##### test_sc_get_operational_slots'
        operational.OperationalSlot.objects.reset_ids_counter()

        # 1) non-existant Spacecraft
        self.assertRaises(
            models.ObjectDoesNotExist,
            jrpc_sc_scheduling.get_operational_slots,
            0
        )

        # 2) basic test, should not generate slots until the GS is added,
        # raising an exception to confirm it
        self.assertEquals(
            jrpc_chs.sc_channel_create(
                spacecraft_id=self.__sc_1_id,
                channel_id=self.__sc_1_ch_1_id,
                configuration=self.__sc_1_ch_1_cfg
            ), True, 'Channel should have been created!'
        )
        self.assertRaises(
            Exception,
            jrpc_sc_scheduling.get_operational_slots,
            self.__sc_1_ch_1_id
        )

        # 3) basic test, should generate 2 FREE slots
        self.assertEquals(
            jrpc_chs.gs_channel_create(
                ground_station_id=self.__gs_1_id,
                channel_id=self.__gs_1_ch_1_id,
                configuration=self.__gs_1_ch_1_cfg
            ), True, 'Channel should have been created!'
        )

        date_i = misc.get_today_utc() + datetime.timedelta(days=1)
        date_f = misc.get_today_utc() + datetime.timedelta(days=366)

        now = misc.get_now_utc()
        s_time = now + datetime.timedelta(minutes=30)
        e_time = now + datetime.timedelta(minutes=45)

        jrpc_rules.add_rule(
            self.__gs_1_id, self.__gs_1_ch_1_id,
            db_tools.create_jrpc_daily_rule(
                date_i=date_i,
                date_f=date_f,
                starting_time=s_time,
                ending_time=e_time
            )
        )

        actual = jrpc_sc_scheduling.get_operational_slots(self.__sc_1_id)
        expected = [
            {
                operational.SLOT_IDENTIFIER: '1',
                operational.GROUNDSTATION_CHANNEL: self.__gs_1_ch_1_id,
                operational.SPACECRAFT_CHANNEL: self.__sc_1_ch_1_id,
                operational.STATE: operational.STATE_FREE,
                operational.DATE_START: s_time.isoformat(),
                operational.DATE_END: e_time.isoformat()
            },
            {
                operational.SLOT_IDENTIFIER: '2',
                operational.GROUNDSTATION_CHANNEL: self.__gs_1_ch_1_id,
                operational.SPACECRAFT_CHANNEL: self.__sc_1_ch_1_id,
                operational.STATE: operational.STATE_FREE,
                operational.DATE_START: (
                    s_time + datetime.timedelta(days=1)
                ).isoformat(),
                operational.DATE_END: (
                    e_time + datetime.timedelta(days=1)
                ).isoformat()
            },
            {
                operational.SLOT_IDENTIFIER: '3',
                operational.GROUNDSTATION_CHANNEL: self.__gs_1_ch_1_id,
                operational.SPACECRAFT_CHANNEL: self.__sc_1_ch_1_id,
                operational.STATE: operational.STATE_FREE,
                operational.DATE_START: (
                    s_time + datetime.timedelta(days=2)
                ).isoformat(),
                operational.DATE_END: (
                    e_time + datetime.timedelta(days=2)
                ).isoformat()
            },
        ]
        self.assertEquals(
            actual, expected,
            'Expected different slots!, diff = ' + str(datadiff.diff(
                actual, expected
            ))
        )

        # ### clean up
        self.assertEquals(
            jrpc_chs.gs_channel_delete(
                groundstation_id=self.__gs_1_id, channel_id=self.__gs_1_ch_1_id
            ),
            True,
            'Could not delete GroundStationChannel = ' + str(
                self.__gs_1_ch_1_id
            )
        )
        self.assertEquals(
            jrpc_chs.sc_channel_delete(
                spacecraft_id=self.__sc_1_id, channel_id=self.__sc_1_ch_1_id
            ),
            True,
            'Could not delete SpacecraftChannel = ' + str(self.__sc_1_ch_1_id)
        )

    def test_sc_get_changes(self):
        """
        Validates the JRPC method <sc_get_changes>.
        """
        if self.__verbose_testing:
            print '##### test_sc_get_changes'
        operational.OperationalSlot.objects.reset_ids_counter()

        # 1) non-existant Spacecraft
        self.assertRaises(
            models.ObjectDoesNotExist, jrpc_sc_scheduling.get_changes, 0
        )
        # 2) Non slots available for the given spacecraft
        self.assertRaises(
            Exception, jrpc_sc_scheduling.get_changes, self.__sc_1_id
        )

        # ### channels required for the tests
        self.assertEquals(
            jrpc_chs.sc_channel_create(
                spacecraft_id=self.__sc_1_id,
                channel_id=self.__sc_1_ch_1_id,
                configuration=self.__sc_1_ch_1_cfg
            ), True, 'Channel should have been created!'
        )
        self.assertEquals(
            jrpc_chs.gs_channel_create(
                ground_station_id=self.__gs_1_id,
                channel_id=self.__gs_1_ch_1_id,
                configuration=self.__gs_1_ch_1_cfg
            ), True, 'Channel should have been created!'
        )

        # 3) we add some slots and they should be retrieved as 'changed' only
        #  once.
        date_i = misc.get_today_utc() + datetime.timedelta(days=1)
        date_f = misc.get_today_utc() + datetime.timedelta(days=366)

        now = misc.get_now_utc()
        s_time = now + datetime.timedelta(minutes=30)
        e_time = now + datetime.timedelta(minutes=45)

        jrpc_rules.add_rule(
            self.__gs_1_id, self.__gs_1_ch_1_id,
            db_tools.create_jrpc_daily_rule(
                date_i=date_i,
                date_f=date_f,
                starting_time=s_time,
                ending_time=e_time
            )
        )

        actual = jrpc_sc_scheduling.get_changes(self.__sc_1_id)
        expected = [
            {
                operational.SLOT_IDENTIFIER: '1',
                operational.GROUNDSTATION_CHANNEL: self.__gs_1_ch_1_id,
                operational.SPACECRAFT_CHANNEL: self.__sc_1_ch_1_id,
                operational.STATE: operational.STATE_FREE,
                operational.DATE_START: s_time.isoformat(),
                operational.DATE_END: e_time.isoformat()
            },
            {
                operational.SLOT_IDENTIFIER: '2',
                operational.GROUNDSTATION_CHANNEL: self.__gs_1_ch_1_id,
                operational.SPACECRAFT_CHANNEL: self.__sc_1_ch_1_id,
                operational.STATE: operational.STATE_FREE,
                operational.DATE_START: (
                    s_time + datetime.timedelta(days=1)
                ).isoformat(),
                operational.DATE_END: (
                    e_time + datetime.timedelta(days=1)
                ).isoformat()
            },
            {
                operational.SLOT_IDENTIFIER: '3',
                operational.GROUNDSTATION_CHANNEL: self.__gs_1_ch_1_id,
                operational.SPACECRAFT_CHANNEL: self.__sc_1_ch_1_id,
                operational.STATE: operational.STATE_FREE,
                operational.DATE_START: (
                    s_time + datetime.timedelta(days=2)
                ).isoformat(),
                operational.DATE_END: (
                    e_time + datetime.timedelta(days=2)
                ).isoformat()
            },
        ]
        self.assertEquals(
            actual, expected,
            'Expected different slots!, diff = ' + str(datadiff.diff(
                actual, expected
            ))
        )

        # 4) the second call asking for changes must return no slots
        self.assertRaises(
            Exception,
            jrpc_sc_scheduling.get_changes,
            self.__sc_1_id
        )

        # 5) we add some slots and they should be retrieved as 'changed' only
        #  once.
        date_i = misc.get_today_utc() + datetime.timedelta(days=1)
        date_f = misc.get_today_utc() + datetime.timedelta(days=366)

        now = misc.get_now_utc()
        s_time = now + datetime.timedelta(minutes=15)
        e_time = now + datetime.timedelta(minutes=20)

        jrpc_rules.add_rule(
            self.__gs_1_id, self.__gs_1_ch_1_id,
            db_tools.create_jrpc_daily_rule(
                date_i=date_i,
                date_f=date_f,
                starting_time=s_time,
                ending_time=e_time
            )
        )

        actual = jrpc_sc_scheduling.get_changes(self.__sc_1_id)
        expected = [
            {
                operational.SLOT_IDENTIFIER: '4',
                operational.GROUNDSTATION_CHANNEL: self.__gs_1_ch_1_id,
                operational.SPACECRAFT_CHANNEL: self.__sc_1_ch_1_id,
                operational.STATE: operational.STATE_FREE,
                operational.DATE_START: s_time.isoformat(),
                operational.DATE_END: e_time.isoformat()
            },
            {
                operational.SLOT_IDENTIFIER: '5',
                operational.GROUNDSTATION_CHANNEL: self.__gs_1_ch_1_id,
                operational.SPACECRAFT_CHANNEL: self.__sc_1_ch_1_id,
                operational.STATE: operational.STATE_FREE,
                operational.DATE_START: (
                    s_time + datetime.timedelta(days=1)
                ).isoformat(),
                operational.DATE_END: (
                    e_time + datetime.timedelta(days=1)
                ).isoformat()
            },
            {
                operational.SLOT_IDENTIFIER: '6',
                operational.GROUNDSTATION_CHANNEL: self.__gs_1_ch_1_id,
                operational.SPACECRAFT_CHANNEL: self.__sc_1_ch_1_id,
                operational.STATE: operational.STATE_FREE,
                operational.DATE_START: (
                    s_time + datetime.timedelta(days=2)
                ).isoformat(),
                operational.DATE_END: (
                    e_time + datetime.timedelta(days=2)
                ).isoformat()
            },
        ]
        self.assertEquals(
            actual, expected,
            'Expected different slots!, diff = ' + str(datadiff.diff(
                actual, expected
            ))
        )

        # ### clean up sc/gs
        self.assertEquals(
            jrpc_chs.gs_channel_delete(
                groundstation_id=self.__gs_1_id, channel_id=self.__gs_1_ch_1_id
            ),
            True,
            'Could not delete GroundStationChannel = ' + str(
                self.__gs_1_ch_1_id
            )
        )
        self.assertEquals(
            jrpc_chs.sc_channel_delete(
                spacecraft_id=self.__sc_1_id, channel_id=self.__sc_1_ch_1_id
            ),
            True,
            'Could not delete SpacecraftChannel = ' + str(self.__sc_1_ch_1_id)
        )

    def test_sc_select_slots(self):
        """
        Validates the method for the selection of the slots.
        """
        if self.__verbose_testing:
            print '##### test_sc_get_changes'
        operational.OperationalSlot.objects.reset_ids_counter()

        # ### channels required for the tests
        self.assertEquals(
            jrpc_chs.sc_channel_create(
                spacecraft_id=self.__sc_1_id,
                channel_id=self.__sc_1_ch_1_id,
                configuration=self.__sc_1_ch_1_cfg
            ), True, 'Channel should have been created!'
        )
        self.assertEquals(
            jrpc_chs.gs_channel_create(
                ground_station_id=self.__gs_1_id,
                channel_id=self.__gs_1_ch_1_id,
                configuration=self.__gs_1_ch_1_cfg
            ), True, 'Channel should have been created!'
        )

        date_i = misc.get_today_utc() + datetime.timedelta(days=1)
        date_f = misc.get_today_utc() + datetime.timedelta(days=366)
        now = misc.get_now_utc()
        s_time = now + datetime.timedelta(minutes=30)
        e_time = now + datetime.timedelta(minutes=45)

        jrpc_rules.add_rule(
            self.__gs_1_id, self.__gs_1_ch_1_id,
            db_tools.create_jrpc_daily_rule(
                date_i=date_i,
                date_f=date_f,
                starting_time=s_time,
                ending_time=e_time
            )
        )

        # 1) select all the slots and retrieve the changes
        actual = jrpc_sc_scheduling.get_changes(self.__sc_1_id)
        id_list = db_tools.create_identifier_list(actual)
        actual = jrpc_sc_scheduling.select_slots(
            self.__sc_1_id, id_list
        )
        expected = [
            {
                operational.SLOT_IDENTIFIER: '1',
                operational.GROUNDSTATION_CHANNEL: self.__gs_1_ch_1_id,
                operational.SPACECRAFT_CHANNEL: self.__sc_1_ch_1_id,
                operational.STATE: operational.STATE_SELECTED,
                operational.DATE_START: s_time.isoformat(),
                operational.DATE_END: e_time.isoformat()
            },
            {
                operational.SLOT_IDENTIFIER: '2',
                operational.GROUNDSTATION_CHANNEL: self.__gs_1_ch_1_id,
                operational.SPACECRAFT_CHANNEL: self.__sc_1_ch_1_id,
                operational.STATE: operational.STATE_SELECTED,
                operational.DATE_START: (
                    s_time + datetime.timedelta(days=1)
                ).isoformat(),
                operational.DATE_END: (
                    e_time + datetime.timedelta(days=1)
                ).isoformat()
            },
            {
                operational.SLOT_IDENTIFIER: '3',
                operational.GROUNDSTATION_CHANNEL: self.__gs_1_ch_1_id,
                operational.SPACECRAFT_CHANNEL: self.__sc_1_ch_1_id,
                operational.STATE: operational.STATE_SELECTED,
                operational.DATE_START: (
                    s_time + datetime.timedelta(days=2)
                ).isoformat(),
                operational.DATE_END: (
                    e_time + datetime.timedelta(days=2)
                ).isoformat()
            },
        ]
        self.assertEquals(
            actual, expected,
            'Expected different slots!, diff = ' + str(datadiff.diff(
                actual, expected
            ))
        )

        # 2) The changes should be notified now to the compatible gs
        actual = jrpc_gs_scheduling.get_changes(self.__gs_1_id)
        self.assertEquals(
            actual, expected,
            'Expected different slots!, diff = ' + str(datadiff.diff(
                actual, expected
            ))
        )
        actual = jrpc_sc_scheduling.get_changes(self.__sc_1_id)
        self.assertEquals(
            actual, expected,
            'Expected different slots!, diff = ' + str(datadiff.diff(
                actual, expected
            ))
        )

        # 3) Not notified again!
        self.assertRaises(
            Exception, jrpc_sc_scheduling.get_changes, self.__sc_1_id
        )
        self.assertRaises(
            Exception, jrpc_gs_scheduling.get_changes, self.__gs_1_id
        )

        # ### clean up sc/gs
        self.assertEquals(
            jrpc_chs.gs_channel_delete(
                groundstation_id=self.__gs_1_id, channel_id=self.__gs_1_ch_1_id
            ),
            True,
            'Could not delete GroundStationChannel = ' + str(
                self.__gs_1_ch_1_id
            )
        )
        self.assertEquals(
            jrpc_chs.sc_channel_delete(
                spacecraft_id=self.__sc_1_id, channel_id=self.__sc_1_ch_1_id
            ),
            True,
            'Could not delete SpacecraftChannel = ' + str(self.__sc_1_ch_1_id)
        )