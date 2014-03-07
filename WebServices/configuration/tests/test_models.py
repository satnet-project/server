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
from configuration.models.rules import AvailabilityRule

__author__ = 'rtubiopa@calpoly.edu'

from django.test import TestCase
from configuration.models.channels import GroundStationChannel, \
    AvailablePolarizations
from configuration.models.segments import GroundStationConfiguration
from configuration.tests.utils import testdb_create_user_profile,  \
    testdb_create_gs, testdb_create_jrpc_once_rule, \
    testdb_create_jrpc_daily_rule
from configuration.jrpc import rules as jrpc_rules
from configuration.utils import define_interval


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

        gs = GroundStationConfiguration.objects.get(
            identifier=self.__gs_identifier)
        gs.delete()
        self.assertEquals(GroundStationChannel.objects.all().count(), 0)

    def test_get_applicable_rules(self):
        """
        This test verifies whether the method that search all the rules
        contained within a given interval works.
        """
        print '>>> TEST (test_get_applicable_rules): get applicable rules'

        rule_1 = testdb_create_jrpc_once_rule()
        rule_2 = testdb_create_jrpc_daily_rule()
        rule_3 = testdb_create_jrpc_once_rule(
            date_text='Thu, 27 Feb 2014 12:14:05 +0000'
        )
        rule_4 = testdb_create_jrpc_once_rule(
            operation=jrpc_rules.RULE_OP_REMOVE)
        rule_5 = testdb_create_jrpc_daily_rule(
            operation=jrpc_rules.RULE_OP_REMOVE)
        rule_6 = testdb_create_jrpc_once_rule(
            operation=jrpc_rules.RULE_OP_REMOVE,
            date_text='Thu, 27 Feb 2014 12:14:05 +0000'
        )
        rule_1_id = jrpc_rules.add_rule(self.__gs_identifier,
                                        self.__ch_identifier, rule_1)
        rule_2_id = jrpc_rules.add_rule(self.__gs_identifier,
                                        self.__ch_identifier, rule_2)
        rule_3_id = jrpc_rules.add_rule(self.__gs_identifier,
                                        self.__ch_identifier, rule_3)
        rule_4_id = jrpc_rules.add_rule(self.__gs_identifier,
                                        self.__ch_identifier, rule_4)
        rule_5_id = jrpc_rules.add_rule(self.__gs_identifier,
                                        self.__ch_identifier, rule_5)
        rule_6_id = jrpc_rules.add_rule(self.__gs_identifier,
                                        self.__ch_identifier, rule_6)
        self.assertEquals(len(AvailabilityRule.objects.all()), 6,
                          'Incorrect number of rules in the database')
        add_rules, remove_rules = AvailabilityRule.objects\
            .get_applicable_rules()
        print '>>>> add_rules = ' + str(len(add_rules))
        self.assertEquals(len(add_rules), 2,
                          'Wrong number of rules returned as applicable, '
                          'returned = ' + str(len(add_rules)))
        print '>>>> remove_rules = ' + str(len(remove_rules))
        self.assertEquals(len(remove_rules), 2,
                          'Wrong number of rules returned as applicable.')
        jrpc_rules.remove_rule(self.__gs_identifier, self.__ch_identifier,
                               rule_1_id)
        jrpc_rules.remove_rule(self.__gs_identifier, self.__ch_identifier,
                               rule_2_id)
        jrpc_rules.remove_rule(self.__gs_identifier, self.__ch_identifier,
                               rule_3_id)
        jrpc_rules.remove_rule(self.__gs_identifier, self.__ch_identifier,
                               rule_4_id)
        jrpc_rules.remove_rule(self.__gs_identifier, self.__ch_identifier,
                               rule_5_id)
        jrpc_rules.remove_rule(self.__gs_identifier, self.__ch_identifier,
                               rule_6_id)
        self.assertEquals(len(AvailabilityRule.objects.all()), 0,
                          'Incorrect number of rules in the database')

    def test_get_availability_slots(self):
        """
        This test validates the generation of slots by the different rules
        supported by the configuration service.
        """
        rule_1 = testdb_create_jrpc_once_rule()
        rule_2 = testdb_create_jrpc_daily_rule()
        rule_3 = testdb_create_jrpc_once_rule(
            date_text='Thu, 27 Feb 2014 12:14:05 +0000'
        )
        rule_4 = testdb_create_jrpc_once_rule(
            operation=jrpc_rules.RULE_OP_REMOVE)
        rule_5 = testdb_create_jrpc_daily_rule(
            operation=jrpc_rules.RULE_OP_REMOVE)
        rule_6 = testdb_create_jrpc_once_rule(
            operation=jrpc_rules.RULE_OP_REMOVE,
            date_text='Thu, 27 Feb 2014 12:14:05 +0000'
        )
        jrpc_rules.add_rule(self.__gs_identifier, self.__ch_identifier, rule_1)
        jrpc_rules.add_rule(self.__gs_identifier, self.__ch_identifier, rule_2)
        jrpc_rules.add_rule(self.__gs_identifier, self.__ch_identifier, rule_3)
        jrpc_rules.add_rule(self.__gs_identifier, self.__ch_identifier, rule_4)
        jrpc_rules.add_rule(self.__gs_identifier, self.__ch_identifier, rule_5)
        jrpc_rules.add_rule(self.__gs_identifier, self.__ch_identifier, rule_6)
        self.assertEquals(len(AvailabilityRule.objects.all()), 6,
                          'Incorrect number of rules in the database')
        available_slots = AvailabilityRule.objects.get_availability_slots(
            interval=define_interval(days=14))
        self.assertEquals(len(available_slots), 6, 'Incorrect number of slots')
