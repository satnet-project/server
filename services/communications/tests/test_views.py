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
import logging
from django import test
from services.common import misc
from services.common.testing import helpers as db_tools
from services.communications import jrpc as comms_jrpc, views as comms_views


class TestCommunicationsViews(test.TestCase):
    """Test class for the Communications Views.
    """

    def setUp(self):
        """Database setup for the tests.
        """
        self.__verbose_testing = False

        self.__user = db_tools.create_user_profile()
        self.__request = db_tools.create_request(user_profile=self.__user)

        self.__user_no_gs = db_tools.create_user_profile(username='no-gs-user')
        self.__request_ung = db_tools.create_request(
            user_profile=self.__user_no_gs
        )

        self.__user_gs_2 = db_tools.create_user_profile(username='gs-2-user')
        self.__request_gs_2 = db_tools.create_request(
            user_profile=self.__user_gs_2
        )

        self.__gs_1_id = 'gs-uvigo'
        self.__gs_1 = db_tools.create_gs(
            user_profile=self.__user,
            identifier=self.__gs_1_id
        )
        self.__gs_2_id = 'gs-calpoly'
        self.__gs_2 = db_tools.create_gs(
            user_profile=self.__user_gs_2,
            identifier=self.__gs_2_id
        )

        self.__short_message = 'QWxhZGRpbjpvcGVuIHNlc2FtZQ=='
        self.__long_message = 'ogAAAABErEarAAAAAESsRwoAAAAARKxHaAAAAABErEfGAA' \
                              'AAAESsSCVCE4y4RKxIg0NICpdErEjhQ4IvIkSsSUBDKx7d' \
                              'RKxJngAAAABErEn8AAAAAESsSloAAAAARKxKuQAAAABEtQ' \
                              'kRAAAAAES1CXkAAAAARLUJ4QAAAABEtQpKAAAAAES1CrJD' \
                              'JhD9RLULGkN2IZtEtQuCQ0j6M0S1C'
        self.__b64_message = base64.b64encode(
            b'Base64 is a group of similar binary-to-text encoding schemes '
            b'that represent binary data in an ASCII string format by '
            b'translating it into a radix-64 representation. The term Base64 '
            b'originates from a specific MIME content transfer encoding.'
        )

        if not self.__verbose_testing:
            logging.getLogger('communications').setLevel(level=logging.CRITICAL)

    def test_get_queryset(self):
        """View test
        Test for validating the retrieval of the messages for the GroundStations
        of a given user (the one making the request).
        """
        if self.__verbose_testing:
            print('>>> test_get_queryset:')

        # 1) User with no ground stations registered
        view = comms_views.PassiveMessages()
        view.request = self.__request_ung
        actual_m = view.get_queryset()
        self.assertEqual(len(actual_m), 0, 'List should be empty')

        # 2) User with a ground station registered that has no messages
        view = comms_views.PassiveMessages()
        view.request = self.__request
        actual_m = view.get_queryset()
        self.assertEqual(len(actual_m), 0, 'List should be empty')

        # 3) User with a ground station registered and a message available
        comms_jrpc.store_passive_message(
            groundstation_id=self.__gs_1_id,
            timestamp=misc.get_utc_timestamp(misc.get_now_utc()),
            doppler_shift=0.0,
            message=self.__b64_message
        )
        view = comms_views.PassiveMessages()
        view.request = self.__request
        actual_m = view.get_queryset()
        self.assertEqual(len(actual_m), 1, 'List should contain one message')

        # 4) User with a ground station registered and two messages available
        comms_jrpc.store_passive_message(
            groundstation_id=self.__gs_1_id,
            timestamp=misc.get_utc_timestamp(misc.get_now_utc()),
            doppler_shift=0.0,
            message=self.__b64_message
        )
        view = comms_views.PassiveMessages()
        view.request = self.__request
        actual_m = view.get_queryset()
        self.assertEqual(len(actual_m), 2, 'List should contain two messages')

        # 5) User 2 should receive no messages from user 1 groundstations
        view = comms_views.PassiveMessages()
        view.request = self.__request_gs_2
        actual_m = view.get_queryset()
        self.assertEqual(len(actual_m), 0, 'List should be empty')

        comms_jrpc.store_passive_message(
            groundstation_id=self.__gs_2_id,
            timestamp=misc.get_utc_timestamp(misc.get_now_utc()),
            doppler_shift=0.0,
            message=self.__b64_message
        )
        view = comms_views.PassiveMessages()
        view.request = self.__request_gs_2
        actual_m = view.get_queryset()
        self.assertEqual(len(actual_m), 1, 'List should have one message')

        if self.__verbose_testing:
            for m in actual_m:
                print('>>> m = ' + str(m))