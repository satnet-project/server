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
from services.common.testing import helpers as db_tools
from services.configuration.models import segments as segment_models
from services.simulation.jrpc.serializers import simulation as \
    simulation_serializer

logger = logging.getLogger('configuration')


class TestGroundTrackPropagation(test.TestCase):
    """Unit test class.
    The following tests validate the propagation of the GroundTracks for the
    available satellites.
    """

    def setUp(self):

        super(TestGroundTrackPropagation, self).setUp()

        self.__verbose_testing = False
        self.__sc_1_id = 'sc-humsat'
        self.__sc_1_tle_id = 'HUMSAT-D'

        self.__band = db_tools.create_band()
        self.__user_profile = db_tools.create_user_profile()
        db_tools.create_sc(
            user_profile=self.__user_profile,
            identifier=self.__sc_1_id, tle_id=self.__sc_1_tle_id
        )

        if not self.__verbose_testing:
            logging.getLogger('configuration').setLevel(level=logging.CRITICAL)

    def test_visualize_groundtracks(self):
        """Basic groundtrack propagation.
        Creates a KML output file with the generated coordinates. The name for
        the points is the timestamp for that given coordinate.
        """
        sc = segment_models.Spacecraft.objects.get(identifier=self.__sc_1_id)
        gt_i = sc.groundtrack
        segment_models.Spacecraft.objects.propagate_groundtracks()
        gt_f = sc.groundtrack
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