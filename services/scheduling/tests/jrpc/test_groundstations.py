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
    groundstations as jrpc_gs_ch_if
from services.configuration.jrpc.views.channels import \
    spacecraft as jrpc_sc_ch_if
from services.configuration.jrpc.views import rules as jrpc_rules
from services.scheduling.models import availability as availability_models
from services.scheduling.models import compatibility as compatibility_models
from services.scheduling.models import operational as operational_models
from services.scheduling.jrpc.serializers import operational as \
    jrpc_sch_serial
from services.scheduling.jrpc.views.operational import \
    groundstations as jrpc_gs_scheduling
from services.simulation.models import passes as pass_models


class JRPCGroundStationsSchedulingTest(test.TestCase):
    """JRPC: services.scheduling.groundstations
    """

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
        self.__sc_1_tle_id = 'HUMSAT-D'
        self.__sc_1_ch_1_id = 'xatcobeo-fm'
        self.__sc_1_ch_1_cfg = {
            channel_serializers.FREQUENCY_K: '437000000',
            channel_serializers.MODULATION_K: 'FM',
            channel_serializers.POLARIZATION_K: 'LHCP',
            channel_serializers.BITRATE_K: '300',
            channel_serializers.BANDWIDTH_K: '12.500000000'
        }
        self.__gs_1_id = 'gs-la'
        self.__gs_1_ch_1_id = 'gs-la-fm'
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

        # noinspection PyUnresolvedReferences
        from services.scheduling.signals import availability
        # noinspection PyUnresolvedReferences
        from services.scheduling.signals import compatibility
        # noinspection PyUnresolvedReferences
        from services.scheduling.signals import operational

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

    def test_gs_get_operational_slots(self):
        """
        Validates the JRPC method <gs_get_operational_slots>
        """
        self.__verbose_testing = True
        if self.__verbose_testing:
            print('##### test_gs_get_operational_slots')
            self.maxDiff = None

        operational_models.OperationalSlot.objects.reset_ids_counter()

        if self.__verbose_testing:
            print('######### CHECK #1')
            misc.print_list(
                availability_models.AvailabilitySlot.objects.all(),
                name='availability'
            )
            misc.print_list(
                compatibility_models.ChannelCompatibility.objects.all(),
                name='compatibility'
            )
            misc.print_list(
                pass_models.PassSlots.objects.all(),
                name='passes'
            )
            misc.print_list(
                operational_models.OperationalSlot.objects.all(),
                name='operational'
            )

        # 1) non-existant GroundStation
        self.assertRaises(
            models.ObjectDoesNotExist,
            jrpc_gs_scheduling.get_operational_slots,
            0
        )

        # 2) basic test, should not generate slots until the GS is added,
        # raising an exception to confirm it
        self.assertTrue(
            jrpc_gs_ch_if.gs_channel_create(
                groundstation_id=self.__gs_1_id,
                channel_id=self.__gs_1_ch_1_id,
                configuration=self.__gs_1_ch_1_cfg
            ),
            'Channel should have been created!'
        )
        self.assertRaises(
            Exception,
            jrpc_gs_scheduling.get_operational_slots,
            self.__gs_1_ch_1_id
        )

        # 3) basic test, should generate 2 FREE slots
        self.assertTrue(
            jrpc_sc_ch_if.sc_channel_create(
                spacecraft_id=self.__sc_1_id,
                channel_id=self.__sc_1_ch_1_id,
                configuration=self.__sc_1_ch_1_cfg
            ),
            'Channel should have been created!'
        )

        date_i = misc.get_today_utc() + datetime.timedelta(days=1)
        date_f = misc.get_today_utc() + datetime.timedelta(days=366)

        now = misc.get_now_utc()
        s_time = now - datetime.timedelta(minutes=30)
        e_time = now + datetime.timedelta(hours=5)

        jrpc_rules.add_rule(
            self.__gs_1_id,
            db_tools.create_jrpc_daily_rule(
                date_i=date_i,
                date_f=date_f,
                starting_time=s_time,
                ending_time=e_time
            )
        )

        if self.__verbose_testing:
            print('######### CHECK #2')
            misc.print_list(
                availability_models.AvailabilitySlot.objects.all(),
                name='availability'
            )
            misc.print_list(
                compatibility_models.ChannelCompatibility.objects.all(),
                name='compatibility'
            )
            misc.print_list(
                pass_models.PassSlots.objects.all(),
                name='passes'
            )
            misc.print_list(
                operational_models.OperationalSlot.objects.all(),
                name='operational'
            )

        actual = jrpc_gs_scheduling.get_operational_slots(self.__gs_1_id)
        expected = {
            self.__gs_1_ch_1_id: {
                self.__sc_1_ch_1_id: {
                    segment_serializers.SC_ID_K: self.__sc_1_id,
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

        # ### clean up sc/gs
        self.assertTrue(
            jrpc_gs_ch_if.gs_channel_delete(
                groundstation_id=self.__gs_1_id, channel_id=self.__gs_1_ch_1_id
            ),
            'Could not delete GroundStationChannel = ' + str(
                self.__gs_1_ch_1_id
            )
        )
        self.assertTrue(
            jrpc_sc_ch_if.sc_channel_delete(
                spacecraft_id=self.__sc_1_id, channel_id=self.__sc_1_ch_1_id
            ),
            'Could not delete SpacecraftChannel = ' + str(self.__sc_1_ch_1_id)
        )
