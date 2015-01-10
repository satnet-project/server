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
import logging
from services.common.testing import helpers as db_tools


class TestUfoModels(test.TestCase):
    """Test class for the UFO model methods.
    """

    def setUp(self):
        """Database setup for the tests.
        """

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

        self.__leop_id = 'leop_cluster_4testing'
        self.__leop = db_tools.create_cluster(
            admin=self.__admin, identifier=self.__leop_id
        )

        self.__ufo_id = 1
        self.__ufo_callsign = 'SCLLY'
        self.__ufo_tle_l1 = '1 27844U 03031E   15007.47529781  .00000328' \
                            '  00000-0  16930-3 0  1108'
        self.__ufo_tle_l2 = '2 27844  98.6976  18.3001 0010316  50.6742 ' \
                            '104.9393 14.21678727597601'

        if not self.__verbose_testing:
            logging.getLogger('leop').setLevel(level=logging.CRITICAL)

    def test_update(self):
        """UNIT method test
        """
        pass