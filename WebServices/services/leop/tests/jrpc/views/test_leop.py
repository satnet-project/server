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

import datadiff
from django import test
from django.core import exceptions as django_ex
import logging
from services.common import misc
from services.common.testing import helpers as db_tools
from services.leop.models import leop as leop_models
from services.leop.jrpc.views import cluster as cluster_jrpc, ufo as ufo_jrpc
from services.leop.jrpc.serializers import cluster as cluster_serial


class TestLeopViews(test.TestCase):
    """Test class for the LEOP JRPC methods.
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

    def test_list_groundstations(self):
        """Unit test case.
        Checks the functioning of the JRPC method that returns the list of
        GroundStations available for the administrator to create a LEOP system.
        """
        # Permissions basic test, no request, no permission
        try:
            cluster_jrpc.list_groundstations('FAKE_ID', **{'request': None})
            self.fail('No request added, permission should not be granted')
        except django_ex.PermissionDenied:
            pass

        # First step: user is not staff, access forbidden...
        try:
            cluster_jrpc.list_groundstations(
                self.__leop_id, **{'request': self.__request_1}
            )
            self.fail('User is not staff, permission should not be granted')
        except django_ex.PermissionDenied:
            pass

        # Second step: user is staff, therefore access should be granted
        e_gs = {
            cluster_serial.JRPC_K_AVAILABLE_GS: [
                self.__gs_1_id, self.__gs_2_id
            ],
            cluster_serial.JRPC_K_IN_USE_GS: []
        }

        try:
            a_gs = cluster_jrpc.list_groundstations(
                self.__leop_id, **{'request': self.__request_2}
            )
            self.assertEquals(
                a_gs, e_gs, 'Unexpected result! diff = ' + str(
                    datadiff.diff(a_gs, e_gs)
                )
            )
        except django_ex.PermissionDenied:
            self.fail('User is staff, permission should have been granted')

        # Third step: one of the ground stations is added to the cluster, it
        # should not appear as available, only as in use.
        self.__leop.add_ground_stations(identifiers=[self.__gs_1_id])
        e_gs = {
            cluster_serial.JRPC_K_AVAILABLE_GS: [self.__gs_2_id],
            cluster_serial.JRPC_K_IN_USE_GS: [self.__gs_1_id]
        }
        a_gs = cluster_jrpc.list_groundstations(
            self.__leop_id, **{'request': self.__request_2}
        )

        self.assertEquals(
            a_gs, e_gs, 'Unexpected result! diff = ' + str(
                datadiff.diff(a_gs, e_gs)
            )
        )

    def test_add_groundstations(self):
        """Unit test case.
        Validates the addition of an array of GroundStations to a given LEOP
        cluster.
        """

        # Permissions test (1): no request, no permission
        try:
            cluster_jrpc.add_groundstations(
                'FAKE_ID', None, **{'request': None}
            )
            self.fail('No request added, permission should not be granted')
        except django_ex.PermissionDenied:
            pass
        # Permissions test (2): user not authorized
        try:
            cluster_jrpc.add_groundstations(
                'FAKE', None, **{'request': self.__request_1}
            )
            self.fail('No request added, permission should not be granted')
        except django_ex.PermissionDenied:
            pass
        # Basic parameters test (1)
        try:
            cluster_jrpc.add_groundstations(
                'FAKE', None, **{'request': self.__request_2}
            )
            self.fail('The leop cluster does not exist')
        except leop_models.LEOP.DoesNotExist:
            pass
        # Basic parameters test (2)
        actual = cluster_jrpc.add_groundstations(
            self.__leop_id, None, **{'request': self.__request_2}
        )
        expected = {cluster_serial.JRPC_K_LEOP_ID: self.__leop_id}
        self.assertEquals(
            actual, expected,
            'Result differs, diff = ' + str(datadiff.diff(actual, expected))
        )
        # Basic parameters test (3)
        actual = cluster_jrpc.add_groundstations(
            self.__leop_id, [], **{'request': self.__request_2}
        )
        expected = {cluster_serial.JRPC_K_LEOP_ID: self.__leop_id}
        self.assertEquals(
            actual, expected,
            'Result differs, diff = ' + str(datadiff.diff(actual, expected))
        )

        # GroundStations array []
        gss = [self.__gs_1_id, self.__gs_2_id]
        actual = cluster_jrpc.add_groundstations(
            self.__leop_id, gss, **{'request': self.__request_2}
        )
        expected = {cluster_serial.JRPC_K_LEOP_ID: self.__leop_id}
        self.assertEquals(
            actual, expected,
            'Result differs, diff = ' + str(datadiff.diff(actual, expected))
        )

        cluster = leop_models.LEOP.objects.get(identifier=self.__leop_id)
        self.assertEquals(
            len(cluster.groundstations.all()), 2,
            'Two groundstations should be part of this cluster object'
        )

    def test_remove_groundstations(self):
        """Unit test case.
        Validates the removal of an array of GroundStations to a given LEOP
        cluster.
        """

        # Permissions test (1): no request, no permission
        try:
            cluster_jrpc.remove_groundstations(
                'FAKE_ID', None, **{'request': None}
            )
            self.fail('No request added, permission should not be granted')
        except django_ex.PermissionDenied:
            pass
        # Permissions test (2): user not authorized
        try:
            cluster_jrpc.remove_groundstations(
                'FAKE', None, **{'request': self.__request_1}
            )
            self.fail('No request added, permission should not be granted')
        except django_ex.PermissionDenied:
            pass
        # Basic parameters test (1)
        try:
            cluster_jrpc.remove_groundstations(
                'FAKE', None, **{'request': self.__request_2}
            )
            self.fail('The leop cluster does not exist')
        except leop_models.LEOP.DoesNotExist:
            pass
        # Basic parameters test (2)
        actual = cluster_jrpc.remove_groundstations(
            self.__leop_id, None, **{'request': self.__request_2}
        )
        expected = {cluster_serial.JRPC_K_LEOP_ID: self.__leop_id}
        self.assertEquals(
            actual, expected,
            'Result differs, diff = ' + str(datadiff.diff(actual, expected))
        )
        # Basic parameters test (3)
        actual = cluster_jrpc.remove_groundstations(
            self.__leop_id, [], **{'request': self.__request_2}
        )
        expected = {cluster_serial.JRPC_K_LEOP_ID: self.__leop_id}
        self.assertEquals(
            actual, expected,
            'Result differs, diff = ' + str(datadiff.diff(actual, expected))
        )

        # First, we add two groundstations to the cluster and we try to remove
        # them later.
        gss = [self.__gs_1_id, self.__gs_2_id]
        cluster_jrpc.add_groundstations(
            self.__leop_id, gss, **{'request': self.__request_2}
        )
        cluster = leop_models.LEOP.objects.get(identifier=self.__leop_id)
        self.assertEquals(
            len(cluster.groundstations.all()), 2,
            'Two groundstations should be part of this cluster object'
        )

        actual = cluster_jrpc.remove_groundstations(
            self.__leop_id, gss, **{'request': self.__request_2}
        )
        expected = {cluster_serial.JRPC_K_LEOP_ID: self.__leop_id}
        self.assertEquals(
            actual, expected,
            'Result differs, diff = ' + str(datadiff.diff(actual, expected))
        )
        self.assertEquals(
            len(cluster.groundstations.all()), 0,
            'No groundstations should be part of this cluster object'
        )

    def test_get_configuration(self):
        """JRPC unit test case
        Validation of the JRPC method that permits obtaining the
        configuration for a given LEOP cluster.
        """
        try:
            cluster_jrpc.get_configuration('')
            self.fail('LEOP doesnt exist, an exception should have been raised')
        except leop_models.LEOP.DoesNotExist:
            pass

        # 1) No ufos
        a_cfg = cluster_jrpc.get_configuration(self.__leop_id)
        e_cfg = {
            cluster_serial.JRPC_K_LEOP_ID: str(self.__leop_id),
            cluster_serial.JRPC_K_TLE: {
                cluster_serial.JRPC_K_TLE_L1:
                    '1 27844U 03031E   15007.47529781  .00000328'
                    '  00000-0  16930-3 0  1108',
                cluster_serial.JRPC_K_TLE_L2:
                    '2 27844  98.6976  18.3001 0010316  50.6742 '
                    '104.9393 14.21678727597601',
            },
            cluster_serial.JRPC_K_UFOS: [],
            cluster_serial.JRPC_K_IDENTIFIED: []
        }
        self.assertEquals(
            a_cfg, e_cfg, 'Configurations differ, diff = ' + str(
                datadiff.diff(a_cfg, e_cfg)
            )
        )

        # 2) 1 ufo
        ufo_jrpc.add(self.__leop_id, 1)
        a_cfg = cluster_jrpc.get_configuration(self.__leop_id)
        e_cfg = {
            cluster_serial.JRPC_K_LEOP_ID: str(self.__leop_id),
            cluster_serial.JRPC_K_TLE: {
                cluster_serial.JRPC_K_TLE_L1:
                    '1 27844U 03031E   15007.47529781  .00000328'
                    '  00000-0  16930-3 0  1108',
                cluster_serial.JRPC_K_TLE_L2:
                    '2 27844  98.6976  18.3001 0010316  50.6742 '
                    '104.9393 14.21678727597601',
            },
            cluster_serial.JRPC_K_UFOS: [
                {cluster_serial.JRPC_K_UFO_ID: '1'}
            ],
            cluster_serial.JRPC_K_IDENTIFIED: []
        }
        self.assertEquals(
            a_cfg, e_cfg, 'Configurations differ, diff = ' + str(
                datadiff.diff(a_cfg, e_cfg)
            )
        )

        # 3) 1 ufo, 1 identified
        ufo_jrpc.add(self.__leop_id, 2)
        ufo_jrpc.identify(
            self.__leop_id,
            self.__ufo_id, self.__ufo_callsign,
            self.__ufo_tle_l1, self.__ufo_tle_l2,
            request=self.__request_1
        )

        a_cfg = cluster_jrpc.get_configuration(self.__leop_id)
        e_cfg = {
            cluster_serial.JRPC_K_LEOP_ID: str(self.__leop_id),
            cluster_serial.JRPC_K_TLE: {
                cluster_serial.JRPC_K_TLE_L1:
                    '1 27844U 03031E   15007.47529781  .00000328'
                    '  00000-0  16930-3 0  1108',
                cluster_serial.JRPC_K_TLE_L2:
                    '2 27844  98.6976  18.3001 0010316  50.6742 '
                    '104.9393 14.21678727597601',
            },
            cluster_serial.JRPC_K_UFOS: [
                {cluster_serial.JRPC_K_UFO_ID: '2'}
            ],
            cluster_serial.JRPC_K_IDENTIFIED: [{
                cluster_serial.JRPC_K_UFO_ID: '1',
                cluster_serial.JRPC_K_CALLSIGN: str(self.__ufo_callsign),
                cluster_serial.JRPC_K_TLE: {
                    cluster_serial.JRPC_K_TLE_L1:
                        '1 27844U 03031E   15007.47529781  .00000328'
                        '  00000-0  16930-3 0  1108',
                    cluster_serial.JRPC_K_TLE_L2:
                        '2 27844  98.6976  18.3001 0010316  50.6742 '
                        '104.9393 14.21678727597601',
                }
            }]
        }
        self.assertEquals(
            a_cfg, e_cfg, 'Configurations differ, diff = ' + str(
                datadiff.diff(a_cfg, e_cfg)
            )
        )

        # 4) 2 ufos
        ufo_jrpc.forget(self.__leop_id, self.__ufo_id)
        a_cfg = cluster_jrpc.get_configuration(self.__leop_id)
        e_cfg = {
            cluster_serial.JRPC_K_LEOP_ID: str(self.__leop_id),
            cluster_serial.JRPC_K_TLE: {
                cluster_serial.JRPC_K_TLE_L1:
                    '1 27844U 03031E   15007.47529781  .00000328'
                    '  00000-0  16930-3 0  1108',
                cluster_serial.JRPC_K_TLE_L2:
                    '2 27844  98.6976  18.3001 0010316  50.6742 '
                    '104.9393 14.21678727597601',
            },
            cluster_serial.JRPC_K_UFOS: [
                {cluster_serial.JRPC_K_UFO_ID: '2'},
                {cluster_serial.JRPC_K_UFO_ID: '1'}
            ],
            cluster_serial.JRPC_K_IDENTIFIED: []
        }

        if self.__verbose_testing:
            misc.print_dictionary(a_cfg)
            misc.print_dictionary(e_cfg)

        self.assertEquals(
            a_cfg, e_cfg, 'Configurations differ, diff = ' + str(
                datadiff.diff(a_cfg, e_cfg)
            )
        )