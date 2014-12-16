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
from services.common.testing import helpers as db_tools
from services.leop.jrpc.views import groundstations as jrpc_leop_gs


class TestLeopViews(test.TestCase):
    """Test class for the LEOP JRPC methods.
    """

    def setUp(self):

        self.__verbose_testing = False

        self.__user = db_tools.create_user_profile()
        self.__request_1 = db_tools.create_request(user_profile=self.__user)

        self.__gs_1_id = 'gs-uvigo'
        self.__gs_1 = db_tools.create_gs(
            user_profile=self.__user,
            identifier=self.__gs_1_id
        )
        self.__gs_2_id = 'gs-calpoly'
        self.__gs_2 = db_tools.create_gs(
            user_profile=self.__user,
            identifier=self.__gs_2_id
        )

        self.__admin = db_tools.create_user_profile(
            username='user_admin',
            email='admin@satnet.org',
            is_staff=True
        )
        self.__request_2 = db_tools.create_request(user_profile=self.__admin)

        if not self.__verbose_testing:
            logging.getLogger('leop').setLevel(level=logging.CRITICAL)

    def test_list_groundstations(self):
        """Unit test case.
        Checks the functioning of the JRPC method that returns the list of
        GroundStations available for the administrator to create a LEOP system.
        """

        # First step: user is not staff, access forbidden...
        try:
            jrpc_leop_gs.list_groundstations(**{ 'request': self.__request_1 })
            self.fail('User is not staff, permission should not be granted')
        except Exception:
            pass

        # Second step: user is staff, therefore access should be granted
        e_gs_list = [ self.__gs_1_id, self.__gs_2_id ]

        try:
            self.assertEquals(
                jrpc_leop_gs.list_groundstations(
                    **{'request': self.__request_2}
                ),
                e_gs_list,
                'No GroundStations should be available'
            )
        except Exception as e:
            print '>>> e = ' + str(e)
            self.fail('User is staff, permission should have been granted')