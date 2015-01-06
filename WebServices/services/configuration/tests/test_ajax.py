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

from django import test
import socket
from services.common import gis
from services.common.testing import helpers as db_tools
from services.configuration.ajax import views as configuration_ajax


class JRPCSegmentsTest(test.TestCase):

    def setUp(self):
        """Test setup.
        No database setup is necessary for this test.
        """
        self.__verbose_testing = False
        self.__http_request = db_tools.create_request()

    def test_geoip(self):
        """JUnit AJAX test.
        Tests the AJAX method that retrieves the estimated location of the IP
        of the user.
        """
        expected_ll = '{"latitude": "35.347099", "longitude": "-120.455299"}'
        ll = configuration_ajax.user_geoip(request=self.__http_request)
        self.assertEquals(
            ll.content, expected_ll,
            'Expected CalPoly location = ' + str(expected_ll)
            + ', found = ' + str(ll.content)
        )

    def test_hostname_geoip(self):
        """JUnit AJAX test.
        Test that validates the functioning of the hostname_geoip AJAX method.
        """
        hostname = 'satnet.aero.calpoly.edu'
        host_ip = socket.gethostbyname(hostname)
        lat, lng = gis.get_remote_user_location(ip=host_ip)
        print '>>> name = ' + str(hostname) + ', ip = ' + str(host_ip) +\
              ', lat = ' + str(lat) + ', lng = ' + str(lng)