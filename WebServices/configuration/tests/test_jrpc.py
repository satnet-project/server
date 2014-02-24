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
from configuration.jrpc import segments, rules
from configuration.models import rules as rules_models
from configuration.models.rules import AvailabilityRule
from configuration.tests.utils import testdb_create_user_profile, \
    testdb_create_request, testdb_create_gs, testdb_create_jrpc_once_rule
from configuration.utils import print_dictionary


class SegmentsTest(TestCase):
    """
    Test class for the channel model testing process. It helps in managing the
    required testing database.

    The 'create' method is not tested since it is utilized for populating the
    testing database. Therefore, the correct exectuion of the rest of the tests
    involves a correct functioning of this method.
    """

    def setUp(self):
        """
        This method populates the database with some information to be used
        only for this test.
        """
        self.__test_gs_identifier = 'gs-castrelos'
        self.__test_ch_identifier = 'ch-gs-cp'
        self.__test_user_profile =\
            testdb_create_user_profile()
        self.__test_ground_station =\
            testdb_create_gs(user_profile=self.__test_user_profile,
                             identifier=self.__test_gs_identifier)
        self.__test_ground_station =\
            testdb_create_gs(user_profile=self.__test_user_profile,
                             identifier='gs-calpoly',
                             ch_identifier=self.__test_ch_identifier)
        self.__test_http_request =\
            testdb_create_request(user_profile=self.__test_user_profile)

    def test_gs_list(self):
        """
        This test validates the list of configuration objects returned through
        the JRPC method.
        """
        print '>>> TEST (test_gs_list): ground station list'
        gs_list = segments.gs_list(request=self.__test_http_request)
        self.assertItemsEqual(gs_list, ['gs-castrelos', 'gs-calpoly'],
                              'Wrong gs identifiers.')

    def test_gs_channels(self):
        """
        This test validates the list of channels returned throught the JRPC
        method.
        """
        print '>>> TEST (test_gs_channels): ground station channels list'
        ch_list = segments.gs_get_channels(self.__test_gs_identifier)
        self.assertItemsEqual(ch_list['groundstation_channels'], ['chan-test'],
                              'Wrong channel identifiers, ch = ' + str(
                                  ch_list))

    def test_gs_get_configuration(self):
        """
        This test validates the returned configuration by the proper JRPC
        method.
        """
        print '>>> TEST (test_gs_get_configuration): ground station ' \
              'configuration'
        cfg = segments.deserialize_gs_configuration(self.__test_gs_identifier)
        print_dictionary(cfg)

    def test_add_rule(self):
        """
        This test validates that the system correctly adds a new rule to the
        set of rules for a given channel of a ground station.
        """
        print '>>> TEST (test_gs_channel_add_rule): ground station ' \
              'configuration'
        rule_cfg = testdb_create_jrpc_once_rule()
        rule_id = rules.add_rule(self.__test_gs_identifier, 'chan-test',
                                 rule_cfg)
        rule = AvailabilityRule.objects.get(id=rule_id)
        self.assertEquals(rule.operation, rules_models.ADD_SLOTS,
                          'Wrong operation')
        self.assertEquals(rule.periodicity, rules_models.ONCE_PERIODICITY,
                          'Wrong periodicity')

    def test_remove_rule(self):
        """
        This test validates that the system correctly adds a new rule to the
        set of rules for a given channel of a ground station.
        """
        print '>>> TEST (test_gs_channel_add_rule): ground station ' \
              'configuration'
        rule_cfg = testdb_create_jrpc_once_rule()
        rule_id = rules.add_rule(self.__test_gs_identifier, 'chan-test',
                                 rule_cfg)
        rules.remove_rule(self.__test_gs_identifier, 'chan-test', rule_id)
        try:
            rule = AvailabilityRule.objects.get(id=rule_id)
            self.fail('Object should not have been found, rule_id = '
                      + str(rule.pk))
        except AvailabilityRule.DoesNotExist as e:
            print e.message
