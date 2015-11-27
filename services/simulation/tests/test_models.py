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

from services.common import helpers as db_tools
from services.configuration.models import tle as tle_models
from services.simulation.models import passes as pass_models


class TestModels(test.TestCase):
    """Test class for the pass model methods
    """

    def setUp(self):
        """Database setup for the tests.
        """
        self.__verbose_testing = False

        self.__user = db_tools.create_user_profile()
        self.__request_1 = db_tools.create_request(user_profile=self.__user)

        self.__gs_1_id = 'gs-uvigo'
        self.__gs_1 = db_tools.create_gs(
            user_profile=self.__user,
            identifier=self.__gs_1_id
        )

        self.__sc_1_id = 'xatcobeo-sc'
        self.__sc_1_tle_id = 'CANX-2'
        self.__sc_1 = db_tools.create_sc(
            user_profile=self.__user,
            identifier=self.__sc_1_id,
            tle_id=self.__sc_1_tle_id,
        )

    def test_pass_models(self):
        """UNIT test: services.simulation.create_pass_slots_sc
        Validation of the creation of the pass slots
        """

        # 1) pass slots creation
        sc_slots_1 = pass_models.PassSlots.objects.create_pass_slots_sc(
            self.__sc_1
        )
        self.assertIsNot(
            len(sc_slots_1), 0,
            'Spacecraft pass slots should have been created'
        )
        gs_slots_1 = pass_models.PassSlots.objects.create_pass_slots_gs(
            self.__gs_1
        )
        self.assertIsNot(
            len(gs_slots_1), 0,
            'Groundstation pass slots should have been created'
        )
        self.assertTrue(
            pass_models.PassSlots.objects.filter(
                spacecraft=self.__sc_1
            ).exists(),
            'Spacecraft associated pass slots should have been created'
        )
        self.assertTrue(
            pass_models.PassSlots.objects.filter(
                groundstation=self.__gs_1
            ).exists(),
            'GroundStation associated pass slots should have been created'
        )

        # 2) pass slots removal
        pass_models.PassSlots.objects.remove_pass_slots_sc(self.__sc_1)
        self.assertFalse(
            pass_models.PassSlots.objects.filter(
                spacecraft=self.__sc_1
            ).exists(),
            'Spacecraft associated pass slots should have been removed'
        )
        pass_models.PassSlots.objects.remove_pass_slots_gs(self.__gs_1)
        self.assertFalse(
            pass_models.PassSlots.objects.filter(
                groundstation=self.__gs_1
            ).exists(),
            'GroundStation associated pass slots should have been removed'
        )

    def test_firebird(self):
        """UNIT test: Firebird TLE bug
        Test carried out to find what is the problem with the Firebird TLE and
        UVIGO groundstation.
        """
        self.__tle_fb_id = 'FirebirdTEST'
        self.__tle_fb_l1 = '1 99991U          15030.59770833 -.00001217  ' \
                           '00000-0 -76033-4 0 00007'
        self.__tle_fb_l2 = '2 99991 099.0667 036.7936 0148154 343.1198 ' \
                           '145.4319 15.00731498000018'

        self.__tle_fb = tle_models.TwoLineElement.objects.create(
            'testingsource',
            self.__tle_fb_id, self.__tle_fb_l1, self.__tle_fb_l2
        )
        self.__sc_fb = db_tools.create_sc(
            user_profile=self.__user, tle_id=self.__tle_fb_id
        )

        self.__gs_uvigo_id = 'uvigo-gs'
        self.__gs_uvigo_e = 0
        self.__gs_uvigo_lat = 42.170075
        self.__gs_uvigo_lng = -8.68826

        self.__gs_uvigo = db_tools.create_gs(
            user_profile=self.__user,
            identifier=self.__gs_uvigo_id,
            latitude=self.__gs_uvigo_lat,
            longitude=self.__gs_uvigo_lng,
            contact_elevation=self.__gs_uvigo_e
        )
