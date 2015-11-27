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

from services.common import misc, helpers as db_tools
from services.configuration.jrpc.serializers import \
    channels as channel_serializers
from services.configuration.jrpc.serializers import rules as rule_serializers
from services.configuration.jrpc.views import rules as rule_jrpc
from services.scheduling.models import availability as availability_models
from services.scheduling.models import operational as operational_models


class INTRARulesAvailability(test.TestCase):
    """INTRA modules tests: rules should automatically update the availability
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

        self.__rule_date = misc.get_today_utc() + datetime.timedelta(days=1)
        self.__rule_s_time = misc.get_today_utc().replace(
            hour=12, minute=0, second=0, microsecond=0
        )
        self.__rule_e_time = self.__rule_s_time + datetime.timedelta(hours=5)

        # noinspection PyUnresolvedReferences
        from services.scheduling.signals import availability

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

    def test_rule_created_deleted(self):
        """INTRA test: availability changed after basic rule operations
        """
        if self.__verbose_testing:
            print('##### test_rule_created_deleted')

        rule_1_pk = rule_jrpc.add_rule(
            self.__gs_1_id,
            db_tools.create_jrpc_once_rule(
                starting_time=self.__rule_s_time, ending_time=self.__rule_e_time
            )
        )

        self.assertEquals(
            availability_models.AvailabilitySlot.objects.count(),
            1,
            'One availability slot should have been created'
        )

        rule_jrpc.remove_rule(self.__gs_1_id, rule_1_pk)
        self.assertEquals(
            availability_models.AvailabilitySlot.objects.count(),
            0,
            'No availability slots should be available'
        )

    def test_multiple_rules(self):
        """INTRA test: multiple rules
        """
        if self.__verbose_testing:
            print('##### test_rule_created_deleted')

        rule_1_pk = rule_jrpc.add_rule(
            self.__gs_1_id,
            db_tools.create_jrpc_once_rule(
                starting_time=self.__rule_s_time, ending_time=self.__rule_e_time
            )
        )

        self.assertEquals(
            availability_models.AvailabilitySlot.objects.count(), 1
        )

        rule_2_pk = rule_jrpc.add_rule(
            self.__gs_1_id,
            db_tools.create_jrpc_once_rule(
                operation=rule_jrpc.rule_serializers.RULE_OP_REMOVE,
                starting_time=self.__rule_s_time, ending_time=self.__rule_e_time
            )
        )

        self.assertEquals(
            availability_models.AvailabilitySlot.objects.count(), 0
        )

        rule_jrpc.remove_rule(self.__gs_1_id, rule_2_pk)

        self.assertEquals(
            availability_models.AvailabilitySlot.objects.count(), 1
        )

        rule_3 = db_tools.create_jrpc_once_rule(
            operation=rule_serializers.RULE_OP_REMOVE,
            starting_time=self.__rule_s_time, ending_time=self.__rule_e_time
        )
        rule_3_pk = rule_jrpc.add_rule(self.__gs_1_id, rule_3)

        self.assertEquals(
            availability_models.AvailabilitySlot.objects.count(), 0
        )

        rule_jrpc.remove_rule(self.__gs_1_id, rule_3_pk)

        self.assertEquals(
            availability_models.AvailabilitySlot.objects.count(), 1
        )

        rule_jrpc.remove_rule(self.__gs_1_id, rule_1_pk)

        self.assertEquals(
            availability_models.AvailabilitySlot.objects.count(), 0
        )
