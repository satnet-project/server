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
from django import test
from services.common.testing import helpers as db_tools
from services.configuration.jrpc.serializers\
    import serialization as jrpc_cfg_serial
from services.scheduling.models import operational


class JRPCAutomatedBookingTest(test.TestCase):
    """JRPC Automated Booking test.
    The tests included in this class validate the booking process that involves
    the usage of fully automated GroundStation channels.
    """

    def setUp(self):
        """Test setup.
        This method populates the database with some information to be used
        only for this test.
        """
        self.__verbose_testing = False

        if not self.__verbose_testing:
            logging.getLogger('common').setLevel(level=logging.CRITICAL)
            logging.getLogger('configuration').setLevel(level=logging.CRITICAL)
            logging.getLogger('scheduling').setLevel(level=logging.CRITICAL)

        operational.OperationalSlot.objects.get_simulator().set_debug()
        operational.OperationalSlot.objects.set_debug()

        self.__sc_1_id = 'xatcobeo-sc'
        self.__sc_1_tle_id = 'HUMSAT-D'
        self.__sc_1_ch_1_id = 'xatcobeo-fm'
        self.__sc_1_ch_1_cfg = {
            jrpc_cfg_serial.FREQUENCY_K: '437000000',
            jrpc_cfg_serial.MODULATION_K: 'FM',
            jrpc_cfg_serial.POLARIZATION_K: 'LHCP',
            jrpc_cfg_serial.BITRATE_K: '300',
            jrpc_cfg_serial.BANDWIDTH_K: '12.500000000'
        }
        self.__gs_1_id = 'gs-la'
        self.__gs_1_ch_1_id = 'gs-la-fm'
        self.__gs_1_ch_1_cfg = {
            jrpc_cfg_serial.BAND_K:
            'UHF / U / 435000000.000000 / 438000000.000000',
            jrpc_cfg_serial.AUTOMATED_K: True,
            jrpc_cfg_serial.MODULATIONS_K: ['FM'],
            jrpc_cfg_serial.POLARIZATIONS_K: ['LHCP'],
            jrpc_cfg_serial.BITRATES_K: [300, 600, 900],
            jrpc_cfg_serial.BANDWIDTHS_K: [12.500000000, 25.000000000]
        }

        db_tools.init_available()
        self.__band = db_tools.create_band()
        self.__user_profile = db_tools.create_user_profile()
        self.__sc_1 = db_tools.create_sc(
            user_profile=self.__user_profile,
            identifier=self.__sc_1_id,
            tle_id=self.__sc_1_tle_id,
        )
        self.__gs_1 = db_tools.create_gs(
            user_profile=self.__user_profile, identifier=self.__gs_1_id,
        )

    def test_book_automated(self):
        """Basic automated booking test.
        Basic JUNIT test that validates the automatic acceptance of the booking
        requests made by an external operator over the available operational
        slots offered by a given GroundStation.
        """
        pass