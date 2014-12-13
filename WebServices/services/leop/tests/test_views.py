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

import logging
from django import test
from services.accounts import models as account_models
from services.common.testing import helpers as db_tools
from services.leop import models as leop_models, views as leop_views


class TestLeopViews(test.TestCase):
    """Test class for the LEOP views.
    """

    def setUp(self):

        self.__verbose_testing = False
        self.__request = db_tools.create_request()
        self.__user_2 = db_tools.create_user_profile(username='User2')

        if not self.__verbose_testing:
            logging.getLogger('leop').setLevel(level=logging.CRITICAL)

    def test_get_queryset(self):
        """Unit test case.
        Simply checks this method of the LeopManagementView since it had to
        be implemented slightly different than what expected beforehand.
        """
        self.__leop_user_2 = leop_models.Leop.objects.create(
            admin=account_models.UserProfile.objects.get(
                username=self.__user_2.username
            )
        )

        cm = leop_views.LeopManagementView()
        cm.request = self.__request
        qs = cm.get_queryset()
        self.assertEquals(len(qs), 0 , 'No LEOPs are owned by test user.')

        cm.request = db_tools.create_request(user_profile=self.__user_2)
        qs_2 = cm.get_queryset()
        self.assertEquals(len(qs_2), 1 , '1 LEOP is owned by test user.')