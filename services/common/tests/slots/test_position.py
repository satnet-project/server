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


class PositionSlotTest(test.TestCase):

    def setUp(self):

        self.__verbose_testing = False

    def test_position_none(self):
        """UNIT test: services.common.slots.position (robustness)
        Nones and empties test.
        """
        self.assertRaises(ValueError, slots.position, None, None)
        self.assertRaises(ValueError, slots.position, None, ())
        self.assertRaises(ValueError, slots.position, (), None)
        self.assertRaises(ValueError, slots.position, (), ())
        self.assertRaises(
            ValueError, slots.position, (
                misc.get_next_midnight() + py_delta(hours=1),
                misc.get_next_midnight()
            ), ()
        )
        self.assertRaises(
            ValueError, slots.position, (), (
                misc.get_next_midnight() + py_delta(hours=1),
                misc.get_next_midnight()
            )
        )
        self.assertRaises(
            ValueError, slots.position, (
                misc.get_next_midnight(),
                misc.get_next_midnight() + py_delta(hours=1)
            ), (
                misc.get_next_midnight() + py_delta(hours=1),
                misc.get_next_midnight()
            )
        )
        self.assertRaises(
            ValueError, slots.position, (
                misc.get_next_midnight() + py_delta(hours=1),
                misc.get_next_midnight()
            ), (
                misc.get_next_midnight(),
                misc.get_next_midnight() + py_delta(hours=1)
            )
        )

    def test_position_case_A(self):
        """UNIT test: services.common.slots.position (CASE A)
        CASE A: slot[1] < interval[0]
        """

        i0 = misc.get_next_midnight() + py_delta(days=300, hours=12)
        interval = (i0, i0 + py_delta(days=2))

        slot = (
            misc.get_next_midnight(),
            misc.get_next_midnight() + py_delta(hours=2)
        )
        result = slots.position(interval, slot)
        expected = (
            slot[0] + py_delta(days=301), slot[1] + py_delta(days=301)
        )

        self.assertEquals(result, expected)

    def test_position_case_B(self):
        """UNIT test: services.common.slots.position (CASE B)
        CASE B: slot[0] < interval[0], slot[1] > interval[0]
        """

        i0 = misc.get_next_midnight() + py_delta(days=300, hours=12)
        interval = (i0, i0 + py_delta(days=2))

        slot = (
            misc.get_next_midnight() + py_delta(hours=11),
            misc.get_next_midnight() + py_delta(hours=13)
        )
        result = slots.position(interval, slot)
        expected = (
            slot[0] + py_delta(days=300), slot[1] + py_delta(days=300)
        )

        self.assertEquals(result, expected)

    def test_position_case_C(self):
        """UNIT test: services.common.slots.position (CASE C)
        CASE C: slot[0] > interval[0], slot[1] < interval[1]
        """

        i0 = misc.get_next_midnight() + py_delta(days=300, hours=12)
        interval = (i0, i0 + py_delta(days=2))

        slot = (
            misc.get_next_midnight() + py_delta(hours=13),
            misc.get_next_midnight() + py_delta(hours=14)
        )
        result = slots.position(interval, slot)
        expected = (
            slot[0] + py_delta(days=300), slot[1] + py_delta(days=300)
        )

        self.assertEquals(result, expected)

        slot = (
            misc.get_next_midnight() + py_delta(hours=13),
            misc.get_next_midnight() + py_delta(days=1, hours=10)
        )
        result = slots.position(interval, slot)
        expected = (
            slot[0] + py_delta(days=300), slot[1] + py_delta(days=300)
        )

        self.assertEquals(result, expected)

    def test_position_case_D(self):
        """UNIT test: services.common.slots.position (CASE D)
        CASE D: interval[1] > slot[0] > interval[0], slot[1] > interval[1]
        """

        i0 = misc.get_next_midnight() + py_delta(days=300, hours=12)
        interval = (i0, i0 + py_delta(days=2))

        slot = (
            misc.get_next_midnight() + py_delta(hours=13),
            misc.get_next_midnight() + py_delta(days=2, hours=14)
        )
        result = slots.position(interval, slot)
        expected = (
            slot[0] + py_delta(days=300), slot[1] + py_delta(days=300)
        )

        self.assertEquals(result, expected)
