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

from services.common import misc, simulation, helpers as db_tools
from services.configuration.jrpc.serializers import \
    channels as channel_serializers
from services.configuration.jrpc.views import rules as jrpc_rules_if
from services.configuration.jrpc.views.channels import \
    groundstations as jrpc_gs_ch_if
from services.configuration.jrpc.views.channels import \
    spacecraft as jrpc_sc_ch_if
from services.configuration.models import rules as rule_models
from services.scheduling.models import availability as availability_models
from services.scheduling.models import operational as operational_models
from services.simulation.models import passes as pass_models


class OperationalModels(test.TestCase):

    def setUp(self):
        """
        This method populates the database with some information to be used
        only for this test.
        """
        self.__verbose_testing = False

        if not self.__verbose_testing:
            logging.getLogger('configuration').setLevel(level=logging.CRITICAL)
            logging.getLogger('scheduling').setLevel(level=logging.CRITICAL)

        self.__rule_1_cfg = db_tools.create_jrpc_daily_rule(
            starting_time=misc.localize_time_utc(datetime.time(
                hour=8, minute=0, second=0
            )),
            ending_time=misc.localize_time_utc(datetime.time(
                hour=23, minute=55, second=0
            ))
        )

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
        self.__gs_1 = db_tools.create_gs(
            user_profile=self.__user_profile, identifier=self.__gs_1_id,
        )

    def test_1_compatibility_sc_channel_added_deleted(self):
        """INTR test: compatibility changed generates operational slots

        1) +GS_CH
        2) +RULE
        3) +SC_CH
        4) -SC_CH
        5) -RULE
        6) -GS_CH

        OperationalSlots should be available only in bewteen steps 3 and 4.
        """
        if self.__verbose_testing:
            print('##### test_add_slots: no rules')

        self.__sc_1 = db_tools.create_sc(
            user_profile=self.__user_profile,
            identifier=self.__sc_1_id,
            tle_id=self.__sc_1_tle_id,
        )

        self.assertTrue(
            jrpc_gs_ch_if.gs_channel_create(
                groundstation_id=self.__gs_1_id,
                channel_id=self.__gs_1_ch_1_id,
                configuration=self.__gs_1_ch_1_cfg
            ),
            'Channel should have been created!'
        )

        r_1_id = jrpc_rules_if.add_rule(self.__gs_1_id, self.__rule_1_cfg)
        self.assertIsNot(r_1_id, 0, 'Rule should have been added!')

        self.assertTrue(
            jrpc_sc_ch_if.sc_channel_create(
                spacecraft_id=self.__sc_1_id,
                channel_id=self.__sc_1_ch_1_id,
                configuration=self.__sc_1_ch_1_cfg
            ), 'Channel should have been created!'
        )

        a_slots = availability_models.AvailabilitySlot.objects.get_applicable(
            groundstation=self.__gs_1
        )

        if self.__verbose_testing:
            misc.print_list(a_slots, 'AvailabilitySlots')
            misc.print_list(
                operational_models.OperationalSlot.objects.all(),
                'OperationalSlots'
            )

        self.assertGreaterEqual(
            len(operational_models.OperationalSlot.objects.all()), 2
        )

        self.assertTrue(
            jrpc_sc_ch_if.sc_channel_delete(
                spacecraft_id=self.__sc_1_id, channel_id=self.__sc_1_ch_1_id
            )
        )

        expected = []
        actual = list(
            operational_models.OperationalSlot.objects.filter(
                state=operational_models.STATE_FREE
            ).values_list('state')
        )

        if self.__verbose_testing:
            print('>>> window = ' + str(
                simulation.OrbitalSimulator.get_simulation_window()
            ))
            misc.print_list(rule_models.AvailabilityRule.objects.all())
            misc.print_list(availability_models.AvailabilitySlot.objects.all())
            misc.print_list(operational_models.OperationalSlot.objects.all())
            misc.print_list(actual)
            misc.print_list(expected)

        self.assertEqual(actual, expected)

        self.assertTrue(
            jrpc_rules_if.remove_rule(self.__gs_1_id, r_1_id),
            'Rule should have been removed!'
        )
        expected = []
        actual = list(
            operational_models.OperationalSlot.objects.filter(
                state=operational_models.STATE_FREE
            ).values_list('state')
        )
        self.assertEqual(actual, expected)

        self.assertTrue(
            jrpc_gs_ch_if.gs_channel_delete(
                groundstation_id=self.__gs_1_id,
                channel_id=self.__gs_1_ch_1_id
            ),
            'Could not delete GroundStationChannel = ' + str(
                self.__gs_1_ch_1_id
            )
        )
        expected = []
        actual = list(
            operational_models.OperationalSlot.objects.filter(
                state=operational_models.STATE_FREE
            ).values_list('state')
        )
        self.assertEqual(actual, expected)

    def test_2_no_compatibility_no_slots(self):
        """INTR test: no compatible channels, no slots

        (INITIAL): 1 GS, no channels, no rules
        (1A - STEP) : +SC
        (1B - STEP) : +rule
        (1C - CHECK): no operational slots
        """
        self.assertEquals(
            pass_models.PassSlots.objects.filter(
                spacecraft__identifier=self.__sc_1_id
            ).count(),
            0
        )

        r_1_id = jrpc_rules_if.add_rule(self.__gs_1_id, self.__rule_1_cfg)
        self.assertIsNot(r_1_id, 0, 'Rule should have been added!')

        self.assertEquals(
            len(operational_models.OperationalSlot.objects.all()), 0
        )

        self.__sc_1 = db_tools.create_sc(
            user_profile=self.__user_profile,
            identifier=self.__sc_1_id,
            tle_id=self.__sc_1_tle_id,
        )

        self.assertEquals(
            len(operational_models.OperationalSlot.objects.all()), 0
        )
