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
from django.db import models

from services.common import misc
from services.common.testing import helpers as db_tools
from services.configuration.jrpc.serializers import \
    channels as channel_serializers
from services.configuration.jrpc.serializers import \
    segments as segment_serializers
from services.configuration.jrpc.views.channels import \
    groundstations as jrpc_gs_chs
from services.configuration.jrpc.views.channels import \
    spacecraft as jrpc_sc_chs
from services.configuration.jrpc.views import rules as jrpc_rules
from services.scheduling.models import operational as operational_models
from services.scheduling.jrpc.views.operational import \
    spacecraft as jrpc_sc_scheduling
from services.scheduling.jrpc.serializers import operational as \
    jrpc_sch_serial


class JRPCSpacecraftSchedulingTest(test.TestCase):

    def setUp(self):
        """
        This method populates the database with some information to be used
        only for this test.
        """
        self.__verbose_testing = False

        if not self.__verbose_testing:
            logging.getLogger('common').setLevel(level=logging.CRITICAL)
            logging.getLogger('configuration').setLevel(level=logging.CRITICAL)
            logging.getLogger('scheduling').setLevel(level=logging.CRITICAL)

        # noinspection PyUnresolvedReferences
        from services.scheduling.signals import availability

        self.__sc_1_id = 'xatcobeo-sc'
        self.__sc_1_tle_id = 'HUMSAT-D'
        self.__sc_1_ch_1_id = str('xatcobeo-fm')
        self.__sc_1_ch_1_cfg = {
            channel_serializers.FREQUENCY_K: '437000000',
            channel_serializers.MODULATION_K: 'FM',
            channel_serializers.POLARIZATION_K: 'LHCP',
            channel_serializers.BITRATE_K: '300',
            channel_serializers.BANDWIDTH_K: '12.500000000'
        }
        self.__gs_1_id = 'gs-la'
        self.__gs_1_ch_1_id = str('gs-la-fm')
        self.__gs_1_ch_1_cfg = {
            channel_serializers.BAND_K:
            'UHF / U / 435000000.000000 / 438000000.000000',
            channel_serializers.AUTOMATED_K: False,
            channel_serializers.MODULATIONS_K: ['FM'],
            channel_serializers.POLARIZATIONS_K: ['LHCP'],
            channel_serializers.BITRATES_K: [300, 600, 900],
            channel_serializers.BANDWIDTHS_K: [12.500000000, 25.000000000]
        }
        self.__gs_1_ch_2_id = 'gs-la-fm-2'
        self.__gs_1_ch_2_cfg = {
            channel_serializers.BAND_K:
            'UHF / U / 435000000.000000 / 438000000.000000',
            channel_serializers.AUTOMATED_K: False,
            channel_serializers.MODULATIONS_K: ['FM'],
            channel_serializers.POLARIZATIONS_K: ['LHCP'],
            channel_serializers.BITRATES_K: [300, 600, 900],
            channel_serializers.BANDWIDTHS_K: [12.500000000, 25.000000000]
        }

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
        operational_models.OperationalSlot.objects.set_debug()

    def _sc_get_operational_slots(self):
        """
        Validates the JRPC method <sc_get_operational_slots>
        """
        if self.__verbose_testing:
            print('##### test_sc_get_operational_slots')
        operational_models.OperationalSlot.objects.reset_ids_counter()

        # 1) non-existant Spacecraft
        self.assertRaises(
            models.ObjectDoesNotExist,
            jrpc_sc_scheduling.get_operational_slots,
            0
        )

        # 2) basic test, should not generate slots until the GS is added,
        # raising an exception to confirm it
        self.assertEqual(
            jrpc_sc_chs.sc_channel_create(
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
        self.assertEqual(
            jrpc_gs_chs.gs_channel_create(
                groundstation_id=self.__gs_1_id,
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
        expected = {
            self.__sc_1_ch_1_id: {
                self.__gs_1_ch_1_id: {
                    segment_serializers.GS_ID_K: self.__sc_1_id,
                    jrpc_sch_serial.SLOTS_K: [{
                        jrpc_sch_serial.SLOT_IDENTIFIER_K: '1',
                        jrpc_sch_serial.STATE_K: operational_models.STATE_FREE,
                        jrpc_sch_serial.DATE_START_K: (
                            s_time + datetime.timedelta(days=1)
                        ).isoformat(),
                        jrpc_sch_serial.DATE_END_K: (
                            e_time + datetime.timedelta(days=1)
                        ).isoformat()
                    }, {
                        jrpc_sch_serial.SLOT_IDENTIFIER_K: '2',
                        jrpc_sch_serial.STATE_K: operational_models.STATE_FREE,
                        jrpc_sch_serial.DATE_START_K: (
                            s_time + datetime.timedelta(days=2)
                        ).isoformat(),
                        jrpc_sch_serial.DATE_END_K: (
                            e_time + datetime.timedelta(days=2)
                        ).isoformat()
                    }]
                }
            }
        }
        self.assertEqual(actual, expected, 'Expected different slots!')

        # ### clean up
        self.assertTrue(
            jrpc_gs_chs.gs_channel_delete(
                groundstation_id=self.__gs_1_id,
                channel_id=self.__gs_1_ch_1_id
            ),
            'Could not delete GroundStationChannel = ' + str(
                self.__gs_1_ch_1_id
            )
        )
        self.assertTrue(
            jrpc_sc_chs.sc_channel_delete(
                spacecraft_id=self.__sc_1_id,
                channel_id=self.__sc_1_ch_1_id
            ),
            'Could not delete SpacecraftChannel = ' + str(
                self.__sc_1_ch_1_id
            )
        )

    def test_sc_get_changes(self):
        """
        Validates the JRPC method <sc_get_changes>.
        """
        if self.__verbose_testing:
            print('##### test_sc_get_changes')
        operational_models.OperationalSlot.objects.reset_ids_counter()

        # ### channels required for the tests
        self.assertTrue(
            jrpc_sc_chs.sc_channel_create(
                spacecraft_id=self.__sc_1_id,
                channel_id=self.__sc_1_ch_1_id,
                configuration=self.__sc_1_ch_1_cfg
            ),
            'Channel should have been created!'
        )
        self.assertTrue(
            jrpc_gs_chs.gs_channel_create(
                groundstation_id=self.__gs_1_id,
                channel_id=self.__gs_1_ch_1_id,
                configuration=self.__gs_1_ch_1_cfg
            ),
            'Channel should have been created!'
        )

        # 3) we add some slots and they should be retrieved as 'changed' only
        #  once.
        date_i = misc.get_today_utc() + datetime.timedelta(days=1)
        date_f = misc.get_today_utc() + datetime.timedelta(days=366)

        now = misc.get_now_utc()
        s_time = now + datetime.timedelta(minutes=30)
        e_time = now + datetime.timedelta(minutes=45)

        jrpc_rules.add_rule(
            self.__gs_1_id,
            db_tools.create_jrpc_daily_rule(
                date_i=date_i,
                date_f=date_f,
                starting_time=s_time,
                ending_time=e_time
            )
        )

        actual = operational_models.OperationalSlot.objects.all()
        self.assertEqual(
            len(actual), 2, 'Wrong slots number!'
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

        actual = operational_models.OperationalSlot.objects.all()
        self.assertEqual(
            len(actual), 2, 'Wrong slots number!'
        )

        # ### clean up sc/gs
        self.assertTrue(
            jrpc_gs_chs.gs_channel_delete(
                groundstation_id=self.__gs_1_id, channel_id=self.__gs_1_ch_1_id
            ),
            'Could not delete GroundStationChannel = ' + str(
                self.__gs_1_ch_1_id
            )
        )
        self.assertTrue(
            jrpc_sc_chs.sc_channel_delete(
                spacecraft_id=self.__sc_1_id, channel_id=self.__sc_1_ch_1_id
            ),
            'Could not delete SpacecraftChannel = ' + str(self.__sc_1_ch_1_id)
        )

    def _test_sc_select_slots(self):
        """
        Validates the method for the selection of the slots.
        """
        if self.__verbose_testing:
            print('##### test_sc_get_changes')
        operational_models.OperationalSlot.objects.reset_ids_counter()

        # ### channels required for the tests
        self.assertTrue(
            jrpc_sc_chs.sc_channel_create(
                spacecraft_id=self.__sc_1_id,
                channel_id=self.__sc_1_ch_1_id,
                configuration=self.__sc_1_ch_1_cfg
            ),
            'Channel should have been created!'
        )
        self.assertTrue(
            jrpc_gs_chs.gs_channel_create(
                groundstation_id=self.__gs_1_id,
                channel_id=self.__gs_1_ch_1_id,
                configuration=self.__gs_1_ch_1_cfg
            ),
            'Channel should have been created!'
        )

        date_i = misc.get_today_utc() + datetime.timedelta(days=1)
        date_f = misc.get_today_utc() + datetime.timedelta(days=366)
        now = misc.get_now_utc()
        s_time = now + datetime.timedelta(minutes=30)
        e_time = now + datetime.timedelta(minutes=45)

        jrpc_rules.add_rule(
            self.__gs_1_id,
            db_tools.create_jrpc_daily_rule(
                date_i=date_i,
                date_f=date_f,
                starting_time=s_time,
                ending_time=e_time
            )
        )

        # 1) select all the slots and retrieve the changes
        actual = operational_models.OperationalSlot.objects.all()
        id_list = db_tools.create_identifier_list(actual)
        actual = jrpc_sc_scheduling.select_slots(self.__sc_1_id, id_list)

        self.assertEqual(
            len(actual), 2, 'Wrong slots number!'
        )

        # ### clean up sc/gs
        self.assertTrue(
            jrpc_gs_chs.gs_channel_delete(
                groundstation_id=self.__gs_1_id, channel_id=self.__gs_1_ch_1_id
            ),
            'Could not delete GroundStationChannel = ' + str(
                self.__gs_1_ch_1_id
            )
        )
        self.assertTrue(
            jrpc_sc_chs.sc_channel_delete(
                spacecraft_id=self.__sc_1_id, channel_id=self.__sc_1_ch_1_id
            ),
            'Could not delete SpacecraftChannel = ' + str(self.__sc_1_ch_1_id)
        )
