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

from services.common import helpers as db_tools
from services.configuration.jrpc.serializers import rules as \
    segment_serializers
from services.configuration.jrpc.views.segments import groundstations as gs_jrpc
from services.configuration.jrpc.views.segments import spacecraft as sc_jrpc
from services.configuration.models import segments as segment_models
from services.simulation.jrpc.views import passes as pass_views
from services.simulation.models import passes as pass_models


class JRPCPassesTest(test.TestCase):
    """JRPC Test Case
    Simple test case for checking that the signal-triggered generation, update
    and removal of pass slots works.
    """

    def setUp(self):
        """
        This method populates the database with some information to be used
        only for this test.
        """
        self.__verbose_testing = False

        self.__test_sc_id = 'sc-canx-2'
        self.__sc_id = 'humd-sc'
        self.__user_profile = db_tools.create_user_profile()
        self.__request = db_tools.create_request(
            user_profile=self.__user_profile
        )
        self.__sc_callsign = 'HUMXXX7'
        self.__sc_tle_1_id = 'HUMSAT-D'
        self.__sc_tle_2_id = 'CANX-2'

        self.__gs_id = 'my-gs'
        self.__gs_callsign = 'GSXXGX'
        self.__gs_elevation = 20.1
        self.__gs_latitude = 54.80
        self.__gs_longitude = -8.90

        if not self.__verbose_testing:
            logging.getLogger('common').setLevel(level=logging.CRITICAL)
            logging.getLogger('configuration').setLevel(level=logging.CRITICAL)
            logging.getLogger('scheduling').setLevel(level=logging.CRITICAL)
            logging.getLogger('simulation').setLevel(level=logging.CRITICAL)

    def _test_sc_passes(self):
        """JRPC Unit Test
        Validates the generation of the passes for a given spacecraft.
        """

        # 1) Basic test, inexistent spacecraft and no groundstation available
        try:
            pass_views.get_sc_passes(self.__sc_id, [])
            self.fail('Wrong spacecraft ID must throw an exception')
        except segment_models.Spacecraft.DoesNotExist:
            pass

        self.assertEqual(
            sc_jrpc.create(
                self.__sc_id, self.__sc_callsign, self.__sc_tle_1_id,
                **{'request': self.__request}
            ),
            {segment_serializers.SC_ID_K: self.__sc_id},
            'Should have returned the spacecraft identifier'
        )
        self.assertEqual(
            pass_views.get_sc_passes(self.__sc_id, []), [],
            'No passes, an array should be returned empty'
        )

        # 2) TLE change, no pass slots since no ground stations are available
        sc_cfg = {
            segment_serializers.SC_CALLSIGN_K: self.__sc_callsign,
            segment_serializers.SC_TLE_ID_K: self.__sc_tle_2_id
        }
        self.assertEqual(
            sc_jrpc.set_configuration(self.__sc_id, sc_cfg),
            self.__sc_id,
            'Should have returned spacecrafts identifier'
        )

        # 3) Spacecraft removal, just to check stability after signal handler
        # execution
        self.assertTrue(
            sc_jrpc.delete(self.__sc_id), 'Should have removed the spacecraft'
        )
        self.assertEqual(
            len(pass_models.PassSlots.objects.all()), 0, 'No slot available'
        )

        # 4) Ground station addition: should create slots for already-added
        # satellites for general testing purposes (check website.tests)
        self.assertEqual(
            gs_jrpc.create(
                self.__gs_id, self.__gs_callsign, self.__gs_elevation,
                self.__gs_latitude, self.__gs_longitude,
                **{'request': self.__request}
            ),
            {segment_serializers.GS_ID_K: self.__gs_id},
            'Should have returned groundstastions identifier'
        )
        self.assertNotEqual(
            len(pass_views.get_sc_passes(self.__test_sc_id)),
            0,
            'Slots should have been added for the sc, id = ' + self.__test_sc_id
        )

        # 5) the creation of a new spacecraft should add more slots
        self.assertEqual(
            sc_jrpc.create(
                self.__sc_id, self.__sc_callsign, self.__sc_tle_1_id,
                **{'request': self.__request}
            ),
            {segment_serializers.SC_ID_K: self.__sc_id},
            'Should have returned the spacecraft identifier'
        )
        self.assertNotEqual(
            len(pass_views.get_sc_passes(self.__sc_id)),
            0,
            'Slots should have been added for the sc, id = ' + self.__sc_id
        )
