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

import urllib
import urllib2
from django.test import TestCase


EXOCUBE_URL = 'https://satcom.calpoly.edu/cgi-bin/polysat-pub/decoder.json'


class TestExocube(TestCase):

    def test_exocube(self):

        post_data = [
            ('mission', 'ExoCube'),
            ('live', '0'),
            ('name', 'anonymous'),
            ('callsign', 'anonymous'),
            ('lat', 35.3471),
            ('long', -120.4553),
            ('time', 1),
            ('rssi', 0.0),
            ('range', None),
            ('az', None),
            ('el', None),
            ('packet', 'C09C6C86A040400296966C908E861503CC450000F700004000011184968141931DE0000001C350000200E34D0501C7C79660724969000500090050006A00A374FE015D74FF02776B00C56C00C31C006A001C00C36A004A006B00C3000000000000966A006A006A00C2D2580000D1270000003E09B30400000024F400000A30000113DC000DB800000425C80009E18800D513B0A3E4000000B2007200001E29000000000000A600A600000000000000000000000000000000000067FFCD01EE00000000000000000000000080000000000027013700000D1A00045794000000004E364350202031000000000000000000000000FF00000000DA6C05A0008700C300000000000000C0')
        ]
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
        #request = urllib2.Request(EXOCUBE_URL)
        request = urllib2.Request('http://localhost:8080')
        request.add_header('content-type', 'application/json')
        #request.data = {"mission":"ExoCube","live":0,"name":"anonymous","callsign":"anonymous","lat":35.3471,"long":-120.4553,"time":1,"rssi":0.0,"range":'null',"az":'null',"el":'null',"packet":"C09C6C86A040400296966C908E861503CC450000F700004000011184968141931DE0000001C350000200E34D0501C7C79660724969000500090050006A00A374FE015D74FF02776B00C56C00C31C006A001C00C36A004A006B00C3000000000000966A006A006A00C2D2580000D1270000003E09B30400000024F400000A30000113DC000DB800000425C80009E18800D513B0A3E4000000B2007200001E29000000000000A600A600000000000000000000000000000000000067FFCD01EE00000000000000000000000080000000000027013700000D1A00045794000000004E364350202031000000000000000000000000FF00000000DA6C05A0008700C300000000000000C0"}
        request.data = str(post_data_2)
        print 'XXX = ' + str(post_data_2)
        result = urllib2.urlopen(request)
        content = result.read()
        print content