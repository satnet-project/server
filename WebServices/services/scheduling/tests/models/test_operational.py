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

from django import test

import datadiff
import datetime
import logging

from services.common import testing as db_tools, misc, simulation
from services.configuration import signals
from services.configuration.jrpc import channels as jrpc_channels_if
from services.configuration.jrpc import rules as jrpc_rules_if
from services.configuration.jrpc import serialization as jrpc_keys
from services.configuration.models import rules, availability, channels
from services.scheduling.models import operational


class OperationalModels(test.TestCase):

    def setUp(self):
        """
        This method populates the database with some information to be used
        only for this test.
        """
        self.__verbose_testing = False

        if not self.__verbose_testing:
            logging.getLogger('configuration').setLevel(level=logging.CRITICAL)
            logging.getLogger('scheduling').setLevel(level=logging.CRITICAL)

        self.__sc_1_id = 'xatcobeo-sc'
        self.__sc_1_tle_id = 'XATCOBEO'
        self.__sc_1_ch_1_id = 'xatcobeo-fm'
        self.__sc_1_ch_1_cfg = {
            jrpc_keys.FREQUENCY_K: '437000000',
            jrpc_keys.MODULATION_K: 'FM',
            jrpc_keys.POLARIZATION_K: 'LHCP',
            jrpc_keys.BITRATE_K: '300',
            jrpc_keys.BANDWIDTH_K: '12.500000000'
        }
        self.__gs_1_id = 'gs-la'
        self.__gs_1_ch_1_id = 'gs-la-fm'
        self.__gs_1_ch_1_cfg = {
            jrpc_keys.BAND_K:
            'UHF / U / 435000000.000000 / 438000000.000000',
            jrpc_keys.MODULATIONS_K: ['FM'],
            jrpc_keys.POLARIZATIONS_K: ['LHCP'],
            jrpc_keys.BITRATES_K: [300, 600, 900],
            jrpc_keys.BANDWIDTHS_K: [12.500000000, 25.000000000]
        }
        self.__gs_1_ch_2_id = 'gs-la-fm-2'
        self.__gs_1_ch_2_cfg = {
            jrpc_keys.BAND_K:
            'UHF / U / 435000000.000000 / 438000000.000000',
            jrpc_keys.MODULATIONS_K: ['FM'],
            jrpc_keys.POLARIZATIONS_K: ['LHCP'],
            jrpc_keys.BITRATES_K: [300, 600, 900],
            jrpc_keys.BANDWIDTHS_K: [12.500000000, 25.000000000]
        }

        signals.connect_availability_2_operational()
        signals.connect_channels_2_compatibility()
        signals.connect_compatibility_2_operational()
        signals.connect_rules_2_availability()
        signals.connect_segments_2_booking_tle()

        db_tools.init_available()
        db_tools.init_tles_database()
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
        operational.OperationalSlot.objects.get_simulator().set_debug()

    def test_1_compatibility_sc_channel_added_deleted(self):
        """
        Validates the update of the OperationalSlots table. In this first
        test, the adding sequence is:

        1) +GS_CH
        2) +RULE
        3) +SC_CH
        4) -SC_CH
        5) -RULE
        6) -GS_CH

        OperationalSlots should be available only in bewteen steps 3 and 4.
        """
        if self.__verbose_testing:
            print '##### test_add_slots: no rules'

        self.assertEquals(
            jrpc_channels_if.gs_channel_create(
                ground_station_id=self.__gs_1_id,
                channel_id=self.__gs_1_ch_1_id,
                configuration=self.__gs_1_ch_1_cfg
            ), True, 'Channel should have been created!'
        )

        r_1_id = jrpc_rules_if.add_rule(
            self.__gs_1_id, self.__gs_1_ch_1_id,
            db_tools.create_jrpc_daily_rule(
                starting_time=misc.localize_time_utc(datetime.time(
                    hour=8, minute=0, second=0
                )),
                ending_time=misc.localize_time_utc(datetime.time(
                    hour=23, minute=55, second=0
                ))
            )
        )
        self.assertIsNot(r_1_id, 0, 'Rule should have been added!')

        self.assertEquals(
            jrpc_channels_if.sc_channel_create(
                spacecraft_id=self.__sc_1_id,
                channel_id=self.__sc_1_ch_1_id,
                configuration=self.__sc_1_ch_1_cfg
            ), True, 'Channel should have been created!'
        )

        a_slots = availability.AvailabilitySlot.objects.get_applicable(
            groundstation_channel=channels.GroundStationChannel.objects.get(
                identifier=self.__gs_1_ch_1_id
            )
        )
        actual = len(operational.OperationalSlot.objects.all())
        expected = len(a_slots)

        if self.__verbose_testing:
            misc.print_list(a_slots, 'AvailabilitySlots')
            misc.print_list(
                operational.OperationalSlot.objects.all(), 'OperationalSlots'
            )

        self.assertEquals(
            actual, expected,
            'Simulated operational slots differ from expected!'
            'actual = ' + str(actual) + ', expected = ' + str(expected)
        )

        self.assertEquals(
            jrpc_channels_if.sc_channel_delete(
                spacecraft_id=self.__sc_1_id,
                channel_id=self.__sc_1_ch_1_id
            ),
            True,
            'Could not delete SpacecraftChannel = ' + str(self.__sc_1_ch_1_id)
        )

        expected = [
            (unicode(operational.STATE_REMOVED),),
            (unicode(operational.STATE_REMOVED),),
        ]
        actual = list(
            operational.OperationalSlot.objects.filter(
                state=operational.STATE_REMOVED
            ).values_list('state')
        )

        if self.__verbose_testing:
            print '>>> window = ' + str(
                simulation.OrbitalSimulator.get_simulation_window()
            )
            misc.print_list(rules.AvailabilityRule.objects.all())
            misc.print_list(availability.AvailabilitySlot.objects.all())
            misc.print_list(operational.OperationalSlot.objects.all())
            misc.print_list(actual)
            misc.print_list(expected)

        self.assertEquals(
            actual, expected,
            'All remaining slots must have the state ' + str(
                operational.STATE_REMOVED
            ) + ', diff = ' + str(datadiff.diff(actual, expected))
        )

        self.assertEquals(
            jrpc_rules_if.remove_rule(
                self.__gs_1_id, self.__gs_1_ch_1_id, r_1_id
            ),
            True,
            'Rule should have been removed!'
        )
        expected = [
            (unicode(operational.STATE_REMOVED),),
            (unicode(operational.STATE_REMOVED),),
        ]
        actual = list(
            operational.OperationalSlot.objects.filter(
                state=operational.STATE_REMOVED
            ).values_list('state')
        )
        self.assertEquals(
            actual, expected,
            'All remaining slots must have the state ' + str(
                operational.STATE_REMOVED
            ) + ', diff = ' + str(datadiff.diff(actual, expected))
        )

        self.assertEquals(
            jrpc_channels_if.gs_channel_delete(
                groundstation_id=self.__gs_1_id, channel_id=self.__gs_1_ch_1_id
            ),
            True,
            'Could not delete GroundStationChannel = ' + str(
                self.__gs_1_ch_1_id
            )
        )
        expected = [
            (unicode(operational.STATE_REMOVED),),
            (unicode(operational.STATE_REMOVED),),
        ]
        actual = list(
            operational.OperationalSlot.objects.filter(
                state=operational.STATE_REMOVED
            ).values_list('state')
        )
        self.assertEquals(
            actual, expected,
            'All remaining slots must have the state ' + str(
                operational.STATE_REMOVED
            ) + ', diff = ' + str(datadiff.diff(actual, expected))
        )

    def compatibility_gs_channel_added_deleted(self):
        """
        Validates the update of the OperationalSlots table. In this first
        test, the adding sequence is:

        1) +SC_CH
        2) +GS_CH
        3) +RULE
        4) -RULE
        5) +RULE
        6) -GS_CH
        7) -SC_CH

        OperationalSlots should be available only in bewteen steps 3 and 4,
        and in between steps 5 and 6.
        """
        if self.__verbose_testing:
            print '##### test_add_slots: no rules'

        self.assertEquals(
            jrpc_channels_if.sc_channel_create(
                spacecraft_id=self.__sc_1_id,
                channel_id=self.__sc_1_ch_1_id,
                configuration=self.__sc_1_ch_1_cfg
            ), True, 'Channel should have been created!'
        )
        self.assertEquals(
            jrpc_channels_if.gs_channel_create(
                ground_station_id=self.__gs_1_id,
                channel_id=self.__gs_1_ch_1_id,
                configuration=self.__gs_1_ch_1_cfg
            ), True, 'Channel should have been created!'
        )
        r_1_id = jrpc_rules_if.add_rule(
            self.__gs_1_id, self.__gs_1_ch_1_id,
            db_tools.create_jrpc_daily_rule(
                date_i=misc.get_today_utc(),
                date_f=misc.get_today_utc() + datetime.timedelta(days=365),
                starting_time=misc.localize_time_utc(datetime.time(
                    hour=8, minute=0, second=0
                )),
                ending_time=misc.localize_time_utc(datetime.time(
                    hour=23, minute=55, second=0
                ))
            )
        )
        self.assertIsNot(r_1_id, 0, 'Rule should have been added!')
        expected = [
            (unicode(operational.STATE_FREE),),
            (unicode(operational.STATE_FREE),)
        ]
        actual = list(
            operational.OperationalSlot.objects.filter(
                state=operational.STATE_FREE
            ).values_list('state')
        )
        self.assertEquals(
            actual, expected,
            'All remaining slots must have the state ' + str(
                operational.STATE_FREE
            ) + ', diff = ' + str(datadiff.diff(actual, expected))
        )

        self.assertEquals(
            jrpc_rules_if.remove_rule(
                self.__gs_1_id, self.__gs_1_ch_1_id, r_1_id
            ),
            True,
            'Rule should have been removed!'
        )
        expected = [
            (unicode(operational.STATE_REMOVED),),
            (unicode(operational.STATE_REMOVED),)
        ]
        actual = list(
            operational.OperationalSlot.objects.filter(
                state=operational.STATE_REMOVED
            ).values_list('state')
        )
        self.assertEquals(
            actual, expected,
            'All remaining slots must have the state ' + str(
                operational.STATE_REMOVED
            ) + ', diff = ' + str(datadiff.diff(actual, expected))
        )

        r_1_id = jrpc_rules_if.add_rule(
            self.__gs_1_id, self.__gs_1_ch_1_id,
            db_tools.create_jrpc_daily_rule(
                date_i=misc.get_today_utc(),
                date_f=misc.get_today_utc() + datetime.timedelta(days=365),
                starting_time=misc.localize_time_utc(datetime.time(
                    hour=8, minute=0, second=0
                )),
                ending_time=misc.localize_time_utc(datetime.time(
                    hour=23, minute=55, second=0
                ))
            )
        )
        self.assertIsNot(r_1_id, 0, 'Rule should have been added!')
        expected = [
            (unicode(operational.STATE_REMOVED),),
            (unicode(operational.STATE_REMOVED),),
            (unicode(operational.STATE_FREE),),
            (unicode(operational.STATE_FREE),)
        ]
        actual = list(
            operational.OperationalSlot.objects.all().values_list('state')
        )
        self.assertEquals(
            actual, expected,
            'Wrong slots..., diff = ' + str(datadiff.diff(actual, expected))
        )

        self.assertEquals(
            jrpc_channels_if.gs_channel_delete(
                groundstation_id=self.__gs_1_id, channel_id=self.__gs_1_ch_1_id
            ),
            True,
            'Could not delete GroundStationChannel = ' + str(
                self.__gs_1_ch_1_id
            )
        )
        expected = [
            (unicode(operational.STATE_REMOVED),),
            (unicode(operational.STATE_REMOVED),),
            (unicode(operational.STATE_REMOVED),),
            (unicode(operational.STATE_REMOVED),),
        ]
        actual = list(
            operational.OperationalSlot.objects.filter(
                state=operational.STATE_REMOVED
            ).values_list('state')
        )
        self.assertEquals(
            actual, expected,
            'All remaining slots must have the state ' + str(
                operational.STATE_REMOVED
            ) + ', diff = ' + str(datadiff.diff(actual, expected))
        )

    def compatibility_complex_1(self):
        """
        Validates the update of the OperationalSlots table. In this first
        test, the adding sequence is:

        1) +SC_CH_A
        2) +GS_CH_1 (SC_CH_A compatible)
        3) +RULE
        4) -RULE
        5) +GS_CH_2 (SC_CH_A compatible)
        5) +RULE
        6) -GS_CH
        7) -SC_CH

        OperationalSlots should be available only in bewteen steps 3 and 4,
        and in between steps 5 and 6.
        """
        if self.__verbose_testing:
            print '##### test_add_slots: no rules'

        self.assertEquals(
            jrpc_channels_if.sc_channel_create(
                spacecraft_id=self.__sc_1_id,
                channel_id=self.__sc_1_ch_1_id,
                configuration=self.__sc_1_ch_1_cfg
            ), True, 'Channel should have been created!'
        )
        self.assertEquals(
            jrpc_channels_if.gs_channel_create(
                ground_station_id=self.__gs_1_id,
                channel_id=self.__gs_1_ch_1_id,
                configuration=self.__gs_1_ch_1_cfg
            ), True, 'Channel should have been created!'
        )
        r_1_id = jrpc_rules_if.add_rule(
            self.__gs_1_id, self.__gs_1_ch_1_id,
            db_tools.create_jrpc_daily_rule(
                date_i=misc.get_today_utc(),
                date_f=misc.get_today_utc() + datetime.timedelta(days=365),
                starting_time=misc.localize_time_utc(datetime.time(
                    hour=8, minute=0, second=0
                )),
                ending_time=misc.localize_time_utc(datetime.time(
                    hour=23, minute=55, second=0
                ))
            )
        )
        self.assertIsNot(r_1_id, 0, 'Rule should have been added!')
        expected = [
            (unicode(operational.STATE_FREE),),
            (unicode(operational.STATE_FREE),)
        ]
        actual = list(
            operational.OperationalSlot.objects.filter(
                state=operational.STATE_FREE
            ).values_list('state')
        )
        self.assertEquals(
            actual, expected,
            'All remaining slots must have the state ' + str(
                operational.STATE_FREE
            ) + ', diff = ' + str(datadiff.diff(actual, expected))
        )

        self.assertEquals(
            jrpc_rules_if.remove_rule(
                self.__gs_1_id, self.__gs_1_ch_1_id, r_1_id
            ),
            True,
            'Rule should have been removed!'
        )
        expected = [
            (unicode(operational.STATE_REMOVED),),
            (unicode(operational.STATE_REMOVED),)
        ]
        actual = list(
            operational.OperationalSlot.objects.filter(
                state=operational.STATE_REMOVED
            ).values_list('state')
        )
        self.assertEquals(
            actual, expected,
            'All remaining slots must have the state ' + str(
                operational.STATE_REMOVED
            ) + ', diff = ' + str(datadiff.diff(actual, expected))
        )

        self.assertEquals(
            jrpc_channels_if.gs_channel_create(
                ground_station_id=self.__gs_1_id,
                channel_id=self.__gs_1_ch_2_id,
                configuration=self.__gs_1_ch_2_cfg
            ), True, 'Channel should have been created!'
        )
        expected = [
            (unicode(operational.STATE_REMOVED),),
            (unicode(operational.STATE_REMOVED),)
        ]
        actual = list(
            operational.OperationalSlot.objects.filter(
                state=operational.STATE_REMOVED
            ).values_list('state')
        )
        self.assertEquals(
            actual, expected,
            'All remaining slots must have the state ' + str(
                operational.STATE_REMOVED
            ) + ', diff = ' + str(datadiff.diff(actual, expected))
        )

        r_1_id = jrpc_rules_if.add_rule(
            self.__gs_1_id, self.__gs_1_ch_1_id,
            db_tools.create_jrpc_daily_rule(
                date_i=misc.get_today_utc(),
                date_f=misc.get_today_utc() + datetime.timedelta(days=365),
                starting_time=misc.localize_time_utc(datetime.time(
                    hour=8, minute=0, second=0
                )),
                ending_time=misc.localize_time_utc(datetime.time(
                    hour=23, minute=55, second=0
                ))
            )
        )
        self.assertIsNot(r_1_id, 0, 'Rule should have been added!')
        expected = [
            (unicode(operational.STATE_REMOVED),),
            (unicode(operational.STATE_REMOVED),),
            (unicode(operational.STATE_FREE),),
            (unicode(operational.STATE_FREE),)
        ]
        actual = list(
            operational.OperationalSlot.objects.all().values_list('state')
        )
        self.assertEquals(
            actual, expected,
            'Wrong slots..., diff = ' + str(datadiff.diff(actual, expected))
        )

        r_2_id = jrpc_rules_if.add_rule(
            self.__gs_1_id, self.__gs_1_ch_2_id,
            db_tools.create_jrpc_daily_rule(
                date_i=misc.get_today_utc(),
                date_f=misc.get_today_utc() + datetime.timedelta(days=365),
                starting_time=misc.localize_time_utc(datetime.time(
                    hour=14, minute=0, second=0
                )),
                ending_time=misc.localize_time_utc(datetime.time(
                    hour=22, minute=55, second=0
                ))
            )
        )
        self.assertIsNot(r_2_id, 0, 'Rule should have been added!')
        expected = [
            (unicode(operational.STATE_FREE),),
            (unicode(operational.STATE_FREE),)
        ]
        actual = list(
            operational.OperationalSlot.objects.filter(
                groundstation_channel=channels.GroundStationChannel.objects
                .get(identifier=self.__gs_1_ch_2_id)
            ).values_list('state')
        )
        self.assertEquals(
            actual, expected,
            'Wrong slots..., diff = ' + str(datadiff.diff(actual, expected))
        )

        self.assertEquals(
            jrpc_channels_if.gs_channel_delete(
                groundstation_id=self.__gs_1_id, channel_id=self.__gs_1_ch_1_id
            ),
            True,
            'Could not delete GroundStationChannel = ' + str(
                self.__gs_1_ch_1_id
            )
        )
        expected = [
            (unicode(operational.STATE_REMOVED),),
            (unicode(operational.STATE_REMOVED),),
            (unicode(operational.STATE_REMOVED),),
            (unicode(operational.STATE_REMOVED),),
            (unicode(operational.STATE_REMOVED),),
            (unicode(operational.STATE_REMOVED),),
        ]
        actual = list(
            operational.OperationalSlot.objects.filter(
                state=operational.STATE_REMOVED
            ).values_list('state')
        )
        self.assertEquals(
            actual, expected,
            'All remaining slots must have the state ' + str(
                operational.STATE_REMOVED
            ) + ', diff = ' + str(datadiff.diff(actual, expected))
        )