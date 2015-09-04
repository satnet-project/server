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

import datadiff

from django.test import TestCase

from services.common.testing import helpers as db_tools
from services.configuration.models import channels as channel_models
from services.scheduling.models import compatibility as compatibility_models
from services.configuration.jrpc.serializers import \
    channels as channel_serializers
from services.configuration.jrpc.views.channels import spacecraft\
    as jrpc_sc_ch_if
from services.scheduling.jrpc.views import compatibility as jrpc_compat_if


# noinspection PyBroadException
class CompatibilityScChUpdate(TestCase):
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

    def test_sc_channel_update_compatibility(self):
        """INTRA scheduling: SC channel update provokes compatibility change
        Initially, the just created spacecraft channel should be compatible
        with the also created Ground Station channel. However, after the
        update they become incompatible and, therefore, this fact should be
        reflected in the compatibility table.
        """

        # 0) initially, the channels are compatible
        compatibility = jrpc_compat_if.sc_channel_get_compatible(
            self.__sc_1_id, self.__sc_1_ch_1_id
        )

        self.assertEqual(
            compatibility[0]['GroundStation']['identifier'],
            'uvigo',
            'Wrong compat!!!'
        )

        # 1) new configuration makes channels incompatible
        expected_c = {
            channel_serializers.CH_ID_K: self.__sc_1_ch_1_id,
            channel_serializers.FREQUENCY_K: 2000000000,
            channel_serializers.MODULATION_K: 'FM',
            channel_serializers.POLARIZATION_K: 'RHCP',
            channel_serializers.BITRATE_K: 600,
            channel_serializers.BANDWIDTH_K: 25
        }

        self.assertTrue(
            jrpc_sc_ch_if.sc_channel_set_configuration(
                self.__sc_1_id, self.__sc_1_ch_1_id, expected_c
            ),
            'Configuration should have been set correctly!'
        )

        actual_c = jrpc_sc_ch_if.sc_channel_get_configuration(
            self.__sc_1_id, self.__sc_1_ch_1_id
        )

        self.assertEqual(
            actual_c, expected_c,
            'Wrong configuration! diff = ' + str(
                datadiff.diff(actual_c, expected_c)
            )
        )

        self.assertEquals(
            jrpc_compat_if.sc_channel_get_compatible(
                self.__sc_1_id, self.__sc_1_ch_1_id
            ),
            [],
            'No compatible channels should have been found, diff = ' + str(
                datadiff.diff(compatibility, [])
            )
        )

        compatibility = jrpc_compat_if.sc_get_compatible(self.__sc_1_id)
        self.assertEquals(
            compatibility['spacecraft_id'], self.__sc_1_id,
            'Wrong compatiblity!'
        )
        self.assertEquals(
            compatibility['Compatibility'][0]['ScChannel']['identifier'],
            self.__sc_1_ch_1_id,
            'Wrong compatiblity!'
        )
        self.assertEquals(
            compatibility['Compatibility'][0]['Compatibility'],
            [],
            'Wrong compatiblity!'
        )

        # 2) this new configuration should make the channels compatible again
        expected_c = {
            channel_serializers.CH_ID_K: self.__sc_1_ch_1_id,
            channel_serializers.FREQUENCY_K: 436365000,
            channel_serializers.MODULATION_K: 'FM',
            channel_serializers.POLARIZATION_K: 'RHCP',
            channel_serializers.BITRATE_K: 600,
            channel_serializers.BANDWIDTH_K: 25
        }

        self.assertTrue(
            jrpc_sc_ch_if.sc_channel_set_configuration(
                self.__sc_1_id, self.__sc_1_ch_1_id, expected_c
            ),
            'Configuration should have been set correctly!'
        )

        actual_c = jrpc_sc_ch_if.sc_channel_get_configuration(
            self.__sc_1_id, self.__sc_1_ch_1_id
        )

        self.assertEqual(
            actual_c, expected_c,
            'Wrong configuration! diff = ' + str(
                datadiff.diff(actual_c, expected_c)
            )
        )

        compatibility = jrpc_compat_if.sc_channel_get_compatible(
            self.__sc_1_id, self.__sc_1_ch_1_id
        )

        self.assertEqual(
            compatibility[0]['GroundStation']['identifier'],
            'uvigo',
            'Wrong compat!!!'
        )

        # 3) deleting the spacecraft channel should erase the compatibility
        self.assertTrue(
            jrpc_sc_ch_if.sc_channel_delete(
                self.__sc_1_id, self.__sc_1_ch_1_id
            ),
            'Could not properly remove spacecraft channel!'
        )

        try:
            channel_models.SpacecraftChannel.objects.get(
                identifier=self.__sc_1_ch_1_id
            )
            self.fail('SC channel should have not been found!')
        except Exception:
            pass

        try:
            jrpc_compat_if.sc_channel_get_compatible(
                self.__sc_1_id, self.__sc_1_ch_1_id
            )
            self.fail(
                'Spacecraft Channel DoesNotExist, an exception should have been'
                'thrown'
            )
        except Exception:
            pass

        try:
            jrpc_compat_if.sc_get_compatible(
                self.__sc_1_id, self.__sc_1_ch_1_id
            )
            self.fail(
                'Spacecraft Channel DoesNotExist, an exception should have been'
                'thrown'
            )
        except Exception:
            pass

        self.assertEquals(
            len(compatibility_models.ChannelCompatibility.objects.all()), 0,
            'No compatibility objects should have been found '
        )
