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

from django import test

from services.common import helpers as db_tools
from services.scheduling.jrpc.views import compatibility as compatibility_jrpc


class TestCompatibilityViews(test.TestCase):
    """
    Tests for the compatibility JRPC views
    """

    def setUp(self):
        """
        Populates the initial database with a set of objects required to run
        the following tests.
        """
        self.__verbose_testing = True

        if not self.__verbose_testing:
            logging.getLogger('configuration').setLevel(level=logging.CRITICAL)

        # noinspection PyUnresolvedReferences
        from services.scheduling.signals import compatibility

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

        self.__sc_1_id = 'humd'
        self.__sc_1_ch_1_id = 'gmsk-sc-1'
        self.__sc_1_ch_1_f = 437000000
        self.__sc_1_ch_2_id = 'gmsk-sc-2'

        self.__sc_1 = db_tools.create_sc(
            user_profile=self.__user_profile,
            identifier=self.__sc_1_id
        )
        self.__sc_1_ch_1 = db_tools.sc_add_channel(
            self.__sc_1, self.__sc_1_ch_1_f, self.__sc_1_ch_1_id,
        )

    def test_sc_channel_get_compatible(self):
        """JRPC method: configuration.sc.channel.getCompatible
        """
        if self.__verbose_testing:
            print('>>> TEST (test_sc_channel_get_compatible)')

        c = compatibility_jrpc.sc_channel_get_compatible(
            self.__sc_1_id, self.__sc_1_ch_1_id
        )

        self.assertEquals(
            c[0]['GroundStation']['identifier'],
            self.__gs_1_id,
            'Wrong GS id!'
        )

    def test_sc_get_compatible(self):
        """JRPC method: configuration.sc.getCompatible
        """
        if self.__verbose_testing:
            print('>>> TEST (test_sc_get_compatible)')

        r = compatibility_jrpc.sc_get_compatible(self.__sc_1_id)

        self.assertEquals(
            r['spacecraft_id'], self.__sc_1_id, 'Wrong SC id!'
        )
        self.assertEquals(
            r['Compatibility'][0]['ScChannel']['identifier'],
            'gmsk-sc-1',
            "Wrong structure!"
        )
