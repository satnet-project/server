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
from services.leop.models import launch as launch_models
from services.leop import utils as launch_utils


class TestLaunchModels(test.TestCase):

    def setUp(self):
        """Database setup for the tests.
        """

        self.__verbose_testing = False

        self.__admin = db_tools.create_user_profile(
            username='user_admin',
            email='admin@satnet.org',
            is_staff=True
        )
        self.__launch_id = 'elana'
        self.__tle_l1 = '1 27844U 03031E   15007.47529781  .00000328' \
                            '  00000-0  16930-3 0  1108'
        self.__tle_l2 = '2 27844  98.6976  18.3001 0010316  50.6742 ' \
                            '104.9393 14.21678727597601'

        if not self.__verbose_testing:
            logging.getLogger('leop').setLevel(level=logging.CRITICAL)

    def test_create_launch(self):

        #tle = launch_utils.create_cluster_tle(
        #    self.__launch_id, self.__tle_l1, self.__tle_l2
        #)
        #sc = launch_utils.create_cluster_spacecraft(
        #    user_profile=self.__admin,
        #    launch_identifier=self.__launch_id,
        #    tle_id=tle.identifier
        #)

        launch_models.Launch.objects.create(
            self.__admin,
            self.__launch_id,
            self.__tle_l1,
            self.__tle_l2
        )