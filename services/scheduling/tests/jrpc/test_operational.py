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

from django import test as django_test

from services.common import misc as common_misc
from services.common import serialization as common_serializers
from services.scheduling.jrpc.views.operational import slots as scheduling_slots


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

        if not self.__verbose_testing:
            logging.getLogger('common').setLevel(level=logging.CRITICAL)
            logging.getLogger('configuration').setLevel(level=logging.CRITICAL)
            logging.getLogger('scheduling').setLevel(level=logging.CRITICAL)

    def test_1_test_slot(self):
        """Basic TEST slot test
        """
        if self.__verbose_testing:
            print('##### test_1_test_slot')

        s_time = common_misc.get_now_utc(no_microseconds=True)
        e_time = s_time + datetime.timedelta(hours=2)

        self.assertEquals(
            scheduling_slots.get_slot(self.__test_slot_id), {
                'state': 'TEST',
                'gs_username': 'test-gs-user',
                'sc_username': 'test-sc-user',
                'starting_time':
                    common_serializers.serialize_iso8601_date(
                        common_misc.get_now_utc()
                    ),
                'ending_time':
                    common_serializers.serialize_iso8601_date(
                        common_misc.get_now_utc() + datetime.timedelta(hours=2)
                    ),
            }
        )
