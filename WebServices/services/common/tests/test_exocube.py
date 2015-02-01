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
import json
import urllib2
from django.test import TestCase
from services.common import misc
from services.common.testing import helpers as db_tools
from services.communications import jrpc as comms_jrpc


EXOCUBE_URL = 'https://satcom.calpoly.edu/cgi-bin/polysat-pub/decoder.json'


class TestExocube(TestCase):
    """UNIT tests
    Validation of the remote ExoCube frames reporting service.
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
        self.__exocube_packet = 'C09C6C86A040400296966C908E861503CC450000F700' \
                                '004000011184968141931DE0000001C350000200E34D' \
                                '0501C7C79660724969000500090050006A00A374FE01' \
                                '5D74FF02776B00C56C00C31C006A001C00C36A004A00' \
                                '6B00C3000000000000966A006A006A00C2D2580000D1' \
                                '270000003E09B30400000024F400000A30000113DC00' \
                                '0DB800000425C80009E18800D513B0A3E4000000B200' \
                                '7200001E29000000000000A600A60000000000000000' \
                                '0000000000000000000067FFCD01EE00000000000000' \
                                '000000000080000000000027013700000D1A00045794' \
                                '000000004E3643502020310000000000000000000000' \
                                '00FF00000000DA6C05A0008700C300000000000000C0'
        self.__exocube_packet_b64 = base64.b64encode(self.__exocube_packet)

    def test_exocube_service(self):
        """UNIT test
        Validates the complete chain: from storing a message to invoking the
        remote ExoCube service.
        """
        if self.__verbose_testing:
            print '>>> test_exocube_service'

        self.assertEquals(
            comms_jrpc.store_passive_message(
                groundstation_id=self.__gs_1_id,
                timestamp=misc.get_utc_timestamp(misc.get_now_utc()),
                doppler_shift=0.0,
                message=self.__exocube_packet_b64
            ),
            1,
            'Message ID expected to be 1'
        )

    def ____test_exocube_wrong_mission_name(self):
        """
        Manual test to start setting up the service.
        """
        print 'test_exocube_wrong_mission_name'

        post_data_1 = {
            'mission': 'exocube',
            'live': '0',
            'name': 'anonymous',
            'callsign': 'anonymous',
            'lat': 35.3471,
            'long': -120.4553,
            'time': 1,
            'rssi': 0.0,
            'range': None,
            'az': None,
            'el': None,
            'packet': 'C09C6C86A040400296966C908E861503CC450000F700004000011184968141931DE0000001C350000200E34D0501C7C79660724969000500090050006A00A374FE015D74FF02776B00C56C00C31C006A001C00C36A004A006B00C3000000000000966A006A006A00C2D2580000D1270000003E09B30400000024F400000A30000113DC000DB800000425C80009E18800D513B0A3E4000000B2007200001E29000000000000A600A600000000000000000000000000000000000067FFCD01EE00000000000000000000000080000000000027013700000D1A00045794000000004E364350202031000000000000000000000000FF00000000DA6C05A0008700C300000000000000C0'
        }
        data = json.dumps(post_data_1)
        request = urllib2.Request(EXOCUBE_URL, data)
        request.add_header('content-type', 'application/json')
        request.add_header('content-length', str(len(data)))
        result = urllib2.urlopen(request)
        content = result.read()
        print content

    def ____test_exocube_ok(self):
        """
        Manual test to start setting up the service.
        """
        print 'test_exocube_ok'
        post_data_2 = {
            'mission': 'ExoCube',
            'live': '0',
            'name': 'anonymous',
            'callsign': 'anonymous',
            'lat': 35.3471,
            'long': -120.4553,
            'time': 1,
            'rssi': 0.0,
            'range': None,
            'az': None,
            'el': None,
            'packet': 'C09C6C86A040400296966C908E861503CC450000F700004000011184968141931DE0000001C350000200E34D0501C7C79660724969000500090050006A00A374FE015D74FF02776B00C56C00C31C006A001C00C36A004A006B00C3000000000000966A006A006A00C2D2580000D1270000003E09B30400000024F400000A30000113DC000DB800000425C80009E18800D513B0A3E4000000B2007200001E29000000000000A600A600000000000000000000000000000000000067FFCD01EE00000000000000000000000080000000000027013700000D1A00045794000000004E364350202031000000000000000000000000FF00000000DA6C05A0008700C300000000000000C0'
        }
        data = json.dumps(post_data_2)
        request = urllib2.Request(EXOCUBE_URL, data)
        request.add_header('content-type', 'application/json')
        request.add_header('content-length', str(len(data)))
        result = urllib2.urlopen(request)
        content = result.read()
        self.assertIsNotNone(content, 'A response was expected')
        print content