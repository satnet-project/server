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

from datetime import timedelta as py_timedelta
from django import test
import logging
logger = logging.getLogger('simulation')

from services.common import helpers as sn_helpers
from services.common import misc as sn_misc
from services.simulation.models import groundtracks as groundtrack_models


class GroundTrackTests(test.TestCase):
    """Test class for the Groundtrack model methods
    """

    def setUp(self):
        """Database setup for the tests.
        """
        self.__verbose_testing = False

        self.__user = sn_helpers.create_user_profile()
        self.__request_1 = sn_helpers.create_request(user_profile=self.__user)

        self.__gs_1_id = 'gs-uvigo'
        self.__gs_1 = sn_helpers.create_gs(
            user_profile=self.__user,
            identifier=self.__gs_1_id
        )

        self.__sc_1_id = 'xatcobeo-sc'
        self.__sc_1_tle_id = 'CANX-2'
        self.__sc_1 = sn_helpers.create_sc(
            user_profile=self.__user,
            identifier=self.__sc_1_id,
            tle_id=self.__sc_1_tle_id,
        )

    def test_read_write(self):
        """services.simulation.models.groundtracks: read + write
        """
        gt = groundtrack_models.GroundTrack.objects.get(spacecraft=self.__sc_1)

        ts, la, lo = gt.read()
        ts[1] = 0
        la[1] = 0
        lo[1] = 0
        gt.write(ts, la, lo)
        ts2, la2, lo2 = gt.read()
        self.assertEquals(ts, ts2)
        self.assertEquals(la, la2)
        self.assertEquals(lo, lo2)

        gt.write(ts2[2:], la2[2:], lo2[2:])
        ts3, la3, lo3 = gt.read()
        self.assertEquals(ts[2:], ts3)
        self.assertEquals(la[2:], la3)
        self.assertEquals(lo[2:], lo3)

    def test_append_new_nominal(self):
        """services.simulation.models.groundtracks: append (NOMINAL)
        """
        gt = groundtrack_models.GroundTrack.objects.get(spacecraft=self.__sc_1)
        tss, las, lns = gt.read()

        new_ts = [tss[-1] + 1, tss[-1] + 2]
        new_lat = [las[-1] + 1, las[-1] + 2]
        new_lng = [lns[-1] + 1, lns[-1] + 2]

        x_gt = {
            'timestamp': tss + new_ts,
            'latitude': las + new_lat,
            'longitude': lns + new_lng
        }

        gt.append(new_ts, new_lat, new_lng)
        r_tss, r_las, r_lns = gt.read()

        self.assertEquals(r_tss, x_gt['timestamp'])
        self.assertEquals(r_las, x_gt['latitude'])
        self.assertEquals(r_lns, x_gt['longitude'])

    def test_append_new_overlap(self):
        """services.simulation.models.groundtracks: test append_new (OVERLAP)
        """
        gt = groundtrack_models.GroundTrack.objects.get(spacecraft=self.__sc_1)
        tss, las, lns = gt.read()

        new_ts = [tss[-1] - 1, tss[-1] + 1]
        new_lat = [las[-1] + 1, las[-1] + 2]
        new_lng = [lns[-1] + 1, lns[-1] + 2]

        x_gt = {
            'timestamp': tss + [tss[-1] + 1],
            'latitude': las + [las[-1] + 2],
            'longitude': lns + [lns[-1] + 2]
        }

        gt.append(new_ts, new_lat, new_lng)
        r_tss, r_las, r_lns = gt.read()

        self.assertEquals(r_tss, x_gt['timestamp'])
        self.assertEquals(r_las, x_gt['latitude'])
        self.assertEquals(r_lns, x_gt['longitude'])

    def test_groundtracks_reboot(self):
        """UNIT test: services.simulation.models - gts generation REBOOT
        """

        # 1) consecutive propagations should not be permitted
        logger.debug('#### FIRST PART OF THE TEST, CURRENT INTERVAL')

        groundtrack_models.GroundTrack.objects.propagate()

        sc_gts_n_1 = groundtrack_models.GroundTrack.objects.get(
            spacecraft=self.__sc_1
        ).len()
        groundtrack_models.GroundTrack.objects.propagate()

        sc_gts_n_2 = groundtrack_models.GroundTrack.objects.get(
            spacecraft=self.__sc_1
        ).len()
        self.assertEquals(sc_gts_n_1, sc_gts_n_2)

        # 2) now, we change the interval of application for avoiding reboots
        logger.debug('#### SECOND PART OF THE TEST, FUTURE INTERVAL')

        interval = (
            sn_misc.get_next_midnight() + py_timedelta(days=3),
            sn_misc.get_next_midnight() + py_timedelta(days=4)
        )

        groundtrack_models.GroundTrack.objects.propagate(interval=interval)
        sc_gts_n_3 = groundtrack_models.GroundTrack.objects.get(
            spacecraft=self.__sc_1
        ).len()
        self.assertGreater(sc_gts_n_3, sc_gts_n_2)

        groundtrack_models.GroundTrack.objects.propagate(interval=interval)
        sc_gts_n_4 = groundtrack_models.GroundTrack.objects.get(
            spacecraft=self.__sc_1
        ).len()
        self.assertEquals(sc_gts_n_4, sc_gts_n_3)
