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
#from services.common import misc
from services.common.testing import helpers as db_tools
from services.leop.models import launch as launch_models
from services.leop.jrpc.views import launch as launch_jrpc
from services.leop.jrpc.serializers import launch as launch_serial


class TestLaunchViews(test.TestCase):
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
        self.__leop = db_tools.create_launch(
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
            launch_jrpc.list_groundstations('FAKE_ID', **{'request': None})
            self.fail('No request added, permission should not be granted')
        except django_ex.PermissionDenied:
            pass

        # First step: user is not staff, access forbidden...
        try:
            launch_jrpc.list_groundstations(
                self.__leop_id, **{'request': self.__request_1}
            )
            self.fail('User is not staff, permission should not be granted')
        except django_ex.PermissionDenied:
            pass

        # Second step: user is staff, therefore access should be granted
        e_gs = {
            launch_serial.JRPC_K_AVAILABLE_GS: [
                self.__gs_1_id, self.__gs_2_id
            ],
            launch_serial.JRPC_K_IN_USE_GS: []
        }

        try:
            a_gs = launch_jrpc.list_groundstations(
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
        launch_jrpc.add_groundstations(
            self.__leop_id, groundstations=[self.__gs_1_id],
            **{'request': self.__request_2}
            )
        e_gs = {
            launch_serial.JRPC_K_AVAILABLE_GS: [self.__gs_2_id],
            launch_serial.JRPC_K_IN_USE_GS: [self.__gs_1_id]
        }
        a_gs = launch_jrpc.list_groundstations(
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
            launch_jrpc.add_groundstations(
                'FAKE_ID', None, **{'request': None}
            )
            self.fail('No request added, permission should not be granted')
        except django_ex.PermissionDenied:
            pass
        # Permissions test (2): user not authorized
        try:
            launch_jrpc.add_groundstations(
                'FAKE', None, **{'request': self.__request_1}
            )
            self.fail('No request added, permission should not be granted')
        except django_ex.PermissionDenied:
            pass
        # Basic parameters test (1)
        try:
            launch_jrpc.add_groundstations(
                'FAKE', ['fake'], **{'request': self.__request_2}
            )
            self.fail('The leop cluster does not exist')
        except launch_models.Launch.DoesNotExist:
            pass
        # Basic parameters test (2)
        try:
            launch_jrpc.add_groundstations(
                self.__leop_id, None, **{'request': self.__request_2}
            )
            self.fail('Groundstations is an empty array')
        except Exception:
            pass

        # GroundStations array []
        gss = [self.__gs_1_id, self.__gs_2_id]
        actual = launch_jrpc.add_groundstations(
            self.__leop_id, gss, **{'request': self.__request_2}
        )
        expected = {launch_serial.JRPC_K_LEOP_ID: self.__leop_id}
        self.assertEquals(
            actual, expected,
            'Result differs, diff = ' + str(datadiff.diff(actual, expected))
        )

        cluster = launch_models.Launch.objects.get(identifier=self.__leop_id)
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
            launch_jrpc.remove_groundstations(
                'FAKE_ID', None, **{'request': None}
            )
            self.fail('No request added, permission should not be granted')
        except django_ex.PermissionDenied:
            pass
        # Permissions test (2): user not authorized
        try:
            launch_jrpc.remove_groundstations(
                'FAKE', None, **{'request': self.__request_1}
            )
            self.fail('No request added, permission should not be granted')
        except django_ex.PermissionDenied:
            pass
        # Basic parameters test (1)
        try:
            launch_jrpc.remove_groundstations(
                'FAKE', ['fake'], **{'request': self.__request_2}
            )
            self.fail('The leop cluster does not exist')
        except launch_models.Launch.DoesNotExist:
            pass
        # Basic parameters test (2)
        actual = launch_jrpc.remove_groundstations(
            self.__leop_id, None, **{'request': self.__request_2}
        )
        expected = {launch_serial.JRPC_K_LEOP_ID: self.__leop_id}
        self.assertEquals(
            actual, expected,
            'Result differs, diff = ' + str(datadiff.diff(actual, expected))
        )
        # Basic parameters test (3)
        actual = launch_jrpc.remove_groundstations(
            self.__leop_id, [], **{'request': self.__request_2}
        )
        expected = {launch_serial.JRPC_K_LEOP_ID: self.__leop_id}
        self.assertEquals(
            actual, expected,
            'Result differs, diff = ' + str(datadiff.diff(actual, expected))
        )

        # First, we add two groundstations to the cluster and we try to remove
        # them later.
        gss = [self.__gs_1_id, self.__gs_2_id]
        launch_jrpc.add_groundstations(
            self.__leop_id, gss, **{'request': self.__request_2}
        )
        cluster = launch_models.Launch.objects.get(identifier=self.__leop_id)
        self.assertEquals(
            len(cluster.groundstations.all()), 2,
            'Two groundstations should be part of this cluster object'
        )

        self.assertTrue(
            launch_jrpc.remove_groundstations(
                self.__leop_id, gss, **{'request': self.__request_2}
            ),
            'Should have returned True'
        )
        self.assertEquals(
            len(cluster.groundstations.all()), 0,
            'No groundstations should be part of this cluster object'
        )

    def test_add_unknown(self):
        """JRPC unit test case
        Validation of the remote addition of a new unknown object to the list.
        """
        try:
            launch_jrpc.add_unknown(
                self.__leop_id, None, **{'request': self.__request_2}
            )
            self.fail('An exception should have been thrown, id < 0')
        except Exception:
            pass
        try:
            launch_jrpc.add_unknown(
                self.__leop_id, -1, **{'request': self.__request_2}
            )
            self.fail('An exception should have been thrown, id < 0')
        except Exception:
            pass

        self.assertEquals(
            launch_jrpc.add_unknown(
                self.__leop_id, 1, **{'request': self.__request_2}
            ), 1,
            'Identifiers must match'
        )

        a_list = [
            a.identifier for a in launch_models.Launch.objects.get(
                identifier=self.__leop_id
            ).unknown_objects.all()
        ]
        e_list = [1]
        self.assertEquals(
            a_list, e_list, 'Data differs in the DB, diff = ' + str(
                datadiff.diff(a_list, e_list)
            )
        )

    def test_remove_unknown(self):
        """JRPC unit test
        Validates the removal of an unknown object from the list
        """
        try:
            launch_jrpc.remove_unknown(self.__leop_id, None)
            self.fail('An exception should have been thrown, id < 0')
        except Exception:
            pass
        try:
            launch_jrpc.remove_unknown(self.__leop_id, -1)
            self.fail('An exception should have been thrown, id < 0')
        except Exception:
            pass
        try:
            launch_jrpc.remove_unknown(self.__leop_id, 2)
            self.fail('An exception should have been thrown, wrong id')
        except Exception:
            pass

        self.assertEquals(
            launch_jrpc.add_unknown(
                self.__leop_id, 1,  **{'request': self.__request_2}
            ), 1,
            'Identifiers must match'
        )
        self.assertTrue(
            launch_jrpc.remove_unknown(
                self.__leop_id, 1,  **{'request': self.__request_2}
            ),
            'Should have returned True'
        )
        self.assertEqual(
            len(launch_models.Launch.objects.get(
                identifier=self.__leop_id
            ).unknown_objects.all()), 0,
            'List must be empty'
        )

    def test_get_configuration(self):
        """JRPC unit test case
        Validation of the JRPC method that permits obtaining the
        configuration for a given LEOP cluster.
        """
        try:
            launch_jrpc.get_configuration('')
            self.fail('LEOP doesnt exist, an exception should have been raised')
        except launch_models.Launch.DoesNotExist:
            pass

        # 1) No ufos
        a_cfg = launch_jrpc.get_configuration(self.__leop_id)
        e_cfg = {
            launch_serial.JRPC_K_LEOP_ID: str(self.__leop_id),
            launch_serial.JRPC_K_TLE: {
                launch_serial.JRPC_K_TLE_L1:
                    '1 27844U 03031E   15007.47529781  .00000328'
                    '  00000-0  16930-3 0  1108',
                launch_serial.JRPC_K_TLE_L2:
                    '2 27844  98.6976  18.3001 0010316  50.6742 '
                    '104.9393 14.21678727597601',
            },
            launch_serial.JRPC_K_UNKNOWN_OBJECTS: [],
            launch_serial.JRPC_K_IDENTIFIED_OBJECTS: []
        }
        self.assertEquals(
            a_cfg, e_cfg, 'Configurations differ, diff = ' + str(
                datadiff.diff(a_cfg, e_cfg)
            )
        )

        # 2) 1 ufo
        launch_jrpc.add_unknown(
            self.__leop_id, 1,  **{'request': self.__request_2}
        )
        a_cfg = launch_jrpc.get_configuration(self.__leop_id)
        e_cfg = {
            launch_serial.JRPC_K_LEOP_ID: str(self.__leop_id),
            launch_serial.JRPC_K_TLE: {
                launch_serial.JRPC_K_TLE_L1:
                    '1 27844U 03031E   15007.47529781  .00000328'
                    '  00000-0  16930-3 0  1108',
                launch_serial.JRPC_K_TLE_L2:
                    '2 27844  98.6976  18.3001 0010316  50.6742 '
                    '104.9393 14.21678727597601',
            },
            launch_serial.JRPC_K_UNKNOWN_OBJECTS: [
                {launch_serial.JRPC_K_OBJECT_ID: '1'}
            ],
            launch_serial.JRPC_K_IDENTIFIED_OBJECTS: []
        }
        self.assertEquals(
            a_cfg, e_cfg, 'Configurations differ, diff = ' + str(
                datadiff.diff(a_cfg, e_cfg)
            )
        )

        """
        # 3) 1 ufo, 1 identified
        launch_jrpc.add_unknown(
            self.__leop_id, 2,  **{'request': self.__request_2}
        )
        launch_jrpc.identify(
            self.__leop_id,
            self.__ufo_id, self.__ufo_callsign,
            self.__ufo_tle_l1, self.__ufo_tle_l2,
            request=self.__request_2
        )

        a_cfg = launch_jrpc.get_configuration(self.__leop_id)
        e_cfg = {
            launch_serial.JRPC_K_LEOP_ID: str(self.__leop_id),
            launch_serial.JRPC_K_TLE: {
                launch_serial.JRPC_K_TLE_L1:
                    '1 27844U 03031E   15007.47529781  .00000328'
                    '  00000-0  16930-3 0  1108',
                launch_serial.JRPC_K_TLE_L2:
                    '2 27844  98.6976  18.3001 0010316  50.6742 '
                    '104.9393 14.21678727597601',
            },
            launch_serial.JRPC_K_UNKNOWN_OBJECTS: [
                {launch_serial.JRPC_K_OBJECT_ID: '2'}
            ],
            launch_serial.JRPC_K_IDENTIFIED_OBJECTS: [{
                launch_serial.JRPC_K_OBJECT_ID: '1',
                launch_serial.JRPC_K_CALLSIGN: str(self.__ufo_callsign),
                launch_serial.JRPC_K_TLE: {
                    launch_serial.JRPC_K_TLE_L1:
                        '1 27844U 03031E   15007.47529781  .00000328'
                        '  00000-0  16930-3 0  1108',
                    launch_serial.JRPC_K_TLE_L2:
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

        """
#        # 4) 2 ufos
#        launch_jrpc.forget(self.__leop_id, self.__ufo_id)
#        a_cfg = launch_jrpc.get_configuration(self.__leop_id)
#        e_cfg = {
#            launch_serial.JRPC_K_LEOP_ID: str(self.__leop_id),
#            launch_serial.JRPC_K_TLE: {
#                launch_serial.JRPC_K_TLE_L1:
#                    '1 27844U 03031E   15007.47529781  .00000328'
#                    '  00000-0  16930-3 0  1108',
#                launch_serial.JRPC_K_TLE_L2:
#                    '2 27844  98.6976  18.3001 0010316  50.6742 '
#                    '104.9393 14.21678727597601',
#            },
#            launch_serial.JRPC_K_UNKNOWN_OBJECTS: [
#                {launch_serial.JRPC_K_OBJECT_ID: '2'},
#                {launch_serial.JRPC_K_OBJECT_ID: '1'}
#            ],
#            launch_serial.JRPC_K_IDENTIFIED_OBJECTS: []
#        }
#
#        if self.__verbose_testing:
#            misc.print_dictionary(a_cfg)
#            misc.print_dictionary(e_cfg)
#
#        self.assertEquals(
#            a_cfg, e_cfg, 'Configurations differ, diff = ' + str(
#                datadiff.diff(a_cfg, e_cfg)
#            )
#        )