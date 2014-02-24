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

from django.test import TestCase
from configuration.utils import get_remote_user_location
from configuration.utils import print_dictionary
from configuration.tests.utils import testdb_create_jrpc_once_rule


class UtilsTest(TestCase):
    
    inp_grul = "129.65.136.182"
    out_grul_latitude = 35.347099
    out_grul_longitude = -120.455299
    
    def test_get_remote_user_location(self):
        """
        Function test.

        This test checks whether the "testing" function is capable of getting
        the location information for a given user by using the WebService from
        GeoPlugin's website.        
        
        """
        
        latitude, longitude = get_remote_user_location(ip=self.inp_grul)
        
        self.assertAlmostEqual(float(latitude),
                               self.out_grul_latitude, places=4,
                               msg="Wrong latitude!")
        self.assertAlmostEqual(float(longitude),
                               self.out_grul_longitude, places=4,
                               msg="Wrong longitude!")

    def test_print_dictionary(self):
        """
        This function tests the function from the utils module that
        recursively prints out the contents of a dictionary object that may
        or may not have additional dictionary objects nested.
        """
        jrpc_dict = testdb_create_jrpc_once_rule()
        print_dictionary(jrpc_dict)
