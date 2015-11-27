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

from django.test import TestCase

from services.accounts import models as account_models
from services.accounts import utils as account_utils
from services.common import helpers as db_tools


class UtilsTest(TestCase):

    inp_guo = {"xxx": "aaa", "op_43": "verify", "opX_40": "wrong"}
    out_guo = {"43": "verify"}
    
    def test_get_user_operations(self):
        """UNIT test: services.accounts.utils - user ID and operations
        Should extract all user_id and operations from the POST request
        """
        result = account_utils.get_user_operations(self.inp_guo)
        self.assertCountEqual(result, self.out_guo, "Wrong result!")

    def test_random_username(self):
        """UNIT test: services.accounts.utils - random username generation
        Should generate random user names
        """
        name_1 = account_utils.generate_random_username()
        name_2 = account_utils.generate_random_username()

        self.assertNotEqual(
            name_1, name_2, 'Generated names should be different'
        )

    def test_get_user(self):
        """UNIT test: services.accounts.utils - user from HTTP request
        Should extract the user object and username from a HTTP request
        """
        username = 'test-user'
        user_profile = db_tools.create_user_profile(
            username=username
        )
        http_request = db_tools.create_request(user_profile=user_profile)
        username_2 = 'another'
        user_profile_2 = db_tools.create_user_profile(
            username=username_2
        )

        self.assertEqual(
            account_models.get_user(
                http_request=http_request,
                permissions_flag=False,
                test_username=username,
                testing_flag=False
            ),
            (user_profile, username),
            'Error extracing the user data from HTTP request'
        )

        self.assertEqual(
            account_models.get_user(
                http_request=http_request,
                permissions_flag=False,
                test_username=username_2,
                testing_flag=False
            ),
            (user_profile_2, username_2),
            'Error extracting the user data when no HTTP request is given'
        )
