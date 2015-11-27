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

import datetime
import difflib
import logging

import datadiff
import pytz
from django import test
from django.core import exceptions as django_ex

from services.common import misc, helpers as db_tools
from services.configuration.models import tle as tle_models
from services.leop import utils as launch_utils
from services.leop.jrpc.serializers import launch as launch_serial
from services.leop.jrpc.serializers import messages as messages_serial
from services.leop.jrpc.views import launch as launch_jrpc
from services.leop.jrpc.views import messages as messages_jrpc
from services.leop.models import launch as launch_models
from services.simulation.models import groundtracks as simulation_models
from website import settings as satnet_settings


class TestLaunchViews(test.TestCase):
    """Test class for the LEOP JRPC methods.
    """

    def setUp(self):
        """Database setup for the tests.
        """

        self.__verbose_testing = False
        satnet_settings.JRPC_PERMISSIONS = True

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

        self.__leop_tle_l1 =\
            '1 27844U 03031E   15007.47529781  ' +\
            '.00000328  00000-0  16930-3 0  1108'
        self.__leop_tle_l2 =\
            '2 27844  98.6976  18.3001 0010316  ' +\
            '50.6742 104.9393 14.21678727597601'

        self.__leop_id = 'leop_cluster_4testing'
        self.__leop_date = pytz.utc.localize(datetime.datetime.today())
        self.__leop = db_tools.create_launch(
            admin=self.__admin, identifier=self.__leop_id,
            date=self.__leop_date,
            tle_l1=self.__leop_tle_l1, tle_l2=self.__leop_tle_l2
        )
        self.__leop_serial_date = str(self.__leop.date.isoformat())
        self.__leop_cs = launch_utils.generate_cluster_callsign(self.__leop_id)
        self.__leop_sc_id = launch_utils.generate_cluster_sc_identifier(
            self.__leop_id, self.__leop_cs
        )

        self.__ufo_id = 1
        self.__ufo_sc_id = launch_utils.generate_object_sc_identifier(
            self.__leop_id, self.__ufo_id
        )
        self.__ufo_callsign = 'SCLLY'
        self.__ufo_tle_l1 = self.__leop_tle_l1
        self.__ufo_tle_l2 = self.__leop_tle_l2

        self.__leop_2_tle_l1 =\
            '1 36799U 10035E   15011.25448421  .00004255  ' +\
            '00000-0  47713-3 0  8407'
        self.__leop_2_tle_l2 =\
            '2 36799  98.0147 109.9908 0013178   6.5991  ' +\
            '46.1472 14.87298023243626'

        if not self.__verbose_testing:
            logging.getLogger('leop').setLevel(level=logging.CRITICAL)
            logging.getLogger('simulation').setLevel(level=logging.CRITICAL)

    def test_list_groundstations(self):
        """JRPC method: services.leop.groundstations.list
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
            self.assertEqual(
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

        self.assertEqual(
            a_gs, e_gs, 'Unexpected result! diff = ' + str(
                datadiff.diff(a_gs, e_gs)
            )
        )

    def test_add_groundstations(self):
        """JRPC method: services.leop.groundstations.add
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
        self.assertRaises(
            Exception,
            launch_jrpc.add_groundstations,
            None, **{'request': self.__request_2}
        )

        # GroundStations array []
        gss = [self.__gs_1_id, self.__gs_2_id]
        actual = launch_jrpc.add_groundstations(
            self.__leop_id, gss, **{'request': self.__request_2}
        )
        expected = {launch_serial.JRPC_K_LEOP_ID: self.__leop_id}
        self.assertEqual(
            actual, expected,
            'Result differs, diff = ' + str(datadiff.diff(actual, expected))
        )

        cluster = launch_models.Launch.objects.get(identifier=self.__leop_id)
        self.assertEqual(
            len(cluster.groundstations.all()), 2,
            'Two groundstations should be part of this cluster object'
        )

    def test_remove_groundstations(self):
        """JRPC method: services.leop.groundstations.remove
        Validates the removal of an array of GroundStations to a given LEOP
        cluster.
        """

        # Permissions test (1): no request, no permission
        self.assertRaises(
            django_ex.PermissionDenied,
            launch_jrpc.remove_groundstations,
            'FAKE_ID', None, **{'request': None}
        )

        # Permissions test (2): user not authorized
        self.assertRaises(
            django_ex.PermissionDenied,
            launch_jrpc.remove_groundstations,
            'FAKE', None, **{'request': self.__request_1}
        )

        # Basic parameters test (1)
        self.assertRaises(
            launch_models.Launch.DoesNotExist,
            launch_jrpc.remove_groundstations,
            'FAKE', ['fake'], **{'request': self.__request_2}
        )

        # Basic parameters test (2)
        actual = launch_jrpc.remove_groundstations(
            self.__leop_id, None, **{'request': self.__request_2}
        )
        expected = {launch_serial.JRPC_K_LEOP_ID: self.__leop_id}
        self.assertEqual(
            actual, expected,
            'Result differs, diff = ' + str(datadiff.diff(actual, expected))
        )
        # Basic parameters test (3)
        actual = launch_jrpc.remove_groundstations(
            self.__leop_id, [], **{'request': self.__request_2}
        )
        expected = {launch_serial.JRPC_K_LEOP_ID: self.__leop_id}
        self.assertEqual(
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
        self.assertEqual(
            len(cluster.groundstations.all()), 2,
            'Two groundstations should be part of this cluster object'
        )

        self.assertTrue(
            launch_jrpc.remove_groundstations(
                self.__leop_id, gss, **{'request': self.__request_2}
            ),
            'Should have returned True'
        )
        self.assertEqual(
            len(cluster.groundstations.all()), 0,
            'No groundstations should be part of this cluster object'
        )

    def test_add_unknown(self):
        """JRPC method: services.leop.unknown.add
        Validation of the remote addition of a new unknown object to the list.
        """
        self.assertRaises(
            Exception, launch_jrpc.add_unknown, self.__leop_id, None
        )
        self.assertRaises(
            Exception, launch_jrpc.add_unknown, self.__leop_id, -1
        )

        self.assertEqual(
            launch_jrpc.add_unknown(self.__leop_id, 1), 1,
            'Identifiers must match'
        )

        a_list = [
            a.identifier for a in launch_models.Launch.objects.get(
                identifier=self.__leop_id
            ).unknown_objects.all()
        ]
        e_list = [1]
        self.assertEqual(
            a_list, e_list, 'Data differs in the DB, diff = ' + str(
                datadiff.diff(a_list, e_list)
            )
        )

    def test_remove_unknown(self):
        """JRPC method: services.leop.unknown.remove
        Validates the removal of an unknown object from the list
        """
        self.assertRaises(
            Exception, launch_jrpc.remove_unknown, self.__leop_id, None
        )
        self.assertRaises(
            Exception, launch_jrpc.remove_unknown, self.__leop_id, -1
        )
        self.assertRaises(
            Exception, launch_jrpc.remove_unknown, self.__leop_id, 2
        )

        self.assertEqual(
            launch_jrpc.add_unknown(self.__leop_id, 1), 1,
            'Identifiers must match'
        )
        self.assertTrue(
            launch_jrpc.remove_unknown(self.__leop_id, 1),
            'Should have returned True'
        )
        self.assertEqual(
            len(launch_models.Launch.objects.get(
                identifier=self.__leop_id
            ).unknown_objects.all()),
            0,
            'List must be empty'
        )

    def test_update_ufo(self):
        """JRPC method: services.leop.ufo.update
        Validation of the updte method for an UFO-like object.
        """
        self.assertRaises(
            Exception, launch_jrpc.update, None, None, None, None, None
        )
        self.assertRaises(
            Exception,
            launch_jrpc.update,
            self.__leop_id, None, None, None, None
        )
        self.assertRaises(
            Exception,
            launch_jrpc.update,
            self.__leop_id, self.__ufo_id, None, None, None
        )

        self.assertEqual(
            launch_jrpc.add_unknown(self.__leop_id, self.__ufo_id),
            self.__ufo_id,
            'Should return the same id'
        )
        self.assertRaises(
            Exception,
            launch_jrpc.update,
            self.__leop_id, self.__ufo_id, None, None, None
        )

        self.assertEqual(
            launch_jrpc.identify(
                self.__leop_id, self.__ufo_id,
                self.__ufo_callsign, self.__ufo_tle_l1, self.__ufo_tle_l2
            ),
            {
                launch_serial.JRPC_K_OBJECT_ID: self.__ufo_id,
                launch_serial.JRPC_K_SC_ID: self.__ufo_sc_id
            },
            'Should have returned the id of the UFO and the SC id'
        )
        self.assertEqual(
            launch_jrpc.update(self.__leop_id, self.__ufo_id, None, None, None),
            {
                launch_serial.JRPC_K_OBJECT_ID: self.__ufo_id,
                launch_serial.JRPC_K_SC_ID: self.__ufo_sc_id
            },
            'Should have returned the id of the UFO and the SC id'
        )
        self.assertEqual(
            launch_jrpc.update(
                self.__leop_id, self.__ufo_id,
                self.__ufo_callsign, self.__ufo_tle_l1, self.__ufo_tle_l2
            ),
            {
                launch_serial.JRPC_K_OBJECT_ID: self.__ufo_id,
                launch_serial.JRPC_K_SC_ID: self.__ufo_sc_id
            },
            'Should have returned the id of the UFO and the SC id'
        )
        self.assertEqual(
            launch_jrpc.update(
                self.__leop_id, self.__ufo_id,
                self.__ufo_callsign, self.__leop_2_tle_l1, self.__leop_2_tle_l2
            ),
            {
                launch_serial.JRPC_K_OBJECT_ID: self.__ufo_id,
                launch_serial.JRPC_K_SC_ID: self.__ufo_sc_id
            },
            'Should have returned the id of the UFO and the SC id'
        )

    def test_get_configuration(self):
        """JRPC method: services.leop.getConfiguration
        Validation of the JRPC method that permits obtaining the
        configuration for a given LEOP cluster.
        """
        self.assertRaises(
            launch_models.Launch.DoesNotExist, launch_jrpc.get_configuration, ''
        )

        # 1) No ufos
        a_cfg = launch_jrpc.get_configuration(self.__leop_id)
        e_cfg = {
            launch_serial.JRPC_K_LEOP_ID: str(self.__leop_id),
            launch_serial.JRPC_K_SC_ID: str(self.__leop_sc_id),
            launch_serial.JRPC_K_DATE: self.__leop_serial_date,
            launch_serial.JRPC_K_TLE_L1: self.__leop_tle_l1,
            launch_serial.JRPC_K_TLE_L2: self.__leop_tle_l2,
            launch_serial.JRPC_K_UNKNOWN_OBJECTS: [],
            launch_serial.JRPC_K_IDENTIFIED_OBJECTS: []
        }
        self.assertEqual(
            a_cfg, e_cfg, 'Configurations differ, diff = ' + str(
                datadiff.diff(a_cfg, e_cfg)
            )
        )

        # 2) 1 ufo
        launch_jrpc.add_unknown(self.__leop_id, 1)
        a_cfg = launch_jrpc.get_configuration(self.__leop_id)
        e_cfg = {
            launch_serial.JRPC_K_LEOP_ID: str(self.__leop_id),
            launch_serial.JRPC_K_SC_ID: str(self.__leop_sc_id),
            launch_serial.JRPC_K_DATE: self.__leop_serial_date,
            launch_serial.JRPC_K_TLE_L1: self.__leop_tle_l1,
            launch_serial.JRPC_K_TLE_L2: self.__leop_tle_l2,
            launch_serial.JRPC_K_UNKNOWN_OBJECTS: [
                {launch_serial.JRPC_K_OBJECT_ID: '1'}
            ],
            launch_serial.JRPC_K_IDENTIFIED_OBJECTS: []
        }
        self.assertEqual(
            a_cfg, e_cfg, 'Configurations differ, diff = ' + str(
                datadiff.diff(a_cfg, e_cfg)
            )
        )

        # 3) 1 ufo, 1 identified
        launch_jrpc.add_unknown(self.__leop_id, 2)
        launch_jrpc.identify(
            self.__leop_id, self.__ufo_id, self.__ufo_callsign,
            self.__ufo_tle_l1, self.__ufo_tle_l2
        )

        a_cfg = launch_jrpc.get_configuration(self.__leop_id)
        e_cfg = {
            launch_serial.JRPC_K_LEOP_ID: str(self.__leop_id),
            launch_serial.JRPC_K_SC_ID: str(self.__leop_sc_id),
            launch_serial.JRPC_K_DATE: self.__leop_serial_date,
            launch_serial.JRPC_K_TLE_L1: self.__leop_tle_l1,
            launch_serial.JRPC_K_TLE_L2: self.__leop_tle_l2,
            launch_serial.JRPC_K_UNKNOWN_OBJECTS: [
                {launch_serial.JRPC_K_OBJECT_ID: '2'}
            ],
            launch_serial.JRPC_K_IDENTIFIED_OBJECTS: [{
                launch_serial.JRPC_K_OBJECT_ID: '1',
                launch_serial.JRPC_K_SC_ID: str(self.__ufo_sc_id),
                launch_serial.JRPC_K_CALLSIGN: str(self.__ufo_callsign),
                launch_serial.JRPC_K_TLE_L1: self.__leop_tle_l1,
                launch_serial.JRPC_K_TLE_L2: self.__leop_tle_l2,
            }]
        }
        self.assertEqual(
            a_cfg, e_cfg, 'Configurations differ, diff = ' + str(
                datadiff.diff(a_cfg, e_cfg)
            )
        )

        # 4) 2 ufos
        launch_jrpc.forget(self.__leop_id, self.__ufo_id)
        a_cfg = launch_jrpc.get_configuration(self.__leop_id)
        e_cfg = {
            launch_serial.JRPC_K_LEOP_ID: str(self.__leop_id),
            launch_serial.JRPC_K_SC_ID: str(self.__leop_sc_id),
            launch_serial.JRPC_K_DATE: self.__leop_serial_date,
            launch_serial.JRPC_K_TLE_L1: self.__leop_tle_l1,
            launch_serial.JRPC_K_TLE_L2: self.__leop_tle_l2,
            launch_serial.JRPC_K_UNKNOWN_OBJECTS: [
                {launch_serial.JRPC_K_OBJECT_ID: '2'},
                {launch_serial.JRPC_K_OBJECT_ID: '1'}
            ],
            launch_serial.JRPC_K_IDENTIFIED_OBJECTS: []
        }

        if self.__verbose_testing:
            misc.print_dictionary(a_cfg)
            misc.print_dictionary(e_cfg)

        self.assertEqual(
            a_cfg, e_cfg, 'Configurations differ, diff = ' + str(
                datadiff.diff(a_cfg, e_cfg)
            )
        )

    def test_set_configuration(self):
        """JRPC method: services.leop.setConfiguration
        Validates the update of the configuration for a given launch object.
        """
        self.assertRaises(
            launch_models.Launch.DoesNotExist,
            launch_jrpc.set_configuration, 'aaaaaaaaaaab', {}
        )
        self.assertRaises(
            Exception,
            launch_jrpc.set_configuration, self.__leop_id, {}
        )

        tomorrow = pytz.utc.localize(
            datetime.datetime.today() + datetime.timedelta(days=1)
        )

        actual_date = launch_models.Launch.objects.get(
            identifier=self.__leop_id
        ).date
        self.assertEqual(
            actual_date.isoformat(), self.__leop_date.isoformat(),
            'Date objects should match, diff = ' + str(difflib.ndiff(
                actual_date.isoformat(), self.__leop_date.isoformat()
            ))
        )
        self.assertEqual(
            launch_jrpc.set_configuration(self.__leop_id, {
                launch_serial.JRPC_K_DATE: str(tomorrow.isoformat())
            }),
            self.__leop_id,
            'Should have returned the same launch identifier'
        )
        actual_date = launch_models.Launch.objects.get(
            identifier=self.__leop_id
        ).date
        self.assertEqual(
            actual_date.isoformat(), tomorrow.isoformat(),
            'Date objects should match, diff = ' + str(difflib.ndiff(
                actual_date.isoformat(), tomorrow.isoformat()
            ))
        )

        old_gt = simulation_models.GroundTrack.objects.get(tle=self.__leop.tle)
        self.assertEqual(
            launch_jrpc.set_configuration(self.__leop_id, {
                launch_serial.JRPC_K_DATE: str(tomorrow.isoformat()),
                launch_serial.JRPC_K_TLE_L1: self.__leop_2_tle_l1,
                launch_serial.JRPC_K_TLE_L2: self.__leop_2_tle_l2,
            }),
            self.__leop_id,
            'Should have returned the same launch identifier'
        )

        self.assertTrue(
            tle_models.TwoLineElement.objects.filter(
                first_line=self.__leop_2_tle_l1
            ).exists(),
            'TLE (first_line) should have already been updated'
        )
        self.assertTrue(
            tle_models.TwoLineElement.objects.filter(
                second_line=self.__leop_2_tle_l2
            ).exists(),
            'TLE (second_line) should have already been updated'
        )
        new_gt = simulation_models.GroundTrack.objects.get(tle=self.__leop.tle)
        self.assertNotEqual(old_gt, new_gt, 'GroundTracks should be different')

    def test_get_passes(self):
        """JRPC method: services.leop.getPasses
        Validates the retrieval of the passes for this launch.
        """
        self.assertEqual(
            launch_jrpc.get_pass_slots(self.__leop_id),
            [],
            'No passes should have been inserted yet'
        )

        self.assertEqual(
            launch_jrpc.add_groundstations(
                self.__leop_id, [self.__gs_1_id],
                **{'request': self.__request_2}
            ),
            {launch_serial.JRPC_K_LEOP_ID: self.__leop_id},
            'Should have returned launch identifier'
        )

        # 1 ufo gets identified, generates pass slots...
        launch_jrpc.add_unknown(self.__leop_id, self.__ufo_id)
        launch_jrpc.identify(
            self.__leop_id, self.__ufo_id, self.__ufo_callsign,
            self.__ufo_tle_l1, self.__ufo_tle_l2
        )

        slots = launch_jrpc.get_pass_slots(self.__leop_id)
        self.assertNotEqual(
            len(slots), 0, 'Pass slots should have been created'
        )

    def test_list_sc(self):
        """JRPC method: services.leop.spacecraft.list
        Validates the retrieval of the list of spacecraft associated to this
        launch.
        """
        launch_jrpc.list_spacecraft(
            self.__leop_id, **{'request': self.__request_2}
        )

    def test_get_messages(self):
        """JRPC method: services.leop.getMessages
        Validates the retrieval of messages from the server.
        """
        # 1) interface robustness
        self.assertRaises(
            launch_models.Launch.DoesNotExist,
            messages_jrpc.get_messages, 'DOESNTEXIST', 'nulldate'
        )
        self.assertRaises(
            Exception, messages_jrpc.get_messages, self.__leop_id, None
        )
        self.assertRaises(
            Exception, messages_jrpc.get_messages, self.__leop_id, None
        )
        self.assertRaises(
            Exception, messages_jrpc.get_messages, self.__leop_id, 'null'
        )

        # 2) basic empty response
        self.assertEqual(
            messages_jrpc.get_messages(
                self.__leop_id, '2002-12-26T00:00:00-06:39'
            ),
            [],
            'No messages, an empty array should have been returned'
        )

        # 3) feeding 1 message, should be retrieved
        # 3.a) gs created and added to the launch
        self.assertEqual(
            launch_jrpc.add_groundstations(
                self.__leop_id, [self.__gs_1_id],
                **{'request': self.__request_2}
            ),
            {launch_serial.JRPC_K_LEOP_ID: self.__leop_id},
            'The identifier of the Launch should have been returned'
        )

        # 3.b) database fed with fake data frame
        message_1 = db_tools.create_message(self.__gs_1)

        # 3.c) service finally invoked
        yesterday = misc.get_now_utc() - datetime.timedelta(days=1)
        actual = messages_jrpc.get_messages(
            self.__leop_id, yesterday.isoformat()
        )
        expected = [{
            launch_serial.JRPC_K_GS_ID: self.__gs_1_id,
            messages_serial.JRPC_K_TS: message_1.groundstation_timestamp,
            messages_serial.JRPC_K_MESSAGE: db_tools.MESSAGE__1_TEST
        }]
        self.assertEqual(
            actual, expected,
            'Single message array expected, diff = ' + str(datadiff.diff(
                actual, expected
            ))
        )

        # 4) multiple groundstations:
        # 4.a) gs created and added to the launch
        self.assertEqual(
            launch_jrpc.add_groundstations(
                self.__leop_id, [self.__gs_2_id],
                **{'request': self.__request_2}
            ),
            {launch_serial.JRPC_K_LEOP_ID: self.__leop_id},
            'The identifier of the Launch should have been returned'
        )

        # 3.b) database fed with fake data frame
        message_2 = db_tools.create_message(
            self.__gs_2, message=db_tools.MESSAGE_BASE64
        )

        # 3.c) service finally invoked
        yesterday = misc.get_now_utc() - datetime.timedelta(days=1)
        actual = messages_jrpc.get_messages(
            self.__leop_id, yesterday.isoformat()
        )
        expected.append({
            launch_serial.JRPC_K_GS_ID: self.__gs_2_id,
            messages_serial.JRPC_K_TS: message_2.groundstation_timestamp,
            messages_serial.JRPC_K_MESSAGE: db_tools.MESSAGE_BASE64.decode()
        })

        self.assertEqual(
            actual, expected,
            'Single message array expected, diff = ' + str(datadiff.diff(
                actual, expected
            ))
        )
