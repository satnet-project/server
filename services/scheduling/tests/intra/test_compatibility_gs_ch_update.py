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

import logging

from django.test import TestCase

from services.common.testing import helpers as db_tools
from services.configuration.models import bands as band_models
from services.configuration.models import channels as channel_models
from services.scheduling.jrpc.views import compatibility as jrpc_compat_if


class CompatibilityGsChUpdate(TestCase):
    """
    Class with the UNIT tests for validating the INTRA modules within the
    configuration service.
    """

    def setUp(self):
        """
        Populates the initial database with a set of objects required to run
        the following tests.
        """
        self.__verbose_testing = False

        if not self.__verbose_testing:
            logging.getLogger('configuration').setLevel(level=logging.CRITICAL)
            logging.getLogger('scheduling').setLevel(level=logging.CRITICAL)
            logging.getLogger('simulation').setLevel(level=logging.CRITICAL)

        # noinspection PyUnresolvedReferences
        from services.scheduling.signals import compatibility

        self.__gs_1_id = 'gs-castrelos'
        self.__gs_1_ch_1_id = 'chan-cas-1'
        self.__gs_1_ch_2_id = 'chan-cas-2'
        self.__gs_1_ch_3_id = 'chan-cas-3'

        self.__sc_1_id = 'sc-xatcobeo'
        self.__sc_1_ch_1_id = 'xatco-fm-1'
        self.__sc_1_ch_1_f = 437000000
        self.__sc_1_ch_2_id = 'xatco-fm-2'
        self.__sc_1_ch_3_id = 'xatco-fm-3'
        self.__sc_1_ch_4_id = 'xatco-afsk-1'

        self.__band = db_tools.create_band()
        self.__user_profile = db_tools.create_user_profile()
        self.__gs = db_tools.create_gs(
            user_profile=self.__user_profile, identifier=self.__gs_1_id,
        )
        self.__sc = db_tools.create_sc(
            user_profile=self.__user_profile, identifier=self.__sc_1_id
        )

    def test_gs_channel_update_compatibility(self):
        """ services.configuration: diff compatibility
        """
        if self.__verbose_testing:
            print('##### test_compatibility_case_6')

        # (CHANGE-1)
        self.__sc_1_ch_1 = db_tools.sc_add_channel(
            self.__sc, self.__sc_1_ch_1_f, self.__sc_1_ch_1_id,
        )
        # (CHANGE-2)
        self.__sc_1_ch_2 = db_tools.sc_add_channel(
            self.__sc, self.__sc_1_ch_1_f, self.__sc_1_ch_2_id,
        )
        # (CHANGE-3)
        db_tools.gs_add_channel(
            self.__gs, self.__band, self.__gs_1_ch_1_id,
        )
        # (CHANGE-4)
        db_tools.gs_add_channel(
            self.__gs, self.__band, self.__gs_1_ch_2_id,
        )

        # 1) by default, no new channels if there is no changes
        gs_ch = channel_models.GroundStationChannel.objects.get(
            identifier=self.__gs_1_ch_1_id
        )

        c1 = jrpc_compat_if.sc_get_compatible(self.__sc_1_id)
        self.assertEquals(
            len(c1['Compatibility'][0]['Compatibility']),
            2,
            'Wrong compatibility'
        )

        # 2) changing the polarization should make the GS_CH incompatible
        gs_ch.polarizations.clear()
        gs_ch.polarizations.add(
            band_models.AvailablePolarizations.objects.get(
                polarization='LHCP'
            )
        )
        gs_ch.save()
        c2 = jrpc_compat_if.sc_get_compatible(self.__sc_1_id)
        self.assertEquals(
            len(c2['Compatibility'][0]['Compatibility']),
            1,
            'Wrong compatibility'
        )

        # 3) changing it to the original configuration
        gs_ch.polarizations.add(
            band_models.AvailablePolarizations.objects.get(
                polarization='RHCP'
            )
        )
        gs_ch.save()
        c3 = jrpc_compat_if.sc_get_compatible(self.__sc_1_id)
        self.assertEquals(
            len(c3['Compatibility'][0]['Compatibility']),
            2,
            'Wrong compatibility'
        )
