"""
   Copyright 2015 Ricardo Tubio-Pardavila

   Licensed under the Apache License, Version 2.0 (the "License");
   you may not use this file except in compliance with the License.
   You may obtain a copy of the License at

       http://www.apache.org/licenses/LICENSE-2.0

   Unless required by applicable law or agreed to in writing, software
   distributed under the License is distributed on an "AS IS" BASIS,
   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
   See the License for the specific language governing permissions and
   limitations under the License.

:Author:
    Ricardo Tubio-Pardavila (rtubiopa@calpoly.edu)
"""

import logging
from datetime import timedelta as py_timedelta

from django import test as django_test
from services.common import misc as sn_misc
from services.common import helpers as sn_helpers
from services.scheduling.models import availability as availability_models


class TestAvailability(django_test.TestCase):

    def setUp(self):

        self.__verbose_testing = False

        if not self.__verbose_testing:
            logging.getLogger('configuration').setLevel(level=logging.CRITICAL)
            logging.getLogger('scheduling').setLevel(level=logging.CRITICAL)

        self.__gs_1_id = 'gs-castrelos'
        self.__gs_1_ch_1_id = 'chan-cas-1'
        self.__gs_2_id = 'gs-cuvi'

        self.__band = sn_helpers.create_band()
        self.__user_profile = sn_helpers.create_user_profile()
        self.__gs = sn_helpers.create_gs(
            user_profile=self.__user_profile, identifier=self.__gs_1_id,
        )

    def test_create_availability(self):
        """UNIT test: services.scheduling.models.availability
        This test validates the creation of an availability slot and the
        further automatic rejections for the creation of availability slots
        that match the start and end of this one.
        """

        slot_s = sn_misc.get_next_midnight()
        slot_e = slot_s + py_timedelta(days=1)

        self.assertIsNotNone(
            availability_models.AvailabilitySlot.objects.create(
                groundstation=self.__gs, start=slot_s, end=slot_e
            )
        )
        self.assertIsNone(
            availability_models.AvailabilitySlot.objects.create(
                groundstation=self.__gs, start=slot_s, end=slot_e
            )
        )

        slot_s = slot_s + py_timedelta(days=1)
        slot_e = slot_s + py_timedelta(days=1)

        self.assertIsNotNone(
            availability_models.AvailabilitySlot.objects.create(
                groundstation=self.__gs, start=slot_s, end=slot_e
            )
        )
        self.assertIsNone(
            availability_models.AvailabilitySlot.objects.create(
                groundstation=self.__gs, start=slot_s, end=slot_e
            )
        )
