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

logger = logging.getLogger('configuration')


class TestGroundTrackPropagation(test.TestCase):
    """Unit test class.
    The following tests validate the propagation of the GroundTracks for the
    available satellites.
    """

    def setUp(self):

        super(TestGroundTrackPropagation, self).setUp()

        self.__verbose_testing = False
        self.__sc_1_id = 'sc-humsat'
        self.__sc_1_tle_id = 'HUMSAT-D'

        self.__band = db_tools.create_band()
        self.__user_profile = db_tools.create_user_profile()
        db_tools.create_sc(
            user_profile=self.__user_profile,
            identifier=self.__sc_1_id, tle_id=self.__sc_1_tle_id
        )

        if not self.__verbose_testing:
            logging.getLogger('configuration').setLevel(level=logging.CRITICAL)