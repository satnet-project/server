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

from django.test import TestCase
from services.common import pusher as satnet_pusher


class TestPusher(TestCase):
    """
    Validation of the usage of the pusher.com services.
    """

    def setUp(self):
        """Test setup
        """
        self.__verbose_testing = False
        self.__push_service = satnet_pusher.PushService()
        self.__ch_name = 'test_channel'
        self.__ev_name = 'test_event'
        self.__ev_data = {
            'message': 'Hello SATNET!'
        }

    def test_basic(self):
        """UNIT test: services.common.pusher.test_service
        Simple test that invokes a testing event through the test channel that
        is enabled by default at the pusher.com website.
        """
        self.__push_service.test_service()

    def test_connection(self):
        """UNIT test: services.common.pusher.trigger_event
        Validates the basic usage of the testing channel.
        """
        self.__push_service.trigger_event(
            self.__ch_name, self.__ev_name, self.__ev_data
        )
