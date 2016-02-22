
import datetime
import logging

import pytz
from django import test

from services.common import misc, simulation, helpers as db_tools
from services.configuration.jrpc.views import rules as jrpc_rules_if
from services.configuration.models import rules
from services.scheduling.models import availability

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


class TestMisc(test.TestCase):

    def setUp(self):

        self.__verbose_testing = False

        if not self.__verbose_testing:
            logging.getLogger('configuration').setLevel(level=logging.CRITICAL)

        self.__gs_1_id = 'gs-castrelos'
        self.__gs_1_ch_1_id = 'chan-cas-1'

        self.__band = db_tools.create_band()
        self.__user_profile = db_tools.create_user_profile()
        self.__gs = db_tools.create_gs(
            user_profile=self.__user_profile, identifier=self.__gs_1_id,
        )
        self.__gs_1_ch_1 = db_tools.gs_add_channel(
            self.__gs, self.__band, self.__gs_1_ch_1_id
        )

    def test_get_utc_timestamp(self):
        """UNIT test: services.common.misc.get_utc_timestamp
        Basic test for the generation of UTC timestamps.
        """
        if self.__verbose_testing:
            print('>>> test_get_utc_timestamp:')

        test_datetime = misc.TIMESTAMP_0 + datetime.timedelta(days=1)
        actual_stamp = misc.get_utc_timestamp(test_datetime)
        expected_stamp = datetime.timedelta(days=1).days * 24 * 3600 * 10**6

        self.assertEqual(expected_stamp, actual_stamp, 'Wrong timestamp!')

    def test_utc_database(self):
        """UNIT test: UTC database datetimes
        This test validates whether the date/time information saved in the
        database is converted to UTC or not.
        """
        if self.__verbose_testing:
            print('>>> test_utc_database:')

        local_dt = datetime.datetime.now(
            pytz.timezone('US/Pacific')
        ).replace(
            hour=0, minute=0, second=0, microsecond=0
        )
        utc_dt = datetime.datetime.now(pytz.timezone('UTC')).replace(
            hour=0, minute=0, second=0, microsecond=0
        )

        if self.__verbose_testing:
            print('>> local_dt = ' + str(local_dt))
            print('>> local_dt.iso() = ' + str(local_dt.isoformat()))
            print('>> local_dt.date() = ' + str(local_dt.date()))
            print('>> local_dt.time() = ' + str(local_dt.time()))
            print('>> local_dt.time().iso() = ' + str(
                local_dt.time().isoformat()
            ))
            print('>> local_dt.timetz() = ' + str(local_dt.timetz()))
            print('>> local_dt.tzname() = ' + str(local_dt.tzname()))
            print('>> local_dt.utcoffset() = ' + str(local_dt.utcoffset()))
            print('>> utc_dt = ' + str(utc_dt))
            print('>> utc_dt.iso() = ' + str(utc_dt.isoformat()))
            print('>> utc_dt.date() = ' + str(utc_dt.date()))
            print('>> utc_dt.time() = ' + str(utc_dt.time()))
            print('>> utc_dt.timetz() = ' + str(utc_dt.timetz()))
            print('>> utc_dt.tzname() = ' + str(utc_dt.tzname()))

        # 1) adds a single UTC rule to the database
        utc_i_date = utc_dt + datetime.timedelta(days=1)
        utc_e_date = utc_dt + datetime.timedelta(days=366)
        utc_s_time = utc_dt - datetime.timedelta(minutes=15)
        utc_e_time = utc_dt + datetime.timedelta(minutes=15)

        jrpc_rules_if.add_rule(
            self.__gs_1_id,
            db_tools.create_jrpc_daily_rule(
                date_i=utc_i_date,
                date_f=utc_e_date,
                starting_time=utc_s_time,
                ending_time=utc_e_time
            )
        )

        actual = [
            str(r) for r in rules.AvailabilityRule.objects.all()
        ]
        expected = [
            '+(D):' + utc_i_date.isoformat().split('T')[0] +
            '>>' + utc_e_date.isoformat().split('T')[0] +
            '_T_' + utc_s_time.isoformat() +
            '>>' + utc_e_time.isoformat()
        ]

        self.assertEqual(actual, expected)

        # 2) adds a single PacificTime rule to the database (should be
        # converted into a UTC one).
        local_i_date = local_dt
        local_e_date = local_dt + datetime.timedelta(days=365)
        local_s_time = local_dt.replace(
            hour=0, minute=0, second=0, microsecond=0
        ) + datetime.timedelta(hours=12)
        local_e_time = local_s_time + datetime.timedelta(minutes=30)

        jrpc_rules_if.add_rule(
            self.__gs_1_id,
            db_tools.create_jrpc_daily_rule(
                date_i=local_i_date, date_f=local_e_date,
                starting_time=local_s_time, ending_time=local_e_time
            )
        )

        if self.__verbose_testing:
            print('>>> window = ' + str(
                simulation.OrbitalSimulator.get_simulation_window()
            ))
            misc.print_list(
                rules.AvailabilityRule.objects.all(), name='RULES'
            )

        actual = [
            str(r) for r in rules.AvailabilityRule.objects.all()
        ]
        expected.append(
            '+(D):' + local_i_date.isoformat().split('T')[0] +
            '>>' + local_e_date.isoformat().split('T')[0] +
            '_T_' + local_s_time.astimezone(pytz.utc).isoformat() +
            '>>' + local_e_time.astimezone(pytz.utc).isoformat()
        )

        self.assertEqual(actual, expected)

        if self.__verbose_testing:
            misc.print_list(
                availability.AvailabilitySlot.objects.all(),
                name='Availability Slots'
            )

    def test_get_fqdn(self):
        """UNIT test: services.common.misc.get_fqdn
        This test validates the function that gets the current hostname.
        """
        if self.__verbose_testing:
            print('>>> test_get_fqdn:')

        hn, ip = misc.get_fqdn_ip()
        if self.__verbose_testing:
            print('fqdn = ' + str(hn) + ', ip = ' + str(ip))
        self.__verbose_testing = False

    def test_get_utc_window(self):
        """UNIT test: services.common.misc.get_utc_window
        """
        if self.__verbose_testing:
            print('>>> test_get_utc_window:')

        c = misc.get_next_midnight()
        d = datetime.timedelta(minutes=3)

        self.assertEquals(
            misc.get_utc_window(center=c, duration=d), (c - d, c + d)
        )
