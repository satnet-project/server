
import datetime
import logging
from django import test

from services.common import misc, helpers as db_tools
from services.configuration.jrpc.serializers import channels as \
    channel_serializers
from services.configuration.jrpc.views import rules as jrpc_rules
from services.configuration.jrpc.views.channels import \
    groundstations as jrpc_gs_chs
from services.configuration.jrpc.views.channels import \
    spacecraft as jrpc_sc_chs
from services.scheduling.jrpc.views.operational import \
    groundstations as jrpc_gs_scheduling
from services.scheduling.jrpc.views.operational import \
    spacecraft as jrpc_sc_scheduling
from services.scheduling.models import operational

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


class JRPCBookingProcessTest(test.TestCase):
    """Testing class for the booking process.

    This class tests completely the booking process in which a GroundStation
    operator and a Spacecraft operator collaborate through the <Scheduling>
    service for arranging the remote operation of the Spacecraft.
    """

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

        operational.OperationalSlot.objects.set_debug()

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

        self.assertEqual(
            jrpc_gs_chs.gs_channel_create(
                groundstation_id=self.__gs_1_id,
                channel_id=self.__gs_1_ch_1_id,
                configuration=self.__gs_1_ch_1_cfg
            ), True, 'Channel should have been created!'
        )
        self.assertRaises(
            Exception,
            jrpc_gs_scheduling.get_operational_slots,
            self.__gs_1_ch_1_id
        )

        # 3) basic test, should generate 2 FREE slots
        self.assertEqual(
            jrpc_sc_chs.sc_channel_create(
                spacecraft_id=self.__sc_1_id,
                channel_id=self.__sc_1_ch_1_id,
                configuration=self.__sc_1_ch_1_cfg
            ), True, 'Channel should have been created!'
        )

        # 4) we add a daily rule 12 hours, 00:00:01am to 11:59:59pm UTC
        #       all pass slots should became operational slots.
        self.__rule_1 = jrpc_rules.add_rule(
            self.__gs_1_id,
            db_tools.create_jrpc_daily_rule(
                date_i=misc.get_today_utc(),
                date_f=misc.get_today_utc() + datetime.timedelta(days=50),
                starting_time=misc.get_next_midnight() + datetime.timedelta(
                    seconds=1
                ),
                ending_time=misc.get_next_midnight() + datetime.timedelta(
                    hours=23, minutes=59, seconds=59
                )
            )
        )

    def test_1_booking(self):
        """Basic booking test.

        This test should validate the basic booking process of remote
        operations, which involve:

        * Spacecraft operators SELECT slots (remote operation request).
        * GroundStation operatotrs CONFIRM the selection of the slots (remote
        operation is RESERVED).
        * Spacecraft operators and GroundStation operators can retrieve this
        final status of the slots through the 'getChanges' method.

        """
        if self.__verbose_testing:
            print('##### test_1_booking')

        selection_1 = [
            int(x.identifier) for x in
            operational.OperationalSlot.objects.filter(
                state=operational.STATE_FREE
            ).order_by('id')[:3]
        ]

        # 0) Spacecraft operators selected a set of slots...
        sc_s_slots = jrpc_sc_scheduling.select_slots(
            self.__sc_1_id, selection_1
        )
        self.assertEqual(
            [int(x['identifier']) for x in sc_s_slots], selection_1
        )

        # 1) GroundStation operators confirm the selected slots...
        gs_c_slots = jrpc_gs_scheduling.confirm_selections(
            self.__gs_1_id, selection_1
        )
        self.assertEqual(
            [int(x['identifier']) for x in gs_c_slots], selection_1
        )

        # 5) GroundStation operators cancel the selected slots...
        jrpc_gs_scheduling.cancel_reservations(self.__gs_1_id, selection_1)
        # 5.a) No canceled Operational Slots
        self.assertEqual(
            [
                x.identifier
                for x in operational.OperationalSlot.objects.filter(
                    state=operational.STATE_CANCELED
                )
            ],
            []
        )
        # 5.b) No selected Operational Slots
        self.assertEqual(
            [
                x.identifier
                for x in operational.OperationalSlot.objects.filter(
                    state=operational.STATE_SELECTED
                )
            ],
            []
        )

        # 7) SpacecraftOperator retries the selection...
        sc_s_slots = jrpc_sc_scheduling.select_slots(
            self.__sc_1_id, selection_1
        )
        self.assertEqual(
            [int(x['identifier']) for x in sc_s_slots], selection_1
        )

        # 8) GroundStation operator denies the selection...
        gs_d_slots = jrpc_gs_scheduling.deny_selections(
            self.__gs_1_id, selection_1
        )
        self.assertEqual(
            [int(x['identifier']) for x in gs_d_slots], selection_1
        )

        # 5.a) No canceled Operational Slots
        self.assertEqual(
            [
                x.identifier
                for x in operational.OperationalSlot.objects.filter(
                    state=operational.STATE_CANCELED
                )
            ],
            []
        )
        # 5.b) No selected Operational Slots
        self.assertEqual(
            [
                x.identifier
                for x in operational.OperationalSlot.objects.filter(
                    state=operational.STATE_SELECTED
                )
            ],
            []
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
