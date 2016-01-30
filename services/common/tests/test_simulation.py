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
import math
from datetime import timedelta, datetime

from django.test import TestCase
from pytz import utc as pytz_utc

from services.common import simulation, helpers as db_tools
from services.configuration.models import tle as tle_models


class TestSimulation(TestCase):
    """
    Validation of the simulation module.
    """

    def setUp(self):

        self.__verbose_testing = False

        if not self.__verbose_testing:
            logging.getLogger('scheduling').setLevel(level=logging.CRITICAL)
            logging.getLogger('configuration').setLevel(level=logging.CRITICAL)

        self.__gs_1_id = 'uvigo'
        self.__gs_1_ch_1_id = 'qpsk-gs-1'
        self.__sc_1_id = 'xatcobe-sc'
        self.__sc_1_tle_id = 'HUMSAT-D'
        self.__sc_1_ch_1_id = 'qpsk-sc-1'
        self.__sc_1_ch_1_f = 437000000

        self.__band = db_tools.create_band()
        self.__test_user_profile = db_tools.create_user_profile()
        self.__simulator = simulation.OrbitalSimulator()

        self.__gs_1 = db_tools.create_gs(
            user_profile=self.__test_user_profile, identifier=self.__gs_1_id,
            contact_elevation=0,
        )
        self.__gs_1_ch_1 = db_tools.gs_add_channel(
            self.__gs_1, self.__band, self.__gs_1_ch_1_id
        )

        self.__sc_1 = db_tools.create_sc(
            user_profile=self.__test_user_profile,
            identifier=self.__sc_1_id,
            tle_id=self.__sc_1_tle_id
        )
        self.__sc_1_ch_1 = db_tools.sc_add_channel(
            self.__sc_1, self.__sc_1_ch_1_f, self.__sc_1_ch_1_id,
        )

    def test_calculate_pass_slot(self):
        """UNIT test: services.common.simualtion.trigger_event
        Validates the calculation of the pass slots that occur during an
        availability slot.
        """
        # ### TODO Understand inaccuracies in between PyEphem and GPredict
        # ### TODO when the minimum contact elevation angle increases,
        # ### TODO what is the influence of body.compute(observer) within the
        # ### TODO simulation loop?
        if self.__verbose_testing:
            print('>>> test_calculate_pass_slot:')

        self.__simulator.set_groundstation(self.__gs_1)
        self.__simulator.set_spacecraft(
            tle_models.TwoLineElement.objects.get(identifier=self.__sc_1_tle_id)
        )

        if self.__verbose_testing:
            print(self.__simulator.__unicode__())

        pass_slots = self.__simulator.calculate_pass_slot(
            start=pytz_utc.localize(datetime.today()),
            end=pytz_utc.localize(datetime.today()) + timedelta(days=3)
        )

        if self.__verbose_testing:
            print('# ### RESULTS:')
            for p in pass_slots:
                print('[' + str(p[0]) + ', ' + str(p[1]) + ']')

    def test_calculate_groundtrack(self):
        """UNIT test: services.common.simualtion.calculate_groundtrack
        Simple and easy test that calculates the groundtrack for a given
        satellite and that validates that calculation by asserting the number
        of expected points for that groundtrack.
        """
        if self.__verbose_testing:
            print('>>> test_calculate_groundtrack:')

        step = timedelta(minutes=1)
        interval = self.__simulator.get_simulation_window()

        groundtrack = self.__simulator.calculate_groundtrack(
            tle_models.TwoLineElement.objects.get(
                identifier=self.__sc_1_tle_id
            ),
            interval=interval, timestep=step
        )

        if self.__verbose_testing:
            for p in groundtrack:
                print(
                    '>> @' + str(p['timestamp']) + ', (' + str(
                        p['latitude']) + ',' + str(p['longitude']) + ')'
                )

        e_n_points = int(math.ceil(
            (interval[1] - interval[0]).total_seconds() / step.total_seconds()
        ))
        self.assertEqual(
            e_n_points, len(groundtrack),
            'Number of points differs! e = ' + str(
                e_n_points
            ) + ', a = ' + str(len(groundtrack))
        )

    def test_passes(self):
        """UNIT test: services.common.simualtion.passes
        """
        self.__tle_fb = tle_models.TwoLineElement.objects.create(
            'testingsource',
            db_tools.ISS_TLE_ID, db_tools.ISS_TLE[0], db_tools.ISS_TLE[1]
        )
        self.__sc_fb = db_tools.create_sc(
            user_profile=self.__test_user_profile, tle_id=db_tools.ISS_TLE_ID
        )

        self.__gs_uvigo_id = 'uvigo-gs'
        self.__gs_uvigo_e = 0
        self.__gs_uvigo_lat = 42.170075
        self.__gs_uvigo_lng = -8.68826

        self.__gs_uvigo = db_tools.create_gs(
            user_profile=self.__test_user_profile,
            identifier=self.__gs_uvigo_id,
            latitude=self.__gs_uvigo_lat,
            longitude=self.__gs_uvigo_lng,
            contact_elevation=self.__gs_uvigo_e
        )

        self.__simulator.set_spacecraft(self.__tle_fb)
        self.__simulator.set_groundstation(self.__gs_uvigo)
        window = self.__simulator.get_simulation_window()
        # noinspection PyUnusedLocal
        slots = self.__simulator.calculate_pass_slot(window[0], window[1])
