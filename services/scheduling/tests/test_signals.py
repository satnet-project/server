"""
   Copyright 2016 Ricardo Tubio-Pardavila

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
import logging

from services.scheduling.models import operational as operational_models
from services.scheduling.signals import operational as operational_signals


class SchedulingSignalsTest(test.TestCase):
    """JRPC Test Case
    This class tests the services related with the Simulation objects.
    """

    def setUp(self):
        """
        This method populates the database with some information to be used
        only for this test.
        """
        self.__verbose_testing = False

        if not self.__verbose_testing:
            logging.getLogger('common').setLevel(level=logging.CRITICAL)
            logging.getLogger('configuration').setLevel(level=logging.CRITICAL)
            logging.getLogger('scheduling').setLevel(level=logging.CRITICAL)
            logging.getLogger('simulation').setLevel(level=logging.CRITICAL)

    def test_create_testing_oslot(self):
        """SGNL test: services.scheduling.signals.satnet_loaded
        This test validates the creation of the operational slot for the
        testing slot -1.
        """

        try:
            operational_models.OperationalSlot.objects.get(
                identifier=operational_models.TEST_O_SLOT_ID
            )
            self.fail('No object should be available')
        except operational_models.OperationalSlot.DoesNotExist:
            operational_signals.satnet_loaded(None)

        o_slot_test = operational_models.OperationalSlot.objects.get(
            identifier=operational_models.TEST_O_SLOT_ID
        )

        self.assertEquals(
            o_slot_test.identifier, operational_models.TEST_O_SLOT_ID
        )
