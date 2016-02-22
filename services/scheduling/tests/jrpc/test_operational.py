
import datetime
from django import test as django_test
from django.db.models import Q
from services.common import misc as sn_misc
from services.common import helpers as db_tools
from services.configuration.jrpc.serializers import \
    channels as channel_serializers
from services.configuration.jrpc.views import rules as jrpc_rules
from services.scheduling.models import operational as operational_models
from services.scheduling.jrpc.views.operational import slots as scheduling_slots

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


class JRPCBookingProcessTest(django_test.TestCase):
    """Testing class for the slot information process
    """

    def setUp(self):
        """
        This method populates the database with some information to be used
        only for this test.
        """
        self.__verbose_testing = False
        self.__test_slot_id = -1

        self.__sc_1_id = 'xatcobeo-sc'
        self.__sc_1_tle_id = 'HUMSAT-D'
        self.__sc_1_ch_1_id = 'gmsk-sc-1'
        self.__sc_1_ch_1_f = 437000000
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
        self.__sc_1_ch_1 = db_tools.sc_add_channel(
            self.__sc_1, self.__sc_1_ch_1_f, self.__sc_1_ch_1_id,
        )
        self.__gs_1_ch_1 = db_tools.gs_add_channel(
            self.__gs_1, self.__band, self.__gs_1_ch_1_id
        )

        self.__rule_1 = jrpc_rules.add_rule(
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

    def test_test_slot(self):
        """JRPC test: services.scheduling.getSlot (SLOT -1)
        Basic TEST slot test
        """
        if self.__verbose_testing:
            print('##### test_test_slot')

        s_time = sn_misc.get_now_utc(no_microseconds=True)
        e_time = s_time + datetime.timedelta(hours=2)

        if self.__verbose_testing:
            print('s_time = ' + str(s_time.isoformat()))
            print('e_time = ' + str(e_time.isoformat()))

        self.assertEquals(
            scheduling_slots.get_slot(self.__test_slot_id), {
                'state': 'TEST',
                'gs_username': 'diego.nodar@humsat.org',
                'sc_username': 'alberto.gonzalez@humsat.org',
                'starting_time': s_time.isoformat(),
                'ending_time': e_time.isoformat()
            }
        )

    def test_get_next_slot(self):
        """JRPC test: services.scheduling.slot.next
        """
        if self.__verbose_testing:
            print('##### test_get_next_slot')

        self.assertEquals(scheduling_slots.get_next_slot('NonExistent'), {})
        self.assertIsNotNone(scheduling_slots.get_next_slot('test@test.test'))
