"""
Main tests for the configuration Django application.
"""

from django.test import TestCase
from django.test.client import Client

from configuration.utils import get_remote_user_location

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
        
        self.assertAlmostEqual(float(latitude), \
                                self.out_grul_latitude, places=4, \
                                msg="Wrong latitude!")
        self.assertAlmostEqual(float(longitude), \
                                self.out_grul_longitude, places=4, \
                                msg="Wrong longitude!")
        
