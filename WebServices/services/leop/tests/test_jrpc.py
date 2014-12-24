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
import datadiff
from django import test
from django.core import exceptions as django_ex
from services.common.testing import helpers as db_tools
from services.leop.models import leop as leop_models
from services.leop.jrpc.views import cluster as jrpc_leop_gs
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

        if not self.__verbose_testing:
            logging.getLogger('leop').setLevel(level=logging.CRITICAL)

    def test_list_groundstations(self):
        """Unit test case.
        Checks the functioning of the JRPC method that returns the list of
        GroundStations available for the administrator to create a LEOP system.
        """
        # Permissions basic test, no request, no permission
        try:
            jrpc_leop_gs.list_groundstations('FAKE_ID', **{'request': None})
            self.fail('No request added, permission should not be granted')
        except django_ex.PermissionDenied:
            pass

        # First step: user is not staff, access forbidden...
        try:
            jrpc_leop_gs.list_groundstations(
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
            a_gs = jrpc_leop_gs.list_groundstations(
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
        a_gs = jrpc_leop_gs.list_groundstations(
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
            jrpc_leop_gs.add_groundstations(
                'FAKE_ID', None, **{'request': None}
            )
            self.fail('No request added, permission should not be granted')
        except django_ex.PermissionDenied:
            pass
        # Permissions test (2): user not authorized
        try:
            jrpc_leop_gs.add_groundstations(
                'FAKE', None, **{'request': self.__request_1}
            )
            self.fail('No request added, permission should not be granted')
        except django_ex.PermissionDenied:
            pass
        # Basic parameters test (1)
        try:
            jrpc_leop_gs.add_groundstations(
                'FAKE', None, **{'request': self.__request_2}
            )
            self.fail('The leop cluster does not exist')
        except leop_models.LEOP.DoesNotExist:
            pass
        # Basic parameters test (2)
        actual = jrpc_leop_gs.add_groundstations(
            self.__leop_id, None, **{'request': self.__request_2}
        )
        expected = {'leop_id': self.__leop_id}
        self.assertEquals(
            actual, expected,
            'Result differs, diff = ' + str(datadiff.diff(actual, expected))
        )
        # Basic parameters test (3)
        actual = jrpc_leop_gs.add_groundstations(
            self.__leop_id, [], **{'request': self.__request_2}
        )
        expected = {'leop_id': self.__leop_id}
        self.assertEquals(
            actual, expected,
            'Result differs, diff = ' + str(datadiff.diff(actual, expected))
        )

        # GroundStations array []
        gss = [self.__gs_1_id, self.__gs_2_id]
        actual = jrpc_leop_gs.add_groundstations(
            self.__leop_id, gss, **{'request': self.__request_2}
        )
        expected = {'leop_id': self.__leop_id}
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
            jrpc_leop_gs.remove_groundstations(
                'FAKE_ID', None, **{'request': None}
            )
            self.fail('No request added, permission should not be granted')
        except django_ex.PermissionDenied:
            pass
        # Permissions test (2): user not authorized
        try:
            jrpc_leop_gs.remove_groundstations(
                'FAKE', None, **{'request': self.__request_1}
            )
            self.fail('No request added, permission should not be granted')
        except django_ex.PermissionDenied:
            pass
        # Basic parameters test (1)
        try:
            jrpc_leop_gs.remove_groundstations(
                'FAKE', None, **{'request': self.__request_2}
            )
            self.fail('The leop cluster does not exist')
        except leop_models.LEOP.DoesNotExist:
            pass
        # Basic parameters test (2)
        actual = jrpc_leop_gs.remove_groundstations(
            self.__leop_id, None, **{'request': self.__request_2}
        )
        expected = {'leop_id': self.__leop_id}
        self.assertEquals(
            actual, expected,
            'Result differs, diff = ' + str(datadiff.diff(actual, expected))
        )
        # Basic parameters test (3)
        actual = jrpc_leop_gs.remove_groundstations(
            self.__leop_id, [], **{'request': self.__request_2}
        )
        expected = {'leop_id': self.__leop_id}
        self.assertEquals(
            actual, expected,
            'Result differs, diff = ' + str(datadiff.diff(actual, expected))
        )

        # First, we add two groundstations to the cluster and we try to remove
        # them later.
        gss = [self.__gs_1_id, self.__gs_2_id]
        jrpc_leop_gs.add_groundstations(
            self.__leop_id, gss, **{'request': self.__request_2}
        )
        cluster = leop_models.LEOP.objects.get(identifier=self.__leop_id)
        self.assertEquals(
            len(cluster.groundstations.all()), 2,
            'Two groundstations should be part of this cluster object'
        )

        actual = jrpc_leop_gs.remove_groundstations(
            self.__leop_id, gss, **{'request': self.__request_2}
        )
        expected = {'leop_id': self.__leop_id}
        self.assertEquals(
            actual, expected,
            'Result differs, diff = ' + str(datadiff.diff(actual, expected))
        )
        self.assertEquals(
            len(cluster.groundstations.all()), 0,
            'No groundstations should be part of this cluster object'
        )