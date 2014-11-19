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
from services.common import misc
from services.common.testing import helpers as db_tools
from services.simulation.jrpc.views import simulation as simulation_jrpc
from services.simulation.jrpc.serializers import simulation as \
    simulation_serializer
from services.simulation.models import simulation as simulation_models


class JRPCSimulationTest(test.TestCase):
    """Test class (JRPC).
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
        # TODO Improve the verificaton method (right now is by INSPECTION).
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

        import simplekml
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