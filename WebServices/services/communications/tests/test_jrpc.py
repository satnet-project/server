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

from django.core import exceptions
from django.test import TestCase

from services.common import testing as db_tools
from services.communications import jrpc as jrpc_comms
from services.configuration import signals
from services.configuration.jrpc.serializers import serialization as jrpc_keys
from services.configuration.jrpc.views import channels as jrpc_channels_if
from services.scheduling.models import operational


class TestPassiveCommunications(TestCase):
    """Unit test class.
    Testing of the passive communications service.
    """

    def setUp(self):

        self.__verbose_testing = False

        self.__gs_1_id = 'gs-la'
        self.__gs_1_ch_1_id = 'gs-la-fm'
        self.__gs_1_ch_1_cfg = {
            jrpc_keys.BAND_K:
            'UHF / U / 435000000.000000 / 438000000.000000',
            jrpc_keys.MODULATIONS_K: ['FM'],
            jrpc_keys.POLARIZATIONS_K: ['LHCP'],
            jrpc_keys.BITRATES_K: [300, 600, 900],
            jrpc_keys.BANDWIDTHS_K: [12.500000000, 25.000000000]
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
        self.__gs_1 = db_tools.create_gs(
            user_profile=self.__user_profile, identifier=self.__gs_1_id,
        )
        jrpc_channels_if.gs_channel_create(
            ground_station_id=self.__gs_1_id,
            channel_id=self.__gs_1_ch_1_id,
            configuration=self.__gs_1_ch_1_cfg
        )
        operational.OperationalSlot.objects.get_simulator().set_debug()

    def test_communications_null(self):
        """Unit test method.
        Basic unit testing method for checking the behavior of the passive
        communications service under null or empty parameters.
        """
        if self.__verbose_testing:
            print '>>> communications_null'

        # 1) GS does not exist
        self.assertRaises(
            exceptions.ObjectDoesNotExist,
            jrpc_comms.store_passive_message,
            groundstation_id='AAA',
            gs_channel_id='AAAA',
            timestamp=0,
            doppler_shift=0,
            message='000'
        )

        # 2) channel does not belong to GS
        self.assertRaises(
            Exception,
            jrpc_comms.store_passive_message,
            groundstation_id=self.__gs_1_id,
            gs_channel_id=0,
            timestamp=0,
            doppler_shift=0,
            message='000'
        )

        # 3) correct storage of a basic message
        self.assertRaises(
            Exception,
            jrpc_comms.store_passive_message,
            groundstation_id=self.__gs_1_id,
            gs_channel_id=0,
            timestamp=0,
            doppler_shift=0,
            message=None
        )

        # 4) correct message is stored
        #message_1_id = jrpc_comms.store_passive_message(
        #    groundstation_id=self.__gs_1_id,
        #    gs_channel_id=self.__gs_1_ch_1_id,
        #    timestamp=0,
        #    doppler_shift=0.0,
        #    message=None
        #)
        #print 'message_1_id = ' + str(message_1_id)