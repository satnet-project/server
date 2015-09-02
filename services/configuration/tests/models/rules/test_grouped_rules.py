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

import datadiff
import datetime
import logging
from django import test
from services.common import misc
from services.common.testing import helpers as db_tools
from services.configuration.signals import models as model_signals
from services.configuration.models import rules as rule_models
from services.configuration.models import segments as segment_models
from services.configuration.jrpc.serializers import serialization \
    as jrpc_serial


class TestGroupedRules(test.TestCase):
    """
    This class includes all the tests for the critical points of how to manage
    the rules into groups depending on the Ground Station.
    """

    def setUp(self):
        """
        Populates the initial database with a set of objects required to run
        the following tests.
        """
        self.__verbose_testing = False

        if not self.__verbose_testing:
            logging.getLogger('configuration').setLevel(level=logging.CRITICAL)
            logging.getLogger('simulation').setLevel(level=logging.CRITICAL)

        model_signals.connect_rules_2_availability()

        self.__gs_1_id = 'gs-castrelos'
        self.__gs_1_ch_1_id = 'chan-cas-1'
        self.__gs_1_ch_2_id = 'chan-cas-2'

        self.__band = db_tools.create_band()
        self.__user_profile = db_tools.create_user_profile()
        self.__gs_1 = db_tools.create_gs(
            user_profile=self.__user_profile, identifier=self.__gs_1_id,
        )
        self.__gs_1_ch_1 = db_tools.gs_add_channel(
            self.__gs_1, self.__band, self.__gs_1_ch_1_id
        )
        self.__gs_1_ch_2 = db_tools.gs_add_channel(
            self.__gs_1, self.__band, self.__gs_1_ch_2_id
        )

    def test_create_grouped_rules(self):
        """services.configuration: grouped rule management
        Validates the creation of a simple grouped rule
        """
        now = misc.get_now_utc()
        r_1_s_time = now + datetime.timedelta(minutes=30)
        r_1_e_time = now + datetime.timedelta(minutes=45)

        r_cfg = db_tools.create_jrpc_daily_rule(
            starting_time=r_1_s_time, ending_time=r_1_e_time
        )
        op, periodicity, dates = jrpc_serial.deserialize_rule_cfg(r_cfg)

        x_group_pks = {
            'group_id': 1,
            'rules': [2, 3]
        }
        a_group_pks = rule_models.GroupedAvailabilityRules.objects.create(
            self.__gs_1_id, op, periodicity, dates
        )
        # It should have created two identifiers
        self.assertEqual(
            a_group_pks, x_group_pks, 'Wrong result!'
        )

        # Two different rules should have been created, each of them for a
        # different channel.
        group = rule_models.GroupedAvailabilityRules.objects.get(
            groundstation=segment_models.GroundStation.objects.get(
                identifier=self.__gs_1_id
            )
        )

        self.assertEqual(
            group.groundstation.identifier, self.__gs_1_id,
            'Wrong ground station id!, a = ' + str(
                group.groundstation.identifier
            ) + ', x = ' + str(self.__gs_1_id)
        )
