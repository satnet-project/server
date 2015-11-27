"""
   Copyright 2015 Ricardo Tubio-Pardavila

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

from django.test import TestCase

from services.common import helpers as db_tools
from services.configuration.jrpc.views.segments import groundstations as \
    jrpc_gs_if
from services.configuration.jrpc.views.segments import spacecraft as \
    jrpc_sc_if
from services.configuration.models import channels as channel_models


# noinspection PyBroadException
class SegmentsChannelsCascade(TestCase):
    """
    This class contains a set of basic tests used to demonstrate the CASCADE
    dependency among segments and channels; this is, the deletion of a given
    segment must delete all the associated channels.
    """

    def setUp(self):
        """
        Populates the initial database with a set of objects required to run
        the following tests.
        """
        self.__verbose_testing = False

        if not self.__verbose_testing:
            logging.getLogger('configuration').setLevel(level=logging.CRITICAL)

        self.__gs_id = 'uvigo'
        self.__gs_ch_1_id = 'qpsk-gs-1'
        self.__gs_ch_2_id = 'qpsk-gs-2'

        self.__sc_id = 'humd'
        self.__sc_ch_1_id = 'gmsk-sc-1'
        self.__sc_ch_f = 437000000
        self.__sc_ch_2_id = 'gmsk-sc-2'

        self.__sc_id = 'beesat'

        self.__band = db_tools.create_band()
        self.__test_user_profile = db_tools.create_user_profile()

        self.__gs = db_tools.create_gs(
            user_profile=self.__test_user_profile, identifier=self.__gs_id,
        )
        self.__gs_ch_1 = db_tools.gs_add_channel(
            self.__gs, self.__band, self.__gs_ch_1_id
        )
        self.__gs_ch_2 = db_tools.gs_add_channel(
            self.__gs, self.__band, self.__gs_ch_2_id
        )

        self.__sc = db_tools.create_sc(
            user_profile=self.__test_user_profile,
            identifier=self.__sc_id
        )
        self.__sc_ch_1 = db_tools.sc_add_channel(
            self.__sc, self.__sc_ch_f, self.__sc_ch_1_id,
        )
        self.__sc_ch_2 = db_tools.sc_add_channel(
            self.__sc, self.__sc_ch_f, self.__sc_ch_2_id,
        )

    def test_gs_cascade(self):
        """INTR test: GS channels cascade deletion
        """

        self.assertEquals(
            len(
                channel_models.GroundStationChannel.objects.filter(
                    groundstation__identifier=self.__gs_id
                )
            ),
            2,
            'Ground Station should have no channels'
        )

        self.assertTrue(
            jrpc_gs_if.delete(self.__gs_id),
            'Ground Station channel should have been properly deleted'
        )

        self.assertEquals(
            len(
                channel_models.GroundStationChannel.objects.filter(
                    groundstation__identifier=self.__gs_id
                )
            ),
            0,
            'Ground Station should have no channels'
        )

    def test_sc_cascade(self):
        """INTR test: SC channels cascade deletion
        """

        self.assertEquals(
            len(
                channel_models.SpacecraftChannel.objects.filter(
                    spacecraft__identifier=self.__sc_id
                )
            ),
            2,
            'Spacecraft should have no channels'
        )

        self.assertTrue(
            jrpc_sc_if.delete(self.__sc_id),
            'Spacecraft channel should have been properly deleted'
        )

        self.assertEquals(
            len(
                channel_models.SpacecraftChannel.objects.filter(
                    spacecraft__identifier=self.__sc_id
                )
            ),
            0,
            'Spacecraft should have no channels'
        )
