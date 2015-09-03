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

from services.common import misc
from services.common.testing import helpers as db_tools
from services.configuration.jrpc.serializers import channels as \
    channel_serializers
from services.configuration.jrpc.views.channels import \
    groundstations as jrpc_gs_chs
from services.configuration.jrpc.views.channels import \
    spacecraft as jrpc_sc_chs
from services.configuration.jrpc.views import rules as jrpc_rules
from services.scheduling.jrpc.views.operational import \
    groundstations as jrpc_gs_scheduling
from services.scheduling.jrpc.views.operational import \
    spacecraft as jrpc_sc_scheduling
from services.scheduling.models import operational


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

        operational.OperationalSlot.objects.get_simulator().set_debug()
        operational.OperationalSlot.objects.set_debug()

        # noinspection PyUnresolvedReferences
        from services.scheduling.signals import availability

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

        self.__date_i = misc.get_today_utc() + datetime.timedelta(days=1)
        self.__date_f = misc.get_today_utc() + datetime.timedelta(days=366)

        self.__date_now = misc.get_now_utc()
        self.__date_s_time = self.__date_now + datetime.timedelta(minutes=30)
        self.__date_e_time = self.__date_now + datetime.timedelta(minutes=45)

        jrpc_rules.add_rule(
            self.__gs_1_id,
            db_tools.create_jrpc_daily_rule(
                date_i=self.__date_i,
                date_f=self.__date_f,
                starting_time=self.__date_s_time,
                ending_time=self.__date_e_time
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
        operational.OperationalSlot.objects.reset_ids_counter()

        sc_s_slots = jrpc_sc_scheduling.select_slots(
            self.__sc_1_id, [1, 2, 3]
        )
        db_tools.create_identifier_list(sc_s_slots)

        # 1) selection has to be notified only once to the GS
        gs_s_slots = jrpc_gs_scheduling.get_changes(self.__gs_1_id)
        self.assertEqual(
            len(gs_s_slots), 2, 'Selected slots should be 2, selected = ' +
            misc.list_2_string(gs_s_slots)
        )
        self.assertRaises(
            Exception, jrpc_gs_scheduling.get_changes, self.__gs_1_id
        )

        # 2) selection should not be notified to the SC (they already made it!)
        self.assertRaises(
            Exception, jrpc_sc_scheduling.get_changes, self.__sc_1_id
        )

        # 3) GroundStation operators confirm the selected slots...
        gs_c_slots = jrpc_gs_scheduling.confirm_selections(
            self.__gs_1_id, [1, 2, 3]
        )
        self.assertEqual(
            len(gs_c_slots), 2, 'Confirmed slots should be 2, selected = ' +
            misc.list_2_string(gs_c_slots)
        )
        self.assertRaises(
            Exception, jrpc_gs_scheduling.get_changes, self.__gs_1_id
        )

        # 4) Spacecraft operators must be notified with the reservations,
        # but only once!
        sc_r_slots = jrpc_sc_scheduling.get_changes(self.__sc_1_id)
        self.assertEqual(
            len(sc_r_slots), 2, 'Reserved slots should be 2, selected = ' +
            misc.list_2_string(sc_r_slots)
        )
        self.assertRaises(
            Exception, jrpc_sc_scheduling.get_changes, self.__sc_1_id
        )

        # 5) GroundStation operators cancel the selected slots...
        jrpc_gs_scheduling.cancel_reservations(
            self.__gs_1_id, [1, 2, 3]
        )
        self.assertRaises(
            Exception, jrpc_gs_scheduling.get_changes, self.__gs_1_id
        )

        # 6) Spacecraft operators must be notified with the cancelations,
        # but only once!
        sc_r_slots = jrpc_sc_scheduling.get_changes(self.__sc_1_id)
        self.assertEqual(
            len(sc_r_slots), 2, 'Canceled slots should be 2, selected = ' +
            misc.list_2_string(sc_r_slots)
        )
        self.assertRaises(
            Exception, jrpc_sc_scheduling.get_changes, self.__sc_1_id
        )
        self.assertEqual(
            len(
                operational.OperationalSlot.objects.filter(
                    state=operational.STATE_CANCELED
                )
            ),
            0,
            'No slots should be kept as canceled, '
            'operational.OperationalSlot.filter('
            'state=operational.STATE_CANCELED) = ' + misc.list_2_string(
                operational.OperationalSlot.objects.filter(
                    state=operational.STATE_CANCELED
                )
            )
        )

        # 7) SpacecraftOperator retries the selection...
        self.assertEqual(
            len(jrpc_sc_scheduling.select_slots(self.__sc_1_id, [1, 2, 3])),
            2,
            '2 slots must have been selected.'
        )

        # 8) GroundStation operator denies the selection...
        gs_d_slots = jrpc_gs_scheduling.deny_selections(
            self.__gs_1_id, [1, 2, 3]
        )
        self.assertEqual(
            len(gs_d_slots), 2, 'Denied slots should be 3, selected = ' +
            misc.list_2_string(gs_d_slots)
        )
        self.assertRaises(
            Exception, jrpc_gs_scheduling.get_changes, self.__gs_1_id
        )
        sc_r_slots = jrpc_sc_scheduling.get_changes(self.__sc_1_id)
        self.assertEqual(
            len(sc_r_slots), 2, 'Denied slots should be 3, selected = ' +
            misc.list_2_string(sc_r_slots)
        )
        self.assertRaises(
            Exception, jrpc_sc_scheduling.get_changes, self.__sc_1_id
        )
        self.assertEqual(
            len(
                operational.OperationalSlot.objects.filter(
                    state=operational.STATE_DENIED
                )
            ),
            0,
            'No slots should be kept as canceled, '
            'operational.OperationalSlot.filter('
            'state=operational.STATE_DENIED) = ' + misc.list_2_string(
                operational.OperationalSlot.objects.filter(
                    state=operational.STATE_DENIED
                )
            )
        )

        # ### clean up sc/gs
        self.assertEqual(
            jrpc_gs_chs.gs_channel_delete(
                groundstation_id=self.__gs_1_id, channel_id=self.__gs_1_ch_1_id
            ),
            True,
            'Could not delete GroundStationChannel = ' + str(
                self.__gs_1_ch_1_id
            )
        )
        self.assertEqual(
            jrpc_sc_chs.sc_channel_delete(
                spacecraft_id=self.__sc_1_id, channel_id=self.__sc_1_ch_1_id
            ),
            True,
            'Could not delete SpacecraftChannel = ' + str(self.__sc_1_ch_1_id)
        )
