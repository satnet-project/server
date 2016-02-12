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

import base64
import datetime
import difflib
from django.core import exceptions
from django.test import TestCase

from services.configuration.jrpc.serializers import channels as \
    channel_serializers
from services.configuration.jrpc.views import rules as jrpc_rules
from services.configuration.jrpc.views.channels import \
    groundstations as jrpc_gs_chs
from services.configuration.jrpc.views.channels import \
    spacecraft as jrpc_sc_chs
from services.common import misc, helpers as db_tools
from services.communications import jrpc as comms_jrpc, models as comms_models
from services.scheduling.models import operational as operational_models
from services.scheduling.signals import operational as operational_signals
from services.scheduling.jrpc.views.operational import \
    groundstations as jrpc_gs_scheduling


class TestPassiveCommunications(TestCase):
    """Unit test class
    Testing of the passive communications service.
    """

    def setUp(self):
        """Database setup
        """
        self.__verbose_testing = False

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

    def test_store_passive_message_null(self):
        """JRPC test: services.communiations.storePassiveMessage (1)
        Basic unit testing method for checking the behavior of the passive
        communications service under null or empty parameters.
        """
        if self.__verbose_testing:
            print('>>> test_store_passive_message_null')

        # 1) GS does not exist
        self.assertRaises(
            exceptions.ObjectDoesNotExist,
            comms_jrpc.store_passive_message,
            groundstation_id='AAA',
            timestamp=0,
            doppler_shift=0,
            message='000'
        )

        # 2) Empty message
        self.assertRaises(
            Exception,
            comms_jrpc.store_passive_message,
            groundstation_id=self.__gs_1_id,
            timestamp=0,
            doppler_shift=0,
            message=None
        )

    def test_store_passive_message(self):
        """JRPC test: services.communiations.storePassiveMessage (2)
        Simple test for validating the storage of passive messages.
        """
        if self.__verbose_testing:
            print('>>> test_store_passive_message')

        self.assertEqual(
            comms_jrpc.store_passive_message(
                groundstation_id=self.__gs_1_id,
                timestamp=misc.get_utc_timestamp(misc.get_now_utc()),
                doppler_shift=0.0,
                message=db_tools.MESSAGE_BASE64
            ),
            1,
            'Message ID expected not to be none'
        )

        message = comms_models.PassiveMessage.objects.get(pk=1).message
        self.assertEqual(
            db_tools.MESSAGE_BASE64.decode(), message,
            'In-database stored message differs, diff = ' + str(
                difflib.ndiff(db_tools.MESSAGE_BASE64.decode(), message))
        )

        if self.__verbose_testing:
            print('>>> message_1 (RAW) = ' + str(message))
            print('>>> message_1 (STR) = ' + str(base64.b64decode(message)))

        self.assertEqual(
            comms_jrpc.store_passive_message(
                groundstation_id=self.__gs_1_id,
                timestamp=misc.get_utc_timestamp(misc.get_now_utc()),
                doppler_shift=0.0,
                message=db_tools.MESSAGE_BASE64
            ),
            2,
            'Message ID expected to be 2'
        )

        message = comms_models.PassiveMessage.objects.get(pk=2).message
        self.assertEqual(
            db_tools.MESSAGE_BASE64.decode(), message,
            'In-database stored message differs, diff = ' + str(
                difflib.ndiff(db_tools.MESSAGE_BASE64.decode(), message))
        )

        if self.__verbose_testing:
            print('>>> message_2 (RAW) = ' + str(message))
            print('>>> message_2 (STR) = ' + str(base64.b64decode(message)))

    def test_store_message_null(self):
        """JRPC test: services.communiations.storeMessage (1)
        Basic unit testing method for checking the behavior of the
        communications service under null or empty parameters.
        """
        if self.__verbose_testing:
            print('>>> test_store_message_null')

        # 1) slot does not exist
        self.assertRaises(
            exceptions.ObjectDoesNotExist,
            comms_jrpc.store_message,
            slot_id=100,
            upwards=True,
            forwarded=True,
            timestamp=0,
            message='000'
        )

        # 2) Empty message
        self.assertRaises(
            Exception,
            slot_id=100,
            upwards=True,
            forwarded=True,
            timestamp=0,
            message=None
        )

    def test_store_message(self):
        """JRPC test: services.communiations.storeMessage (2)

        Validates the remote storage of a message through JRPC.
        """
        if self.__verbose_testing:
            print('>>> test_store_message')

        # 1) we retrieve any of the slots that we have just created
        op_slot = operational_models.OperationalSlot.objects.all()[0]
        # 2) now we attemp to write a messageto to the retrieved slot
        message_id = comms_jrpc.store_message(
            slot_id=op_slot.identifier,
            upwards=True, forwarded=True, timestamp=0,
            message=db_tools.MESSAGE_BASE64
        )
        # 3) we check that the message was stored correctly
        message = comms_models.Message.objects.get(pk=message_id)
        self.maxDiff = None
        self.assertEquals(
            str.encode(message.message, 'UTF-8'), db_tools.MESSAGE_BASE64
        )

    def test_store_message_testing_slot(self):
        """JRPC test: services.communications.storeMessage (3)

        Unit test that validates the storage of messages when referred to the
        operational slot -1, which does not exist. This method is necessary for
        allowing complex integration tests in order to validate the connection
        and the usage of the protocol component.
        """
        if self.__verbose_testing:
            print('>>> test_store_message_testing_slot')

        # 1) first, we create the fake operational slot to associate the message
        #       with
        operational_signals.satnet_loaded(None)

        # 2) now we attemp to write a messageto the slot -1
        message_id = comms_jrpc.store_message(
            slot_id='-1', upwards=True, forwarded=True, timestamp=0,
            message=db_tools.MESSAGE_BASE64
        )

        # 3) we check that the message was stored correctly
        message = comms_models.Message.objects.get(pk=message_id)
        self.maxDiff = None
        self.assertEquals(
            str.encode(message.message, 'UTF-8'), db_tools.MESSAGE_BASE64
        )
