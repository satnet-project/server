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
import traceback
from services.common import misc
from services.common.testing import helpers as db_tools
from services.configuration.models import segments as segment_models
from services.configuration.models import tle as tle_models
from services.configuration.jrpc.views.segments import spacecraft as sc_jrpc
from services.simulation.jrpc.views import groundtracks as simulation_jrpc
from services.simulation.jrpc.serializers import groundtracks as \
    simulation_serializer
from services.simulation.models import groundtracks as simulation_models
import simplekml


class JRPCSimulationTest(test.TestCase):
    """JRPC Test Case
    This class tests the services related with the Simulation objects.
    """

    def setUp(self):
        """
        This method populates the database with some information to be used
        only for this test.
        """
        self.__verbose_testing = False

        if not self.__verbose_testing:
            logging.getLogger('common').setLevel(level=logging.CRITICAL)
            logging.getLogger('configuration').setLevel(level=logging.CRITICAL)
            logging.getLogger('scheduling').setLevel(level=logging.CRITICAL)
            logging.getLogger('simulation').setLevel(level=logging.CRITICAL)

        self.__user_profile = db_tools.create_user_profile()
        self.__sc_1_id = 'humd-sc'
        self.__sc_1_tle_id = 'HUMSAT-D'
        self.__sc_1 = db_tools.create_sc(
            user_profile=self.__user_profile,
            identifier=self.__sc_1_id,
            tle_id=self.__sc_1_tle_id,
        )

    def test_get_groundtrack(self):
        """UNIT test (JRPC Method).
        Tests the generation of the GroundTracks for registered spacecraft.
        """
        gt = simulation_jrpc.get_groundtrack(self.__sc_1_id)
        if self.__verbose_testing:
            misc.print_list(gt)
            print 'gt.length = ' + str(len(gt))

    def test_visualize_groundtracks(self):
        """Basic groundtrack propagation.
        Creates a KML output file with the generated coordinates. The name for
        the points is the timestamp for that given coordinate.
        """
        simulation_models.GroundTrack.objects.propagate_groundtracks()
        gt_f = simulation_models.GroundTrack.objects.all()[0]
        track = simulation_serializer\
            .SimulationSerializer().serialize_groundtrack(gt_f)

        kml = simplekml.Kml()
        for p in track:
            if self.__verbose_testing:
                print '>>> @, ' + str(p['timestamp']) + ':(' +\
                    str(p['latitude']) + ',' + str(p['longitude']) + ')'
            kml.newpoint(
                name=str(p['timestamp']),
                coords=[(p['latitude'], p['longitude'])]
            )
        kml.save("test.kml")

        if self.__verbose_testing:
            print '>>> points = ' + str(len(track))

    def test_remove_sc(self):
        """JRPC remove spacecraft test.
        Basic test for validating the removal of a given Spacecraft object from
        the database through the correspondent JRPC method.
        """
        if self.__verbose_testing:
            print '>>> TEST (test_remove_sc)'

        try:
            a_id = sc_jrpc.delete(self.__sc_1_id)
            self.assertEquals(
                a_id, self.__sc_1_id,
                'Wrong id returned, e = ' + self.__sc_1_id + ', a = ' + a_id
            )
        except Exception as e:
            print traceback.format_exc()
            self.fail('No exception should have been thrown, e = ' + str(e))

        if segment_models.Spacecraft.objects.filter(identifier=self.__sc_1_id)\
                .exists():
            self.fail('Spacecraft should not be available anymore')

        if not tle_models.TwoLineElement.objects.filter(
                identifier=self.__sc_1_tle_id
        ).exists():
            self.fail('TLE should not have been deleted')

        tle = tle_models.TwoLineElement.objects.get(
            identifier=self.__sc_1_tle_id
        )

        if simulation_models.GroundTrack.objects.filter(tle=tle).exists():
            self.fail(
                'GroundTrack should have been deleted, tle_id = '
                    + str(self.__sc_1_tle_id)
            )