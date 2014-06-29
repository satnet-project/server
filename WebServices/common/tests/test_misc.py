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

from datetime import timedelta
from django import test

from common import misc


class TestMisc(test.TestCase):

    def test_get_utc_timestamp(self):
        """
        Basic test for the generation of UTC timestamps.
        """
        test_datetime = misc.TIMESTAMP_0 + timedelta(days=1)
        actual_stamp = misc.get_utc_timestamp(test_datetime)
        expected_stamp = timedelta(days=1).days*24*3600 * 10**6

        self.assertEquals(expected_stamp, actual_stamp, 'Wrong timestamp!')