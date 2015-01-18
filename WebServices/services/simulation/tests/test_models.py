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
from services.common.testing import helpers as db_tools
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
        """Unit test case
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