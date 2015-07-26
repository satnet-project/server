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
import logging

from django.test import TestCase

from services.common import misc
from services.common.testing import helpers as db_tools
from services.configuration.signals import models as model_signals
from services.configuration.jrpc.serializers import serialization as jrpc_serial
from services.configuration.jrpc.views import channels as jrpc_channels_if
from services.configuration.jrpc.views import compatibility as jrpc_compat_if


# noinspection PyBroadException
class JRPCChannelsTest(TestCase):
    """
    Class with the UNIT tests for JRPC methods concerning the access to the
    channels.
    """

    def setUp(self):
        """
        Populates the initial database with a set of objects required to run
        the following tests.
        """
        self.__verbose_testing = False

        if not self.__verbose_testing:
            logging.getLogger('configuration').setLevel(level=logging.CRITICAL)

        model_signals.connect_channels_2_compatibility()

        self.__gs_1_id = 'uvigo'
        self.__gs_1_ch_1_id = 'qpsk-gs-1'
        self.__gs_1_ch_2_id = 'qpsk-gs-2'

        self.__gs_2_id = 'calpoly'

        self.__sc_1_id = 'humd'
        self.__sc_1_ch_1_id = 'gmsk-sc-1'
        self.__sc_1_ch_1_f = 437000000
        self.__sc_1_ch_2_id = 'gmsk-sc-2'

        self.__sc_2_id = 'beesat'

        self.__band = db_tools.create_band()
        self.__test_user_profile = db_tools.create_user_profile()

        self.__gs_1 = db_tools.create_gs(
            user_profile=self.__test_user_profile, identifier=self.__gs_1_id,
        )
        self.__gs_1_ch_1 = db_tools.gs_add_channel(
            self.__gs_1, self.__band, self.__gs_1_ch_1_id
        )

        self.__gs_2 = db_tools.create_gs(
            user_profile=self.__test_user_profile, identifier=self.__gs_2_id,
        )

        self.__sc_1 = db_tools.create_sc(
            user_profile=self.__test_user_profile,
            identifier=self.__sc_1_id
        )
        self.__sc_2 = db_tools.create_sc(
            user_profile=self.__test_user_profile,
            identifier=self.__sc_2_id
        )
        self.__sc_1_ch_1 = db_tools.sc_add_channel(
            self.__sc_1, self.__sc_1_ch_1_f, self.__sc_1_ch_1_id,
        )

        if not self.__verbose_testing:
            logging.getLogger('configuration').setLevel(level=logging.CRITICAL)
            logging.getLogger('simulation').setLevel(level=logging.CRITICAL)

    def test_sc_channel_update_compatibility(self):
        """INTRA configuration: SC channel update provokes compatibility change
        """

        self.assertEqual(
            jrpc_compat_if.sc_channel_get_compatible(
                self.__sc_1_id, self.__sc_1_ch_1_id
            ),
            {

            },
            'Wrong compat!!!'
        )

        expected_c = {
            jrpc_serial.CH_ID_K: self.__sc_1_ch_1_id,
            jrpc_serial.FREQUENCY_K: 438000000,
            jrpc_serial.MODULATION_K: 'FM',
            jrpc_serial.POLARIZATION_K: 'RHCP',
            jrpc_serial.BITRATE_K: 600,
            jrpc_serial.BANDWIDTH_K: 25
        }

        self.assertEqual(
            jrpc_channels_if.sc_channel_set_configuration(
                self.__sc_1_id, self.__sc_1_ch_1_id, expected_c
            ),
            True,
            'Configuration should have been set correctly!'
        )

        actual_c = jrpc_channels_if.sc_channel_get_configuration(
            self.__sc_1_id, self.__sc_1_ch_1_id
        )

        if self.__verbose_testing:
            misc.print_dictionary(actual_c)
            misc.print_dictionary(expected_c)

        self.assertEqual(
            actual_c, expected_c,
            'Configuration dictionaries do not match!, diff = \n'
            + str(datadiff.diff(actual_c, expected_c))
        )
