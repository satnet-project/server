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

from services.common import misc, helpers as db_tools, pusher as satnet_push
from services.communications import jrpc as comms_jrpc


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
        self.__short_message = 'QWxhZGRpbjpvcGVuIHNlc2FtZQ=='
        self.__long_message = 'ogAAAABErEarAAAAAESsRwoAAAAARKxHaAAAAABErEfGAA' \
                              'AAAESsSCVCE4y4RKxIg0NICpdErEjhQ4IvIkSsSUBDKx7d' \
                              'RKxJngAAAABErEn8AAAAAESsSloAAAAARKxKuQAAAABEtQ' \
                              'kRAAAAAES1CXkAAAAARLUJ4QAAAABEtQpKAAAAAES1CrJD' \
                              'JhD9RLULGkN2IZtEtQuCQ0j6M0S1C'

        self.__push = satnet_push.PushService()

    def test_push_downlink_frame(self):
        """Unit test method.
        Validates the transmission of a frame received from a remote client to
        the registered remote web clients of the push service.
        """
        if self.__verbose_testing:
            print('>>> test_push_downlink_frame')

        # Invoking the JRPC method should provoke the creation of a new element
        # in the passive messages table that should trigger the transmission of
        # the element itself through the push service.
        comms_jrpc.store_passive_message(
            groundstation_id=self.__gs_1_id,
            timestamp=misc.get_utc_timestamp(misc.get_now_utc()),
            doppler_shift=0.0,
            message=self.__short_message
        )