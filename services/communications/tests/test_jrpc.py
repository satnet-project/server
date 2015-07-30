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
import difflib
from django.core import exceptions
from django.test import TestCase
from services.common import misc
from services.common.testing import helpers as db_tools
from services.communications import jrpc as comms_jrpc, models as comms_models


class TestPassiveCommunications(TestCase):
    """Unit test class.
    Testing of the passive communications service.
    """

    def setUp(self):
        """Database setup
        """
        self.__verbose_testing = False
        self.__gs_1_id = 'gs-la'
        self.__user_profile = db_tools.create_user_profile()
        self.__gs_1 = db_tools.create_gs(
            user_profile=self.__user_profile, identifier=self.__gs_1_id,
        )

    def test_store_passive_message_null(self):
        """JRPC method: services.communiations.storePassiveMessage (1)
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
        """JRPC method: services.communiations.storePassiveMessage (2)
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
        """JRPC method: services.communiations.storeMessage (1)
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
