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
import datadiff
from django import test as django_test
from services.common import ax25


class AX25Tests(django_test.TestCase):
    """Unit Test
    Validate the library for AX25 packet enconding/decoding.
    """

    __ax25_frame_1 = '7E96709A9A9E40E0AE8468948C9261F0HHHH7E'
    __ax25_frame_1_b64 = base64.b64encode(__ax25_frame_1)

    def test_decode_ax25(self):

        p = ax25.AX25Packet.decode_base64(self.__ax25_frame_1_b64)
        print '>>> p = ' + p.__unicode__()

        expected = {
            'raw_packet': '7E96709A9A9E40E0AE8468948C9261F0HHHH7E',
            'start_flag': '7E',
            'destination': '96709A9A9E40E0',
            'source': 'AE8468948C9261',
            'end_flag': '7E'
        }

        actual = p.as_dictionary()
        self.assertEquals(
            actual, expected,
            'Results differ, diff = ' + str(datadiff.diff(actual, expected))
        )