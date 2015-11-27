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

import pytz
from django import test

from services.common import serialization, helpers as db_tools


class TestSerialization(test.TestCase):

    def setUp(self):

        self.__verbose_testing = False

        if not self.__verbose_testing:
            logging.getLogger('configuration').setLevel(level=logging.CRITICAL)

        self.__gs_1_id = 'gs-castrelos'
        self.__gs_1_ch_1_id = 'chan-cas-1'

        self.__band = db_tools.create_band()
        self.__user_profile = db_tools.create_user_profile()
        self.__gs = db_tools.create_gs(
            user_profile=self.__user_profile, identifier=self.__gs_1_id,
        )
        self.__gs_1_ch_1 = db_tools.gs_add_channel(
            self.__gs, self.__band, self.__gs_1_ch_1_id
        )

    def test_serialize_iso8601_date(self):
        """UNIT test: services.common.serialization.serialize_iso8601_date
        Validates the function that transforms a Datetime object into a
        ISO-8601 string with Time and TimeZone.
        """
        if self.__verbose_testing:
            print('>>> test_serialize_iso8601_date:')

        dt = datetime.datetime.now(pytz.timezone('US/Pacific'))

        if dt.tzname() == 'PDT':
            birthday = dt.replace(
                year=1984, month=7, day=17,
                hour=0, minute=0, second=0, microsecond=0
            )
            expected = '1984-07-17T00:00:00-07:00'
        else:
            birthday = dt.replace(
                year=1984, month=7, day=17,
                hour=0, minute=0, second=0, microsecond=0
            )
            expected = '1984-07-17T00:00:00-08:00'

        actual = serialization.serialize_iso8601_date(birthday)

        if self.__verbose_testing:
            print('e = ' + str(expected))
            print('a = ' + str(actual))

        self.assertEqual(actual, expected, 'Wrong ISO-8601 format.')

        self.__verbose_testing = False

    def test_deserialize_iso8601_date(self):
        """UNIT test: services.common.serialization.deserialize_iso8601_date
        Validates the deserializaiton of an ISO-8601 string into a
        datetime.datetime object.
        """
        if self.__verbose_testing:
            print('>>> test_deserialize_iso8601_date:')

        if datetime.datetime.now(pytz.timezone('US/Pacific')).tzname() == 'PDT':
            in_param = '1984-07-17T00:00:00-07:00'
            expected = datetime.datetime.now(
                pytz.timezone('US/Pacific')
            ).replace(
                year=1984, month=7, day=17,
                hour=0, minute=0, second=0, microsecond=0
            )
        else:
            in_param = '1984-07-17T00:00:00-08:00'
            expected = datetime.datetime.now(
                pytz.timezone('US/Pacific')
            ).replace(
                year=1984, month=7, day=17,
                hour=0, minute=0, second=0, microsecond=0
            )

        actual = serialization.deserialize_iso8601_date(in_param)

        if self.__verbose_testing:
            print('e = ' + str(expected))
            print('a = ' + str(actual))

        self.assertEqual(actual, expected, 'Wrong ISO-8601 format.')
        self.__verbose_testing = False

    def test_serialize_iso8601_time(self):
        """UNIT test: services.common.serialization.serialize_iso8601_time
        Validates the function that transforms a Datetime object into a
        ISO-8601 string with Date and TimeZone.
        """
        if self.__verbose_testing:
            print('\n>>> test_serialize_iso8601_time:')

        dt = datetime.datetime.now(pytz.timezone('US/Pacific'))

        midnight = dt.replace(hour=0, minute=0, second=0, microsecond=0)
        if midnight.tzname() == 'PDT':
            expected = '00:00:00-07:00'
        else:
            expected = '00:00:00-08:00'

        actual = serialization.serialize_iso8601_time(midnight)

        if self.__verbose_testing:
            print('e = ' + str(expected))
            print('a = ' + str(actual))

        self.assertEqual(actual, expected, 'Wrong ISO-8601 format.')

    def test_deserialize_iso8601_time(self):
        """UNIT test: services.common.serialization.deserialize_iso8601_time
        Validates the deserializaiton of an ISO-8601 string into a
        datetime.datetime object.
        """
        if self.__verbose_testing:
            print('\n>>> test_deserialize_iso8601_time:')

        if datetime.datetime.now(pytz.timezone('US/Pacific')).tzname() == 'PDT':
            in_param = '01:00:00-07:00'
            expected = '08:00:00'
        else:
            in_param = '01:00:00-08:00'
            expected = '09:00:00'

        actual = serialization.deserialize_iso8601_time(in_param)

        if self.__verbose_testing:
            print('e = ' + str(expected))
            print('a = ' + str(actual))

        self.assertEqual(
            actual.isoformat(), expected, 'Wrong ISO-8601 format.'
        )
        self.__verbose_testing = False
