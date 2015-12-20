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

from services.common import helpers as db_tools
from services.simulation.models import groundtracks as groundtrack_models


class GroundTrackTests(test.TestCase):
    """Test class for the Groundtrack model methods
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

        self.__sc_1_id = 'xatcobeo-sc'
        self.__sc_1_tle_id = 'CANX-2'
        self.__sc_1 = db_tools.create_sc(
            user_profile=self.__user,
            identifier=self.__sc_1_id,
            tle_id=self.__sc_1_tle_id,
        )

    def test_append_new_nominal(self):
        """services.simulation.models.groundtracks: test append_new (NOMINAL)
        """
        gt = groundtrack_models.GroundTrack.objects.get(spacecraft=self.__sc_1)

        new_ts = [gt.timestamp[-1] + 1, gt.timestamp[-1] + 2]
        new_lat = [gt.latitude[-1] + 1, gt.latitude[-1] + 2]
        new_lng = [gt.longitude[-1] + 1, gt.longitude[-1] + 2]

        x_gt = {
            'timestamp': gt.timestamp + new_ts,
            'latitude': gt.latitude + new_lat,
            'longitude': gt.longitude + new_lng
        }

        r_gt = groundtrack_models.GroundTrackManager.append_new(
            gt, new_ts, new_lat, new_lng
        )

        self.assertEquals(r_gt.timestamp, x_gt['timestamp'])
        self.assertEquals(r_gt.latitude, x_gt['latitude'])
        self.assertEquals(r_gt.longitude, x_gt['longitude'])

    def test_append_new_overlap(self):
        """services.simulation.models.groundtracks: test append_new (OVERLAP)
        """
        gt = groundtrack_models.GroundTrack.objects.get(spacecraft=self.__sc_1)

        new_ts = [gt.timestamp[-1] - 1, gt.timestamp[-1] + 1]
        new_lat = [gt.latitude[-1] + 1, gt.latitude[-1] + 2]
        new_lng = [gt.longitude[-1] + 1, gt.longitude[-1] + 2]

        x_gt = {
            'timestamp': gt.timestamp + [gt.timestamp[-1] + 1],
            'latitude': gt.latitude + [gt.latitude[-1] + 2],
            'longitude': gt.longitude + [gt.longitude[-1] + 2]
        }

        r_gt = groundtrack_models.GroundTrackManager.append_new(
            gt, new_ts, new_lat, new_lng
        )

        self.assertEquals(r_gt.timestamp, x_gt['timestamp'])
        self.assertEquals(r_gt.latitude, x_gt['latitude'])
        self.assertEquals(r_gt.longitude, x_gt['longitude'])
