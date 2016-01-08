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
from services.configuration.models import segments as segment_models
from services.configuration.models import tle as tle_models
from services.leop import utils as leop_utils
from services.leop.models import launch as launch_models
from services.simulation.models import groundtracks as simulation_models


class TestLaunchModels(test.TestCase):
    """UNIT test cases
    UNIT test to validate the models for the LEOP application.
    """

    def setUp(self):
        """Database setup for the tests.
        """

        self.__verbose_testing = False

        self.__launch_id = 'launch-test'
        self.__ufo_1_id = 1
        self.__ufo_1_cs = 'UFOXXXS'

        self.__tle_l1 = db_tools.ISS_TLE[0]
        self.__tle_l2 = db_tools.ISS_TLE[1]
        self.__launch = db_tools.create_launch(identifier=self.__launch_id)

        if not self.__verbose_testing:
            logging.getLogger('leop').setLevel(level=logging.CRITICAL)
            logging.getLogger('simulation').setLevel(level=logging.CRITICAL)

    def test_create_launch(self):
        """UNIT test: services.leop.launch.create
        Validates the creation of a launch object together with its associated
        resources.
        """

        # 1) a TLE object should have been created
        tle_id = leop_utils.generate_cluster_tle_id(self.__launch_id)
        self.assertTrue(
            tle_models.TwoLineElement.objects.filter(
                identifier=tle_id
            ).exists(),
            'Cluster TLE object should have been created'
        )

        # 2) a spacecraft object should have been created
        callsign = leop_utils.generate_cluster_callsign(self.__launch_id)
        sc_id = leop_utils.generate_cluster_sc_identifier(
            self.__launch_id, callsign
        )
        self.assertTrue(
            segment_models.Spacecraft.objects.filter(
                identifier=sc_id
            ).exists(),
            'Spacecraft object should have been created'
        )

        # 3) the groundtrack for the spacecraft should have been created
        self.assertTrue(
            simulation_models.GroundTrack.objects.filter(
                spacecraft=segment_models.Spacecraft.objects.get(
                    identifier=sc_id
                )
            ).exists(),
            'Groundtrack should have been created'
        )

        if self.__verbose_testing:

            print('>>> sc_id (cluster) = ' + str(sc_id))
            print('>>> tle_id (cluster) = ' + str(tle_id))
            print('>>> callsign (cluster) = ' + str(callsign))

    def test_delete_launch(self):
        """UNIT test: services.leop.launch.delete
        Validates the deletion of a Launch object together with its associated
        resources.
        """
        launch_id = 'XXXlaunch'
        self.assertEqual(
            db_tools.create_launch(identifier=launch_id).identifier,
            launch_id,
            'Create should have returned the same identifier for the launch'
        )
        launch_tle_id = leop_utils.generate_cluster_tle_id(launch_id)
        self.assertTrue(
            tle_models.TwoLineElement.objects.filter(
                identifier=launch_tle_id
            ).exists(),
            'TLE for the new launch object should have been CREATED'
        )
        launch_models.Launch.objects.get(identifier=launch_id).delete()
        self.assertFalse(
            tle_models.TwoLineElement.objects.filter(
                identifier=launch_tle_id
            ).exists(),
            'TLE for the new launch object should have been DELETED'
        )

    def test_add_unknown(self):
        """UNIT test: services.leop.launch.addUnknown
        Validates the creation of an unknown object within the database.
        """
        self.assertEqual(
            launch_models.Launch.objects.add_unknown(
                self.__launch_id, self.__ufo_1_id
            ),
            self.__ufo_1_id,
            'Should return the same identifier!'
        )

        ufo = self.__launch.unknown_objects.get(identifier=self.__ufo_1_id)
        self.assertEqual(
            ufo.identifier, self.__ufo_1_id, 'Identifiers should be the same'
        )

    def test_remove_unknown(self):
        """UNIT test: services.leop.launch.removeUnknown
        Validates the removal of an unknown object from the database.
        """
        launch_models.Launch.objects.add_unknown(
            self.__launch_id, self.__ufo_1_id
        )
        launch_models.Launch.objects.remove_unknown(
            self.__launch_id, self.__ufo_1_id
        )

        self.assertFalse(
            self.__launch.unknown_objects.filter(
                identifier=self.__ufo_1_id
            ).exists(),
            'Object should not exist'
        )

    def test_identifiy(self):
        """UNIT test: services.leop.launch.identify
        Validates the promotion of an unknown object into an identified one
        and the allocation of the resources necessary (spacecraft, tle and
        associated groundtrack).
        """
        launch_models.Launch.objects.add_unknown(
            self.__launch_id, self.__ufo_1_id
        )
        actual_id = launch_models.Launch.objects.identify(
            self.__launch_id, self.__ufo_1_id, self.__ufo_1_cs,
            self.__tle_l1, self.__tle_l2
        )
        self.assertEqual(
            actual_id[0], self.__ufo_1_id, 'Identifiers should be the same'
        )

        # 1) unknown object should have been deleted from the database.
        self.assertFalse(
            self.__launch.unknown_objects.filter(
                identifier=self.__ufo_1_id
            ).exists(),
            'Object should not exist'
        )
        # 2) Objects should exist as an spacecraft object now
        sc_id = leop_utils.generate_object_sc_identifier(
            self.__launch_id, self.__ufo_1_id
        )

        self.assertTrue(
            self.__launch.identified_objects.filter(
                identifier=self.__ufo_1_id
            ).exists(),
            'Object should exist'
        )

        # 3) The associated TLE object should have been created as well
        tle_id = leop_utils.generate_object_tle_id(
            self.__ufo_1_id, self.__ufo_1_cs
        )
        self.assertTrue(
            tle_models.TwoLineElement.objects.filter(
                identifier=tle_id
            ).exists(),
            'Cluster TLE object should have been created'
        )

        # 4) and the groundtrack generated
        self.assertTrue(
            simulation_models.GroundTrack.objects.filter(
                spacecraft=segment_models.Spacecraft.objects.get(
                    identifier=sc_id
                )
            ).exists(),
            'Groundtrack should have been created'
        )

        if self.__verbose_testing:

            print(' >>> sc_id (object) = ' + str(sc_id))
            print(' >>> tle_id (object) = ' + str(tle_id))

    def test_forget(self):
        """UNIT test: services.leop.launch.forget
        Validates the under-promotion of an identified object back to its
        unknown state.
        """
        launch_models.Launch.objects.add_unknown(
            self.__launch_id, self.__ufo_1_id
        )
        self.assertEqual(
            len(simulation_models.GroundTrack.objects.all()), 2,
            'One single track at the beginning'
        )

        launch_models.Launch.objects.identify(
            self.__launch_id, self.__ufo_1_id, self.__ufo_1_cs,
            self.__tle_l1, self.__tle_l2
        )

        self.assertFalse(
            self.__launch.unknown_objects.filter(
                identifier=self.__ufo_1_id
            ).exists(),
            'Object should not exist'
        )

        # 0) Object should have been forgotten...
        self.assertTrue(
            launch_models.Launch.objects.forget(
                self.__launch_id, self.__ufo_1_id
            ),
            'Object should have been forgotten'
        )
        # 1) ... although it should exist now as an "unknown" object:
        self.assertTrue(
            self.__launch.unknown_objects.filter(
                identifier=self.__ufo_1_id
            ).exists(),
            'Object should not exist'
        )

        # 2) Associated spacecraft should have been deleted...
        sc_id = leop_utils.generate_object_sc_identifier(
            self.__launch_id, self.__ufo_1_id
        )
        self.assertFalse(
            self.__launch.identified_objects.filter(
                identifier=self.__ufo_1_id
            ).exists(),
            'Spacecraft object should have been deleted'
        )

        # 3) ...,, the associated TLE object should have been deleted...
        tle_id = leop_utils.generate_object_tle_id(
            self.__ufo_1_id, self.__ufo_1_cs
        )
        self.assertFalse(
            tle_models.TwoLineElement.objects.filter(
                identifier=tle_id
            ).exists(),
            'Cluster TLE object should have been deleted'
        )

        # 4) ... and the groundtrack as well.
        self.assertEqual(
            len(simulation_models.GroundTrack.objects.all()), 2,
            'Groundtrack should have been deleted'
        )

        if self.__verbose_testing:

            print(' >>> sc_id (object) = ' + str(sc_id))
            print(' >>> tle_id (object) = ' + str(tle_id))
