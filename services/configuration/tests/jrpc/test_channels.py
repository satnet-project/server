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

from django.db.models import ObjectDoesNotExist
from django.test import TestCase

from services.common import misc
from services.common.testing import helpers as db_tools
from services.configuration.jrpc.serializers import serialization as jrpc_serial
from services.configuration.jrpc.views import channels as jrpc_channels_if


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

        self.__sc_1_id = 'humd'
        self.__sc_1_ch_1_id = 'gmsk-sc-1'
        self.__sc_1_ch_1_f = 437000000
        self.__sc_1_ch_2_id = 'gmsk-sc-2'

        self.__band = db_tools.create_band()
        self.__test_user_profile = db_tools.create_user_profile()

        self.__gs_1 = db_tools.create_gs(
            user_profile=self.__test_user_profile, identifier=self.__gs_1_id,
        )
        self.__gs_1_ch_1 = db_tools.gs_add_channel(
            self.__gs_1, self.__band, self.__gs_1_ch_1_id
        )

        self.__sc_1 = db_tools.create_sc(
            user_profile=self.__test_user_profile,
            identifier=self.__sc_1_id
        )
        self.__sc_1_ch_1 = db_tools.sc_add_channel(
            self.__sc_1, self.__sc_1_ch_1_f, self.__sc_1_ch_1_id,
        )

        if not self.__verbose_testing:
            logging.getLogger('configuration').setLevel(level=logging.CRITICAL)
            logging.getLogger('simulation').setLevel(level=logging.CRITICAL)

    def test_get_channel_options(self):
        """
        This test validates the configuration of the options available for
        the channels of either GroundStations or Spacecraft.
        """
        if self.__verbose_testing:
            print('>>> TEST (test_get_channel_options)')

        actual_o = jrpc_channels_if.get_options()
        expected_o = {
            jrpc_serial.BAND_K: [
                'UHF / U / 435000000.000000 / 438000000.000000'
            ],
            jrpc_serial.MODULATIONS_K: ['FM', 'AFSK'],
            jrpc_serial.POLARIZATIONS_K: ['LHCP', 'RHCP'],
            jrpc_serial.BITRATES_K: ['300', '600', '900'],
            jrpc_serial.BANDWIDTHS_K: ['12.500000000', '25.000000000']
        }
        self.assertEqual(
            actual_o, expected_o,
            'Options differ! diff = ' + str(
                datadiff.diff(actual_o, expected_o)
            )
        )

    def test_gs_channel_is_unique(self):
        """
        This test validates the JRPC method that checks whether a given
        channel already exists or not.
        """
        if self.__verbose_testing:
            print('>>> TEST (test_gs_channel_is_unique)')

        self.assertEqual(
            jrpc_channels_if.gs_channel_is_unique(self.__gs_1_ch_1_id),
            True,
            'Channel should exist already!'
        )
        self.assertEqual(
            jrpc_channels_if.gs_channel_is_unique('CH-FAKE'),
            False,
            'Channel should not exist yet!'
        )

    def test_sc_channel_is_unique(self):
        """
        This test validates the JRPC method that checks whether a given
        channel already exists or not.
        """
        if self.__verbose_testing:
            print('>>> TEST (test_sc_channel_is_unique)')

        self.assertEqual(
            jrpc_channels_if.sc_channel_is_unique(self.__sc_1_ch_1_id),
            True,
            'Channel should exist already!'
        )
        self.assertEqual(
            jrpc_channels_if.sc_channel_is_unique('CH-FAKE'),
            False,
            'Channel should not exist yet!'
        )

    def test_gs_channel_create(self):
        """
        This test validates the JRPC method that creates a new channel.
        """
        if self.__verbose_testing:
            print('>>> TEST (test_gs_channel_create)')

        try:
            jrpc_channels_if.gs_channel_create(
                ground_station_id='FAKE-GS',
                channel_id=self.__gs_1_ch_2_id,
                configuration={
                    jrpc_serial.BAND_K:
                        'UHF / U / 435000000.000000 / 438000000.000000',
                    jrpc_serial.AUTOMATED_K: False,
                    jrpc_serial.MODULATIONS_K: ['FM'],
                    jrpc_serial.POLARIZATIONS_K: ['LHCP'],
                    jrpc_serial.BITRATES_K: [300, 600, 900],
                    jrpc_serial.BANDWIDTHS_K: [12.500000000]
                }
            )
            self.fail('An exception should have been thrown!')
        except ObjectDoesNotExist:
            pass

        self.assertEqual(
            jrpc_channels_if.gs_channel_create(
                ground_station_id=self.__gs_1_id,
                channel_id=self.__gs_1_ch_2_id,
                configuration={
                    jrpc_serial.BAND_K:
                        'UHF / U / 435000000.000000 / 438000000.000000',
                    jrpc_serial.AUTOMATED_K: False,
                    jrpc_serial.MODULATIONS_K: ['FM'],
                    jrpc_serial.POLARIZATIONS_K: ['LHCP'],
                    jrpc_serial.BITRATES_K: [300, 600, 900],
                    jrpc_serial.BANDWIDTHS_K: [12.500000000]
                }
            ),
            True,
            'Channel should have been created!'
        )
        db_tools.remove_gs_channel(self.__gs_1_id, self.__gs_1_ch_2_id)

    def test_sc_channel_create(self):
        """
        This test validates the JRPC method that creates a new channel.
        """
        if self.__verbose_testing:
            print('>>> TEST (test_sc_channel_create)')

        try:
            jrpc_channels_if.sc_channel_create(
                spacecraft_id='FAKE-SC',
                channel_id=self.__sc_1_ch_2_id,
                configuration={
                    jrpc_serial.FREQUENCY_K: '437000000',
                    jrpc_serial.MODULATION_K: 'FM',
                    jrpc_serial.POLARIZATION_K: 'LHCP',
                    jrpc_serial.BITRATE_K: '300',
                    jrpc_serial.BANDWIDTH_K: '12.500000000'
                }
            )
            self.fail('An exception should have been thrown!')
        except ObjectDoesNotExist:
            pass

        self.assertEqual(
            jrpc_channels_if.sc_channel_create(
                spacecraft_id=self.__sc_1_id,
                channel_id=self.__sc_1_ch_2_id,
                configuration={
                    jrpc_serial.FREQUENCY_K: '437000000',
                    jrpc_serial.MODULATION_K: 'FM',
                    jrpc_serial.POLARIZATION_K: 'LHCP',
                    jrpc_serial.BITRATE_K: '300',
                    jrpc_serial.BANDWIDTH_K: '12.500000000'
                }
            ),
            True,
            'Channel should have been created!'
        )
        db_tools.remove_sc_channel(self.__sc_1_ch_2_id)

    def test_gs_channel_delete(self):
        """
        This tests validates the JRPC method that deletes an existing channel.
        """
        try:
            jrpc_channels_if.gs_channel_delete(
                'FAKE-GS', 'FAKE-GS-CHANNEL'
            )
            self.fail('An exception should have been thrown!')
        except ObjectDoesNotExist:
            pass

        try:
            jrpc_channels_if.gs_channel_delete(
                self.__gs_1_id, 'FAKE-GS-CHANNEL'
            )
            self.fail('An exception should have been thrown!')
        except ObjectDoesNotExist:
            pass

        self.assertEqual(
            jrpc_channels_if.gs_channel_create(
                ground_station_id=self.__gs_1_id,
                channel_id=self.__gs_1_ch_2_id,
                configuration={
                    jrpc_serial.BAND_K:
                        'UHF / U / 435000000.000000 / 438000000.000000',
                    jrpc_serial.AUTOMATED_K: False,
                    jrpc_serial.MODULATIONS_K: ['FM'],
                    jrpc_serial.POLARIZATIONS_K: ['LHCP'],
                    jrpc_serial.BITRATES_K: [300, 600, 900],
                    jrpc_serial.BANDWIDTHS_K: [12.500000000]
                }
            ),
            True,
            'Channel should have been created!'
        )
        self.assertEqual(
            jrpc_channels_if.gs_channel_delete(
                self.__gs_1_id, self.__gs_1_ch_2_id
            ),
            True,
            'Channel should have been removed!'
        )
        self.assertEqual(
            jrpc_channels_if.gs_channel_is_unique(self.__gs_1_ch_2_id),
            False,
            'Channel should not exist yet!'
        )

    def test_sc_channel_delete(self):
        """
        This tests validates the JRPC method that deletes an existing channel.
        """
        try:
            jrpc_channels_if.sc_channel_delete(
                'FAKE-SC', 'FAKE-SC-CHANNEL'
            )
            self.fail('An exception should have been thrown!')
        except ObjectDoesNotExist:
            pass

        try:
            jrpc_channels_if.sc_channel_delete(
                self.__sc_1_id, 'FAKE-SC-CHANNEL'
            )
            self.fail('An exception should have been thrown!')
        except ObjectDoesNotExist:
            pass

        self.assertEqual(
            jrpc_channels_if.sc_channel_create(
                spacecraft_id=self.__sc_1_id,
                channel_id=self.__sc_1_ch_2_id,
                configuration={
                    jrpc_serial.FREQUENCY_K: '437000000',
                    jrpc_serial.MODULATION_K: 'FM',
                    jrpc_serial.POLARIZATION_K: 'LHCP',
                    jrpc_serial.BITRATE_K: '300',
                    jrpc_serial.BANDWIDTH_K: '12.500000000'
                }
            ),
            True,
            'Channel should have been created!'
        )
        self.assertEqual(
            jrpc_channels_if.sc_channel_delete(
                self.__sc_1_id, self.__sc_1_ch_2_id
            ),
            True,
            'Channel should have been removed!'
        )
        self.assertEqual(
            jrpc_channels_if.sc_channel_is_unique(self.__sc_1_ch_2_id),
            False,
            'Channel should not exist yet!'
        )

    def test_gs_channel_get_configuration(self):
        """
        Tests the JRPC method for getting the configuration from a channel.
        """
        try:
            jrpc_channels_if.gs_channel_get_configuration(
                'FAKE-GS', 'FAKE-GS-CHANNEL'
            )
            self.fail('An exception should have been thrown!')
        except ObjectDoesNotExist:
            pass
        try:
            jrpc_channels_if.gs_channel_get_configuration(
                self.__gs_1_id, 'FAKE-GS-CHANNEL'
            )
            self.fail('An exception should have been thrown!')
        except ObjectDoesNotExist:
            pass

        expected_c = {
            jrpc_serial.CH_ID_K: self.__gs_1_ch_2_id,
            jrpc_serial.BAND_K: 'UHF / U / 435000000.000000 / 438000000.000000',
            jrpc_serial.AUTOMATED_K: False,
            jrpc_serial.MODULATIONS_K: ['FM'],
            jrpc_serial.POLARIZATIONS_K: ['LHCP'],
            jrpc_serial.BITRATES_K: [300, 600, 900],
            jrpc_serial.BANDWIDTHS_K: [12.500000000]
        }
        self.assertEqual(
            jrpc_channels_if.gs_channel_create(
                ground_station_id=self.__gs_1_id,
                channel_id=self.__gs_1_ch_2_id,
                configuration=expected_c
            ), True, 'Channel should have been created!'
        )

        actual_c = jrpc_channels_if.gs_channel_get_configuration(
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
        """
        Tests the JRPC method for getting the configuration from a channel.
        """
        try:
            jrpc_channels_if.sc_channel_get_configuration(
                'FAKE-SC', 'FAKE-SC-CHANNEL'
            )
            self.fail('An exception should have been thrown!')
        except ObjectDoesNotExist:
            pass
        try:
            jrpc_channels_if.sc_channel_get_configuration(
                self.__sc_1_id, 'FAKE-SC-CHANNEL'
            )
            self.fail('An exception should have been thrown!')
        except ObjectDoesNotExist:
            pass

        expected_c = {
            jrpc_serial.CH_ID_K: self.__sc_1_ch_2_id,
            jrpc_serial.FREQUENCY_K: 437000000,
            jrpc_serial.MODULATION_K: 'FM',
            jrpc_serial.POLARIZATION_K: 'LHCP',
            jrpc_serial.BITRATE_K: 300,
            jrpc_serial.BANDWIDTH_K: 12.500000000
        }

        self.assertEqual(
            jrpc_channels_if.sc_channel_create(
                spacecraft_id=self.__sc_1_id,
                channel_id=self.__sc_1_ch_2_id,
                configuration=expected_c
            ), True, 'Channel should have been created!'
        )

        actual_c = jrpc_channels_if.sc_channel_get_configuration(
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
        """
        Test that validates the change of a configuration for a given channel
        by using the correspondent JRPC method.
        """
        self.__verbose_testing = False
        try:
            jrpc_channels_if.gs_channel_set_configuration(
                'FAKE-GS', 'FAKE-GS-CHANNEL', None
            )
            self.fail('An exception should have been thrown!')
        except ObjectDoesNotExist:
            pass
        try:
            jrpc_channels_if.gs_channel_set_configuration(
                self.__gs_1_id, 'FAKE-GS-CHANNEL', None
            )
            self.fail('An exception should have been thrown!')
        except ObjectDoesNotExist:
            pass
        try:
            jrpc_channels_if.gs_channel_set_configuration(
                self.__gs_1_id, self.__gs_1_ch_1_id, None
            )
            self.fail('An exception should have been thrown!')
        except Exception:
            pass
        try:
            jrpc_channels_if.gs_channel_set_configuration(
                self.__gs_1_id, self.__gs_1_ch_1_id, {}
            )
            self.fail('An exception should have been thrown!')
        except Exception:
            pass

        jrpc_channels_if.gs_channel_get_configuration(
            self.__gs_1_id, self.__gs_1_ch_1_id
        )

        try:
            jrpc_channels_if.gs_channel_set_configuration(
                self.__gs_1_id, self.__gs_1_ch_1_id, {
                    jrpc_serial.BAND_K:
                        'UHF / U / 435000000.000000 / 438000000.000000',
                    jrpc_serial.AUTOMATED_K: False,
                    jrpc_serial.MODULATIONS_K: ['HM'],
                    jrpc_serial.POLARIZATIONS_K: ['LHCP'],
                    jrpc_serial.BITRATES_K: [600],
                    jrpc_serial.BANDWIDTHS_K: [25]
                }
            )
            self.fail('An exception should have been thrown!')
        except Exception:
            pass

        try:
            jrpc_channels_if.gs_channel_set_configuration(
                self.__gs_1_id, self.__gs_1_ch_1_id, {
                    jrpc_serial.BAND_K:
                    'UHF / U / 435000000.000000 / 438000000.000000',
                    jrpc_serial.AUTOMATED_K: False,
                    jrpc_serial.MODULATIONS_K: ['FM'],
                    jrpc_serial.POLARIZATIONS_K: ['XHHMP'],
                    jrpc_serial.BITRATES_K: [600],
                    jrpc_serial.BANDWIDTHS_K: [25]
                }
            )
            self.fail('An exception should have been thrown!')
        except Exception:
            pass

        expected_c = {
            jrpc_serial.CH_ID_K: self.__gs_1_ch_1_id,
            jrpc_serial.BAND_K: 'UHF / U / 435000000.000000 / 438000000.000000',
            jrpc_serial.AUTOMATED_K: False,
            jrpc_serial.MODULATIONS_K: [str('AFSK'), str('FM')],
            jrpc_serial.POLARIZATIONS_K: [str('LHCP'), str('RHCP')],
            jrpc_serial.BITRATES_K: [300, 600],
            jrpc_serial.BANDWIDTHS_K: [25]
        }

        self.assertEqual(
            jrpc_channels_if.gs_channel_set_configuration(
                self.__gs_1_id, self.__gs_1_ch_1_id, expected_c
            ),
            True,
            'Configuration should have been set correctly!'
        )

        actual_c = jrpc_channels_if.gs_channel_get_configuration(
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
        """
        Test that validates the change of a configuration for a given channel
        by using the correspondent JRPC method.
        """
        try:
            jrpc_channels_if.sc_channel_set_configuration(
                'FAKE-SC', 'FAKE-SC-CHANNEL', None
            )
            self.fail('An exception should have been thrown!')
        except ObjectDoesNotExist:
            pass
        try:
            jrpc_channels_if.sc_channel_set_configuration(
                self.__sc_1_id, 'FAKE-SC-CHANNEL', None
            )
            self.fail('An exception should have been thrown!')
        except ObjectDoesNotExist:
            pass
        try:
            jrpc_channels_if.sc_channel_set_configuration(
                self.__sc_1_id, self.__sc_1_ch_1_id, None
            )
            self.fail('An exception should have been thrown!')
        except Exception:
            pass
        try:
            jrpc_channels_if.sc_channel_set_configuration(
                self.__sc_1_id, self.__sc_1_ch_1_id, {}
            )
            self.fail('An exception should have been thrown!')
        except Exception:
            pass

        jrpc_channels_if.sc_channel_get_configuration(
            self.__sc_1_id, self.__sc_1_ch_1_id
        )

        try:
            jrpc_channels_if.sc_channel_set_configuration(
                self.__sc_1_id, self.__sc_1_ch_1_id, {
                    jrpc_serial.CH_ID_K: self.__sc_1_ch_1_id,
                    jrpc_serial.FREQUENCY_K: 438000000,
                    jrpc_serial.MODULATION_K: 'XM',
                    jrpc_serial.POLARIZATION_K: 'RHCP',
                    jrpc_serial.BITRATE_K: 600,
                    jrpc_serial.BANDWIDTH_K: 25
                }
            )
            self.fail('An exception should have been thrown!')
        except Exception:
            pass

        try:
            jrpc_channels_if.sc_channel_set_configuration(
                self.__sc_1_id, self.__sc_1_ch_1_id, {
                    jrpc_serial.CH_ID_K: self.__sc_1_ch_1_id,
                    jrpc_serial.FREQUENCY_K: 438000000,
                    jrpc_serial.MODULATION_K: 'FM',
                    jrpc_serial.POLARIZATION_K: 'XHHMP',
                    jrpc_serial.BITRATE_K: 600,
                    jrpc_serial.BANDWIDTH_K: 25
                }
            )
            self.fail('An exception should have been thrown!')
        except Exception:
            pass

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