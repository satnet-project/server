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

from datetime import timedelta
from django.test import TestCase

import common.testing as db_tools
from common.misc import get_today_utc, print_list
import configuration.jrpc.rules as jrpc_rules
import configuration.jrpc.serialization as jrpc_keys
from configuration.models.channels import GroundStationChannel
from configuration.models.bands import AvailablePolarizations
from configuration.models.segments import GroundStationConfiguration,\
    ChannelsCompatibility
from configuration.models.rules import AvailabilityRule,\
    AvailabilityRuleManager


class TestModels(TestCase):
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
        self.__verbose_testing = False

        self.__gs_1_id = 'gs-castrelos'
        self.__gs_1_ch_1_id = 'chan-cas-1'

        self.__sc_1_id = 'sc-xatcobeo'
        self.__sc_1_ch_1_id = 'xatco-fm-1'
        self.__sc_1_ch_2_id = 'xatco-fm-2'
        self.__sc_1_ch_3_id = 'xatco-fm-3'
        self.__sc_1_ch_4_id = 'xatco-afsk-1'

        db_tools.init_available()
        self.__band = db_tools.create_band()
        self.__test_user_profile = db_tools.create_user_profile()
        self.__gs = db_tools.create_gs(
            user_profile=self.__test_user_profile, identifier=self.__gs_1_id,
        )
        self.__sc = db_tools.create_sc(
            user_profile=self.__test_user_profile, identifier=self.__sc_1_id
        )

    def get_availability_slots(self):
        """
        This test validates the generation of slots by the different rules
        supported by the configuration service.
        """
        if self.__verbose_testing:
            print '>>>>> get_availability_slots'

        gs = db_tools.create_gs(
            user_profile=self.__test_user_profile,
            identifier=self.__gs_1_id,
        )
        db_tools.gs_add_channel(
            gs, self.__band,
            self.__gs_1_id, self.__gs_1_ch_1_id
        )

        rule_1 = db_tools.create_jrpc_once_rule(
            operation=jrpc_keys.RULE_OP_REMOVE,
            date=get_today_utc() + timedelta(days=2)
        )
        jrpc_rules.add_rule(self.__gs_1_id, self.__gs_1_ch_1_id, rule_1)

        rule_2 = db_tools.create_jrpc_daily_rule()
        jrpc_rules.add_rule(self.__gs_1_id, self.__gs_1_ch_1_id, rule_2)

        rule_3 = db_tools.create_jrpc_once_rule(
            operation=jrpc_keys.RULE_OP_REMOVE,
            date=get_today_utc() + timedelta(days=3)
        )
        jrpc_rules.add_rule(self.__gs_1_id, self.__gs_1_ch_1_id, rule_3)

        rule_4 = db_tools.create_jrpc_once_rule(
            operation=jrpc_keys.RULE_OP_REMOVE,
            date=get_today_utc() + timedelta(days=3)
        )
        jrpc_rules.add_rule(self.__gs_1_id, self.__gs_1_ch_1_id, rule_4)

        ch_1_pk = GroundStationChannel\
            .objects.get(identifier=self.__gs_1_ch_1_id).pk
        rules_ch_1_n = len(AvailabilityRule.objects
                           .filter(gs_channel_id=ch_1_pk).all())
        self.assertEquals(rules_ch_1_n, 3, 'Incorrect number of rules.')

        ch = GroundStationConfiguration.objects.get_channel(
            ground_station_id=self.__gs_1_id,
            channel_id=self.__gs_1_ch_1_id
        )
        actual_s = AvailabilityRuleManager.get_availability_slots(ch)
        if self.__verbose_testing:
            print_list(actual_s, 'AVAILABLE SLOTS')

        self.assertEquals(len(actual_s), 8, 'Wrong number of available slots.')

    def test_find_compatible_sc_channels(self):
        """
        Tests the process for identifying the compatible channels once a new
        channel for a Ground Station has been added to the system.
        """
        if self.__verbose_testing:
            print '>>>>> test_find_compatible_sc_channels'

        db_tools.gs_add_channel(
            self.__gs, self.__band, self.__gs_1_ch_1_id,
            polarizations=[AvailablePolarizations.objects.get(
                polarization='RHCP'
            )]
        )

        # 0) First test, no sc channels available >>> NO COMPATIBLE!
        c_chs = ChannelsCompatibility.objects.find_compatible_sc_channels(
            self.__gs_1_ch_1_id
        )
        self.assertEquals(len(c_chs), 0, 'Wrong number of compatible chs')

        # 1) Second test, one sc channel compatible
        db_tools.sc_add_channel(self.__sc, 437000000, self.__sc_1_ch_1_id)
        c_chs = ChannelsCompatibility.objects\
            .find_compatible_sc_channels(self.__gs_1_ch_1_id)
        self.assertEquals(len(c_chs), 1, 'Wrong number of compatible chs')

        # 2) Third test, two sc channels compatible
        db_tools.sc_add_channel(self.__sc, 437100000, self.__sc_1_ch_2_id)
        c_chs = ChannelsCompatibility.objects\
            .find_compatible_sc_channels(self.__gs_1_ch_1_id)
        self.assertEquals(len(c_chs), 2, 'Wrong number of compatible chs')

        # 3) Fourth test, two out of three sc channels are compatible.
        db_tools.sc_add_channel(self.__sc, 500000000, self.__sc_1_ch_3_id)
        c_chs = ChannelsCompatibility.objects\
            .find_compatible_sc_channels(self.__gs_1_ch_1_id)
        self.assertEquals(len(c_chs), 2, 'Wrong number of compatible chs')

        # 4) Third test, two sc channels compatible
        db_tools.sc_add_channel(
            self.__sc, 437100000, self.__sc_1_ch_4_id,
            polarization=AvailablePolarizations.objects.get(
                polarization='LHCP'
            )
        )
        c_chs = ChannelsCompatibility.objects\
            .find_compatible_sc_channels(self.__gs_1_ch_1_id)
        self.assertEquals(len(c_chs), 2, 'Wrong number of compatible chs')

        # ### We delete all channel objects from the database
        db_tools.remove_sc_channel(self.__sc_1_ch_1_id)
        db_tools.remove_sc_channel(self.__sc_1_ch_2_id)
        db_tools.remove_sc_channel(self.__sc_1_ch_3_id)
        db_tools.remove_sc_channel(self.__sc_1_ch_4_id)
        db_tools.remove_gs_channel(self.__gs_1_id, self.__gs_1_ch_1_id)

    def test_find_compatible_gs_channels(self):
        """
        Tests the process for identifying the compatible channels once a new
        channel for a Spacecraft has been added to the system.
        """
        if self.__verbose_testing:
            print '>>>>> find_compatible_gs_channels'

        db_tools.sc_add_channel(self.__sc, 437000000, self.__sc_1_ch_1_id)

        # 0) First test, no GS channels available >>> NO COMPATIBLE!
        c_chs = ChannelsCompatibility.objects\
            .find_compatible_gs_channels(self.__sc_1_ch_1_id)
        self.assertEquals(len(c_chs), 0, 'Wrong number of compatible chs')

        # ### We delete all channel objects from the database
        db_tools.remove_sc_channel(self.__sc_1_ch_1_id)

    def test_new_gs_channel(self):
        """
        Tests the method that handles the addition of a new GS channel to the
        table of compatible channels.
        """
        if self.__verbose_testing:
            print '>>>>> test_new_gs_channel'

        db_tools.gs_add_channel(
            self.__gs, self.__band, self.__gs_1_ch_1_id,
            polarizations=[AvailablePolarizations.objects.get(
                polarization='RHCP'
            )]
        )
        # 0) First test, no SC channels available >>> NO CHANGES!
        ChannelsCompatibility.objects.new_gs_channel(
            self.__gs_1_ch_1_id
        )
        self.assertEquals(
            len(ChannelsCompatibility.objects.all()),
            0,
            'Table must be empty!'
        )
        db_tools.remove_gs_channel(self.__gs_1_id, self.__gs_1_ch_1_id)

        # 1) Second test, we add a single compatible SC channel and, later,
        # we add the new GS channel. The first step should generate one new
        # entry in the table with no associated GS channels.
        sc_ch = db_tools.sc_add_channel(
            self.__sc, 437000000, self.__sc_1_ch_1_id
        )
        self.assertEquals(
            len(ChannelsCompatibility.objects.all()), 1,
            'Table must have 1 item!'
        )
        cch = ChannelsCompatibility.objects.get(spacecraft_channel=sc_ch)
        self.assertEquals(
            len(cch.compatible_groundstation_chs.all()), 0,
            'No GS channels should be found!'
        )
        db_tools.gs_add_channel(
            self.__gs, self.__band, self.__gs_1_ch_1_id,
            polarizations=[AvailablePolarizations.objects.get(
                polarization='RHCP'
            )]
        )
        self.assertEquals(
            len(ChannelsCompatibility.objects.all()), 1,
            'Table must have 1 item!'
        )
        self.assertEquals(
            len(cch.compatible_groundstation_chs.all()), 1,
            'One GS channels should\'ve be found!'
        )

        # ### We remove the ground station channel and, therefore,
        # the CompatibleChannels table should be updated accordingly...
        db_tools.remove_gs_channel(self.__gs_1_id, self.__gs_1_ch_1_id)
        self.assertEquals(
            len(ChannelsCompatibility.objects.all()), 1,
            'Table must have 1 item!'
        )
        self.assertEquals(
            len(cch.compatible_groundstation_chs.all()), 0,
            'There should not be any GroundStation channels!'
        )

        # ### We now remove the spacecraft channel and we expect the
        # CompatibleChannels table to be updated accordingly...
        db_tools.remove_sc_channel(self.__sc_1_ch_1_id)
        self.assertEquals(
            len(ChannelsCompatibility.objects.all()),
            0,
            'Table must be empty!'
        )