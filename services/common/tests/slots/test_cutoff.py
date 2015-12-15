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

from datetime import timedelta as py_delta

from django import test
from services.common import misc, slots


class CutoffSlotsTest(test.TestCase):

    def setUp(self):

        self.__verbose_testing = False

    def test_cutoff_none(self):
        """UNIT test: services.common.slots.cutoff_slot (robustness)
        Nones and empties test.
        """
        self.assertRaises(ValueError, slots.cutoff, None, None)
        self.assertRaises(ValueError, slots.cutoff, None, ())
        self.assertRaises(ValueError, slots.cutoff, (), None)
        self.assertRaises(ValueError, slots.cutoff, (), ())
        self.assertRaises(
            ValueError, slots.cutoff, (
                misc.get_next_midnight() + py_delta(hours=1),
                misc.get_next_midnight()
            ), ()
        )
        self.assertRaises(
            ValueError, slots.cutoff, (), (
                misc.get_next_midnight() + py_delta(hours=1),
                misc.get_next_midnight()
            )
        )
        self.assertRaises(
            ValueError, slots.cutoff, (
                misc.get_next_midnight(),
                misc.get_next_midnight() + py_delta(hours=1)
            ), (
                misc.get_next_midnight() + py_delta(hours=1),
                misc.get_next_midnight()
            )
        )
        self.assertRaises(
            ValueError, slots.cutoff, (
                misc.get_next_midnight() + py_delta(hours=1),
                misc.get_next_midnight()
            ), (
                misc.get_next_midnight(),
                misc.get_next_midnight() + py_delta(hours=1)
            )
        )

    def test_cutoff_case_A(self):
        """UNIT test: services.common.slots.cutoff_slot (CASE A)
        CASE A: slot[1] < interval[0]
        """
        self.assertRaisesMessage(
            ValueError, '@cutoff_slot: slot[1] <= interval[0]',
            slots.cutoff, (
                misc.get_next_midnight(),
                misc.get_next_midnight() + py_delta(hours=1)
            ), (
                misc.get_next_midnight() - py_delta(hours=4),
                misc.get_next_midnight() - py_delta(hours=3),
            )
        )

    def test_cutoff_case_B(self):
        """UNIT test: services.common.slots.cutoff_slot (CASE B)
        CASE B: slot[0] < interval[0] && slot[1] < interval[1]
        """
        self.assertEquals(
            slots.cutoff((
                misc.get_next_midnight(),
                misc.get_next_midnight() + py_delta(hours=1)
            ), (
                misc.get_next_midnight() - py_delta(minutes=15),
                misc.get_next_midnight() + py_delta(minutes=15)
            )), (
                misc.get_next_midnight(),
                misc.get_next_midnight() + py_delta(minutes=15)
            )
        )
        self.assertEquals(
            slots.cutoff((
                misc.get_next_midnight(),
                misc.get_next_midnight() + py_delta(hours=1)
            ), (
                misc.get_next_midnight(),
                misc.get_next_midnight() + py_delta(minutes=15)
            )), (
                misc.get_next_midnight(),
                misc.get_next_midnight() + py_delta(minutes=15)
            )
        )
        self.assertEquals(
            slots.cutoff((
                misc.get_next_midnight(),
                misc.get_next_midnight() + py_delta(hours=1)
            ), (
                misc.get_next_midnight(),
                misc.get_next_midnight() + py_delta(hours=1)
            )), (
                misc.get_next_midnight(),
                misc.get_next_midnight() + py_delta(hours=1)
            )
        )

    def test_cutoff_case_C(self):
        """UNIT test: services.common.slots.cutoff_slot (CASE C)
        CASE C: slot[0] > interval[0] && slot[1] < interval[1]
        """
        self.assertEquals(
            slots.cutoff((
                misc.get_next_midnight(),
                misc.get_next_midnight() + py_delta(hours=1)
            ), (
                misc.get_next_midnight() + py_delta(minutes=15),
                misc.get_next_midnight() + py_delta(minutes=30)
            )), (
                misc.get_next_midnight() + py_delta(minutes=15),
                misc.get_next_midnight() + py_delta(minutes=30)
            )
        )
        self.assertEquals(
            slots.cutoff((
                misc.get_next_midnight(),
                misc.get_next_midnight() + py_delta(hours=1)
            ), (
                misc.get_next_midnight() + py_delta(minutes=15),
                misc.get_next_midnight() + py_delta(hours=1)
            )), (
                misc.get_next_midnight() + py_delta(minutes=15),
                misc.get_next_midnight() + py_delta(hours=1)
            )
        )

    def test_cutoff_case_D(self):
        """UNIT test: services.common.slots.cutoff_slot (CASE D)
        CASE D: slot[0] < interval[1] && slot[1] > interval[1]
        """
        self.assertEquals(
            slots.cutoff((
                misc.get_next_midnight(),
                misc.get_next_midnight() + py_delta(hours=1)
            ), (
                misc.get_next_midnight() + py_delta(minutes=15),
                misc.get_next_midnight() + py_delta(hours=2)
            )), (
                misc.get_next_midnight() + py_delta(minutes=15),
                misc.get_next_midnight() + py_delta(hours=1)
            )
        )

    def test_cutoff_case_E(self):
        """UNIT test: services.common.slots.cutoff_slot (CASE E)
        CASE E: slot[0] > interval[1]
        """
        self.assertRaisesMessage(
            ValueError, '@cutoff_slot: slot[0] >= interval[1]',
            slots.cutoff, (
                misc.get_next_midnight(),
                misc.get_next_midnight() + py_delta(hours=1)
            ), (
                misc.get_next_midnight() + py_delta(hours=4),
                misc.get_next_midnight() + py_delta(hours=5),
            )
        )
        self.assertRaisesMessage(
            ValueError, '@cutoff_slot: slot[0] >= interval[1]',
            slots.cutoff, (
                misc.get_next_midnight(),
                misc.get_next_midnight() + py_delta(hours=1)
            ), (
                misc.get_next_midnight() + py_delta(hours=1),
                misc.get_next_midnight() + py_delta(hours=5),
            )
        )
