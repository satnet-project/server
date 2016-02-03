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

import json

from django import test

from services.common import helpers as db_tools
from services.configuration.ajax import views as configuration_ajax


class JRPCSegmentsTest(test.TestCase):

    def setUp(self):
        """Test setup.
        No database setup is necessary for this test.
        """
        self.__verbose_testing = False
        self.__http_request = db_tools.create_request()

    def test_geoip(self):
        """AJAX test: configuration.geoip
        Tests the AJAX method that retrieves the estimated location of the IP
        of the user.
        """
        expected_ll = {
            'longitude': '-120.4553',
            'latitude': '35.3471'
        }

        ll = configuration_ajax.user_geoip(request=self.__http_request)
        ll_json = json.loads(ll.content.decode("utf-8"))

        self.assertEqual(
            ll_json, expected_ll,
            'Expected CalPoly location = ' + str(
                expected_ll
            ) + ', found = ' + str(ll.content)
        )
