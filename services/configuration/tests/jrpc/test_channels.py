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
from django.db.models import ObjectDoesNotExist
from django.test import TestCase

from services.common import misc, helpers as db_tools
from services.configuration.jrpc.serializers import \
    channels as channel_serializers
from services.configuration.jrpc.views import bands as band_jrpc
from services.configuration.jrpc.views.channels import groundstations as \
    jrpc_gs_channels_if
from services.configuration.jrpc.views.channels import spacecraft as \
    jrpc_sc_channels_if


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

    def test_gs_get_channel_list(self):
        """JRPC test: configuration.gs.channel.list
        """
        if self.__verbose_testing:
            print('>>> TEST (test_gs_get_channel_list)')

        try:
            jrpc_gs_channels_if.gs_channel_list('FAKE')
            self.fail('An exception should have been thrown!')
        except ObjectDoesNotExist:
            pass

        self.assertEquals(
            jrpc_gs_channels_if.gs_channel_list(self.__gs_2_id),
            [],
            'Should have returned an empty array'
        )

        self.assertEquals(
            jrpc_gs_channels_if.gs_channel_list(self.__gs_1_id),
            [self.__gs_1_ch_1_id],
            'Should have returned a non-empty array'
        )

    def test_sc_get_channel_list(self):
        """JRPC test: configuration.sc.channel.list
        """
        if self.__verbose_testing:
            print('>>> TEST (test_sc_get_channel_list)')

        try:
            jrpc_sc_channels_if.sc_channel_list('FAKE')
            self.fail('An exception should have been thrown!')
        except ObjectDoesNotExist:
            pass

        self.assertEquals(
            jrpc_sc_channels_if.sc_channel_list(self.__sc_2_id),
            [],
            'Should have returned an empty array'
        )

        self.assertEquals(
            jrpc_sc_channels_if.sc_channel_list(self.__sc_1_id),
            [self.__sc_1_ch_1_id],
            'Should have returned a non-empty array'
        )

    def test_get_channel_options(self):
        """JRPC test: configuration.channels.getOptions
        """
        if self.__verbose_testing:
            print('>>> TEST (test_get_channel_options)')

        actual_o = band_jrpc.get_options()
        expected_o = {
            channel_serializers.BANDS_K: [
                'UHF / U / 435000000.000000 / 438000000.000000'
            ],
            channel_serializers.MODULATIONS_K: ['FM', 'AFSK'],
            channel_serializers.POLARIZATIONS_K: ['LHCP', 'RHCP'],
            channel_serializers.BITRATES_K: ['300', '600', '900'],
            channel_serializers.BANDWIDTHS_K: ['12.500000000', '25.000000000']
        }
        self.assertEqual(
            actual_o, expected_o,
            'Options differ! diff = ' + str(
                datadiff.diff(actual_o, expected_o)
            )
        )

    def test_gs_channel_is_unique(self):
        """JRPC test: configuration.gs.channel.isUnique
        """
        if self.__verbose_testing:
            print('>>> TEST (test_gs_channel_is_unique)')

        self.assertTrue(
            jrpc_gs_channels_if.gs_channel_is_unique(self.__gs_1_ch_1_id),
            'Channel should exist already!'
        )
        self.assertFalse(
            jrpc_gs_channels_if.gs_channel_is_unique('CH-FAKE'),
            'Channel should not exist yet!'
        )

    def test_sc_channel_is_unique(self):
        """JRPC test: configuration.sc.channel.isUnique
        """
        if self.__verbose_testing:
            print('>>> TEST (test_sc_channel_is_unique)')

        self.assertTrue(
            jrpc_sc_channels_if.sc_channel_is_unique(self.__sc_1_ch_1_id),
            'Channel should exist already!'
        )
        self.assertFalse(
            jrpc_sc_channels_if.sc_channel_is_unique('CH-FAKE'),
            'Channel should not exist yet!'
        )

    def test_gs_channel_create(self):
        """JRPC test: configuration.gs.channel.create
        """
        if self.__verbose_testing:
            print('>>> TEST (test_gs_channel_create)')

        try:
            jrpc_gs_channels_if.gs_channel_create(
                groundstation_id='FAKE-GS',
                channel_id=self.__gs_1_ch_2_id,
                configuration={
                    channel_serializers.BAND_K:
                        'UHF / U / 435000000.000000 / 438000000.000000',
                    channel_serializers.AUTOMATED_K: False,
                    channel_serializers.MODULATIONS_K: ['FM'],
                    channel_serializers.POLARIZATIONS_K: ['LHCP'],
                    channel_serializers.BITRATES_K: [300, 600, 900],
                    channel_serializers.BANDWIDTHS_K: [12.500000000]
                }
            )
            self.fail('An exception should have been thrown!')
        except Exception:
            pass

        self.assertTrue(
            jrpc_gs_channels_if.gs_channel_create(
                groundstation_id=self.__gs_1_id,
                channel_id=self.__gs_1_ch_2_id,
                configuration={
                    channel_serializers.BAND_K:
                        'UHF / U / 435000000.000000 / 438000000.000000',
                    channel_serializers.AUTOMATED_K: False,
                    channel_serializers.MODULATIONS_K: ['FM'],
                    channel_serializers.POLARIZATIONS_K: ['LHCP'],
                    channel_serializers.BITRATES_K: [300, 600, 900],
                    channel_serializers.BANDWIDTHS_K: [12.500000000]
                }
            ),
            'Channel should have been created!'
        )
        db_tools.remove_gs_channel(self.__gs_1_id, self.__gs_1_ch_2_id)

    def test_sc_channel_create(self):
        """JRPC test: configuration.sc.channel.create
        """
        if self.__verbose_testing:
            print('>>> TEST (test_sc_channel_create)')

        try:
            jrpc_sc_channels_if.sc_channel_create(
                spacecraft_id='FAKE-SC',
                channel_id=self.__sc_1_ch_2_id,
                configuration={
                    channel_serializers.FREQUENCY_K: '437000000',
                    channel_serializers.MODULATION_K: 'FM',
                    channel_serializers.POLARIZATION_K: 'LHCP',
                    channel_serializers.BITRATE_K: '300',
                    channel_serializers.BANDWIDTH_K: '12.500000000'
                }
            )
            self.fail('An exception should have been thrown!')
        except Exception:
            pass

        self.assertTrue(
            jrpc_sc_channels_if.sc_channel_create(
                spacecraft_id=self.__sc_1_id,
                channel_id=self.__sc_1_ch_2_id,
                configuration={
                    channel_serializers.FREQUENCY_K: '437000000',
                    channel_serializers.MODULATION_K: 'FM',
                    channel_serializers.POLARIZATION_K: 'LHCP',
                    channel_serializers.BITRATE_K: '300',
                    channel_serializers.BANDWIDTH_K: '12.500000000'
                }
            ),
            'Channel should have been created!'
        )
        db_tools.remove_sc_channel(self.__sc_1_ch_2_id)

    def test_gs_channel_delete(self):
        """JRPC test: configuration.gs.channel.delete
        """
        try:
            jrpc_gs_channels_if.gs_channel_delete(
                'FAKE-GS', 'FAKE-GS-CHANNEL'
            )
            self.fail('An exception should have been thrown!')
        except Exception:
            pass

        try:
            jrpc_gs_channels_if.gs_channel_delete(
                self.__gs_1_id, 'FAKE-GS-CHANNEL'
            )
            self.fail('An exception should have been thrown!')
        except Exception:
            pass

        self.assertTrue(
            jrpc_gs_channels_if.gs_channel_create(
                groundstation_id=self.__gs_1_id,
                channel_id=self.__gs_1_ch_2_id,
                configuration={
                    channel_serializers.BAND_K:
                        'UHF / U / 435000000.000000 / 438000000.000000',
                    channel_serializers.AUTOMATED_K: False,
                    channel_serializers.MODULATIONS_K: ['FM'],
                    channel_serializers.POLARIZATIONS_K: ['LHCP'],
                    channel_serializers.BITRATES_K: [300, 600, 900],
                    channel_serializers.BANDWIDTHS_K: [12.500000000]
                }
            ),
            'Channel should have been created!'
        )
        self.assertTrue(
            jrpc_gs_channels_if.gs_channel_delete(
                self.__gs_1_id, self.__gs_1_ch_2_id
            ),
            'Channel should have been removed!'
        )
        self.assertFalse(
            jrpc_gs_channels_if.gs_channel_is_unique(self.__gs_1_ch_2_id),
            'Channel should not exist yet!'
        )

    def test_sc_channel_delete(self):
        """JRPC test: configuration.sc.channel.delete
        """
        try:
            jrpc_sc_channels_if.sc_channel_delete(
                'FAKE-SC', 'FAKE-SC-CHANNEL'
            )
            self.fail('An exception should have been thrown!')
        except Exception:
            pass

        try:
            jrpc_sc_channels_if.sc_channel_delete(
                self.__sc_1_id, 'FAKE-SC-CHANNEL'
            )
            self.fail('An exception should have been thrown!')
        except Exception:
            pass

        self.assertTrue(
            jrpc_sc_channels_if.sc_channel_create(
                spacecraft_id=self.__sc_1_id,
                channel_id=self.__sc_1_ch_2_id,
                configuration={
                    channel_serializers.FREQUENCY_K: '437000000',
                    channel_serializers.MODULATION_K: 'FM',
                    channel_serializers.POLARIZATION_K: 'LHCP',
                    channel_serializers.BITRATE_K: '300',
                    channel_serializers.BANDWIDTH_K: '12.500000000'
                }
            ),
            'Channel should have been created!'
        )
        self.assertTrue(
            jrpc_sc_channels_if.sc_channel_delete(
                self.__sc_1_id, self.__sc_1_ch_2_id
            ),
            'Channel should have been removed!'
        )
        self.assertFalse(
            jrpc_sc_channels_if.sc_channel_is_unique(self.__sc_1_ch_2_id),
            'Channel should not exist yet!'
        )

    def test_gs_channel_get_configuration(self):
        """JRPC test: configuration.gs.channel.getConfiguration
        """
        try:
            jrpc_gs_channels_if.gs_channel_get_configuration(
                'FAKE-GS', 'FAKE-GS-CHANNEL'
            )
            self.fail('An exception should have been thrown!')
        except Exception:
            pass
        try:
            jrpc_gs_channels_if.gs_channel_get_configuration(
                self.__gs_1_id, 'FAKE-GS-CHANNEL'
            )
            self.fail('An exception should have been thrown!')
        except Exception:
            pass

        expected_c = {
            channel_serializers.CH_ID_K: self.__gs_1_ch_2_id,
            channel_serializers.BAND_K:
                'UHF / U / 435000000.000000 / 438000000.000000',
            channel_serializers.AUTOMATED_K: False,
            channel_serializers.MODULATIONS_K: ['FM'],
            channel_serializers.POLARIZATIONS_K: ['LHCP'],
            channel_serializers.BITRATES_K: [300, 600, 900],
            channel_serializers.BANDWIDTHS_K: [12.500000000]
        }
        self.assertTrue(
            jrpc_gs_channels_if.gs_channel_create(
                groundstation_id=self.__gs_1_id,
                channel_id=self.__gs_1_ch_2_id,
                configuration=expected_c
            ),
            'Channel should have been created!'
        )

        actual_c = jrpc_gs_channels_if.gs_channel_get_configuration(
            self.__gs_1_id, self.__gs_1_ch_2_id
        )

        if self.__verbose_testing:
            misc.print_dictionary(actual_c)
            misc.print_dictionary(expected_c)
            print(datadiff.diff(actual_c, expected_c))

        self.assertEqual(
            actual_c, expected_c,
            'Configuration dictionaries do not match! Diff = ' + str(
                datadiff.diff(actual_c, expected_c)
            )
        )
        db_tools.remove_gs_channel(self.__gs_1_id, self.__gs_1_ch_2_id)

    def test_sc_channel_get_configuration(self):
        """JRPC test: configuration.sc.channel.getConfiguration
        """
        try:
            jrpc_sc_channels_if.sc_channel_get_configuration(
                'FAKE-SC', 'FAKE-SC-CHANNEL'
            )
            self.fail('An exception should have been thrown!')
        except Exception:
            pass
        try:
            jrpc_sc_channels_if.sc_channel_get_configuration(
                self.__sc_1_id, 'FAKE-SC-CHANNEL'
            )
            self.fail('An exception should have been thrown!')
        except Exception:
            pass

        expected_c = {
            channel_serializers.CH_ID_K: self.__sc_1_ch_2_id,
            channel_serializers.FREQUENCY_K: 437000000,
            channel_serializers.MODULATION_K: 'FM',
            channel_serializers.POLARIZATION_K: 'LHCP',
            channel_serializers.BITRATE_K: 300,
            channel_serializers.BANDWIDTH_K: 12.500000000
        }

        self.assertEqual(
            jrpc_sc_channels_if.sc_channel_create(
                spacecraft_id=self.__sc_1_id,
                channel_id=self.__sc_1_ch_2_id,
                configuration=expected_c
            ), True, 'Channel should have been created!'
        )

        actual_c = jrpc_sc_channels_if.sc_channel_get_configuration(
            self.__sc_1_id, self.__sc_1_ch_2_id
        )

        if self.__verbose_testing:
            misc.print_dictionary(actual_c)
            misc.print_dictionary(expected_c)
            print(datadiff.diff(actual_c, expected_c))

        self.assertEqual(
            actual_c, expected_c,
            'Configuration dictionaries do not match!'
        )
        db_tools.remove_sc_channel(self.__sc_1_ch_2_id)

    def test_gs_channel_set_configuration(self):
        """JRPC test: configuration.gs.channel.setConfiguration
        """
        self.__verbose_testing = False
        try:
            jrpc_gs_channels_if.gs_channel_set_configuration(
                'FAKE-GS', 'FAKE-GS-CHANNEL', None
            )
            self.fail('An exception should have been thrown!')
        except Exception:
            pass
        try:
            jrpc_gs_channels_if.gs_channel_set_configuration(
                self.__gs_1_id, 'FAKE-GS-CHANNEL', None
            )
            self.fail('An exception should have been thrown!')
        except Exception:
            pass
        try:
            jrpc_gs_channels_if.gs_channel_set_configuration(
                self.__gs_1_id, self.__gs_1_ch_1_id, None
            )
            self.fail('An exception should have been thrown!')
        except Exception:
            pass
        try:
            jrpc_gs_channels_if.gs_channel_set_configuration(
                self.__gs_1_id, self.__gs_1_ch_1_id, {}
            )
            self.fail('An exception should have been thrown!')
        except Exception:
            pass

        jrpc_gs_channels_if.gs_channel_get_configuration(
            self.__gs_1_id, self.__gs_1_ch_1_id
        )

        try:
            jrpc_gs_channels_if.gs_channel_set_configuration(
                self.__gs_1_id, self.__gs_1_ch_1_id, {
                    channel_serializers.BAND_K:
                        'UHF / U / 435000000.000000 / 438000000.000000',
                    channel_serializers.AUTOMATED_K: False,
                    channel_serializers.MODULATIONS_K: ['HM'],
                    channel_serializers.POLARIZATIONS_K: ['LHCP'],
                    channel_serializers.BITRATES_K: [600],
                    channel_serializers.BANDWIDTHS_K: [25]
                }
            )
            self.fail('An exception should have been thrown!')
        except Exception:
            pass

        try:
            jrpc_gs_channels_if.gs_channel_set_configuration(
                self.__gs_1_id, self.__gs_1_ch_1_id, {
                    channel_serializers.BAND_K:
                    'UHF / U / 435000000.000000 / 438000000.000000',
                    channel_serializers.AUTOMATED_K: False,
                    channel_serializers.MODULATIONS_K: ['FM'],
                    channel_serializers.POLARIZATIONS_K: ['XHHMP'],
                    channel_serializers.BITRATES_K: [600],
                    channel_serializers.BANDWIDTHS_K: [25]
                }
            )
            self.fail('An exception should have been thrown!')
        except Exception:
            pass

        expected_c = {
            channel_serializers.CH_ID_K: self.__gs_1_ch_1_id,
            channel_serializers.BAND_K:
                'UHF / U / 435000000.000000 / 438000000.000000',
            channel_serializers.AUTOMATED_K: False,
            channel_serializers.MODULATIONS_K: [str('AFSK'), str('FM')],
            channel_serializers.POLARIZATIONS_K: [str('LHCP'), str('RHCP')],
            channel_serializers.BITRATES_K: [300, 600],
            channel_serializers.BANDWIDTHS_K: [25]
        }

        self.assertEqual(
            jrpc_gs_channels_if.gs_channel_set_configuration(
                self.__gs_1_id, self.__gs_1_ch_1_id, expected_c
            ),
            True,
            'Configuration should have been set correctly!'
        )

        actual_c = jrpc_gs_channels_if.gs_channel_get_configuration(
            self.__gs_1_id, self.__gs_1_ch_1_id
        )

        if self.__verbose_testing:
            misc.print_dictionary(actual_c)
            misc.print_dictionary(expected_c)

        self.assertEqual(
            actual_c, expected_c,
            'Configuration dictionaries do not match!, diff = \n'
            + str(datadiff.diff(actual_c, expected_c))
        )

    def test_sc_channel_set_configuration(self):
        """JRPC test: configuration.sc.channel.setConfiguration
        """
        try:
            jrpc_sc_channels_if.sc_channel_set_configuration(
                'FAKE-SC', 'FAKE-SC-CHANNEL', None
            )
            self.fail('An exception should have been thrown!')
        except Exception:
            pass
        try:
            jrpc_sc_channels_if.sc_channel_set_configuration(
                self.__sc_1_id, 'FAKE-SC-CHANNEL', None
            )
            self.fail('An exception should have been thrown!')
        except Exception:
            pass
        try:
            jrpc_sc_channels_if.sc_channel_set_configuration(
                self.__sc_1_id, self.__sc_1_ch_1_id, None
            )
            self.fail('An exception should have been thrown!')
        except Exception:
            pass
        try:
            jrpc_sc_channels_if.sc_channel_set_configuration(
                self.__sc_1_id, self.__sc_1_ch_1_id, {}
            )
            self.fail('An exception should have been thrown!')
        except Exception:
            pass

        jrpc_sc_channels_if.sc_channel_get_configuration(
            self.__sc_1_id, self.__sc_1_ch_1_id
        )

        try:
            jrpc_sc_channels_if.sc_channel_set_configuration(
                self.__sc_1_id, self.__sc_1_ch_1_id, {
                    channel_serializers.CH_ID_K: self.__sc_1_ch_1_id,
                    channel_serializers.FREQUENCY_K: 438000000,
                    channel_serializers.MODULATION_K: 'XM',
                    channel_serializers.POLARIZATION_K: 'RHCP',
                    channel_serializers.BITRATE_K: 600,
                    channel_serializers.BANDWIDTH_K: 25
                }
            )
            self.fail('An exception should have been thrown!')
        except Exception:
            pass

        try:
            jrpc_sc_channels_if.sc_channel_set_configuration(
                self.__sc_1_id, self.__sc_1_ch_1_id, {
                    channel_serializers.CH_ID_K: self.__sc_1_ch_1_id,
                    channel_serializers.FREQUENCY_K: 438000000,
                    channel_serializers.MODULATION_K: 'FM',
                    channel_serializers.POLARIZATION_K: 'XHHMP',
                    channel_serializers.BITRATE_K: 600,
                    channel_serializers.BANDWIDTH_K: 25
                }
            )
            self.fail('An exception should have been thrown!')
        except Exception:
            pass

        expected_c = {
            channel_serializers.CH_ID_K: self.__sc_1_ch_1_id,
            channel_serializers.FREQUENCY_K: 438000000,
            channel_serializers.MODULATION_K: 'FM',
            channel_serializers.POLARIZATION_K: 'RHCP',
            channel_serializers.BITRATE_K: 600,
            channel_serializers.BANDWIDTH_K: 25
        }

        self.assertEqual(
            jrpc_sc_channels_if.sc_channel_set_configuration(
                self.__sc_1_id, self.__sc_1_ch_1_id, expected_c
            ),
            True,
            'Configuration should have been set correctly!'
        )

        actual_c = jrpc_sc_channels_if.sc_channel_get_configuration(
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
