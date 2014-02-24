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

from django.test import TestCase
from configuration.models.channels import GroundStationChannel, \
    AvailablePolarizations
from configuration.models.segments import GroundStationConfiguration
from configuration.tests.utils import testdb_create_user_profile,  \
    testdb_create_gs


class ChannelsTest(TestCase):
    """
    Test class for the channel model testing process. It helps in managing the
    required testing database.

    The 'create' method is not tested since it is utilized for populating the
    testing database. Therefore, the correct exectuion of the rest of the tests
    involves a correct functioning of this method.
    """

    def setUp(self):
        """
        Populates the initial database with a set of objects required to run
        the following tests.
        """
        self.__gs_identifier = 'gs-castrelos'
        self.__ch_identifier = 'chan-cas'

        self.__test_user_profile =\
            testdb_create_user_profile()
        self.__test_ground_station =\
            testdb_create_gs(user_profile=self.__test_user_profile,
                             identifier=self.__gs_identifier,
                             ch_identifier=self.__ch_identifier)

        self.__ch_pols_1 =\
            [AvailablePolarizations.objects.get(polarization='Any')]

    def test_channel_update(self):
        """
        Test that the update method of a channel works properly. Take into
        consideration the fact that it must support a partial definition of
        all the properties of a channel object.
        """
        print '>>> TEST (test_channel_update): identifier change'
        ch = GroundStationChannel.objects.get(identifier=self.__ch_identifier)
        ch.update(polarizations_list=self.__ch_pols_1)
        print '>>>> ch.identifier = ' + ch.identifier
        ch2 = GroundStationConfiguration.objects.get_channel(
            ground_station_id=self.__gs_identifier,
            channel_id=self.__ch_identifier)
        self.assertItemsEqual(
            [str(p.polarization) for p in ch2.polarization.all()],
            [str(p.polarization) for p in self.__ch_pols_1],
            'Wrong Polarizations')
        print '>>>> polarizations = ' +\
              str([str(p.polarization) for p in ch2.polarization.all()])

    def test_gs_delete(self):
        """
        This test validates the functioning of the delete method for removing
        a ground station from the database, together with all its associated
        resources like channels.
        """
        print '>>> TEST (test_gs_delete): ground station deletion'

        gs = GroundStationConfiguration.objects.get(identifier='gs-castrelos')
        gs.delete()
        self.assertEquals(GroundStationChannel.objects.all().count(), 0)
