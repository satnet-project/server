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

from datetime import timedelta

from services.common import misc, slots


class NormalizeSlotsTest(test.TestCase):

    def setUp(self):

        self.__verbose_testing = False

    def test_normalize_none(self):
        """UNIT test: services.common.slots.normalize_slots (robustness)
        Nones and empties test.
        """
        self.assertCountEqual(
            [], slots.normalize_slots(None),
            '[] is the expected response to (None)'
        )
        self.assertCountEqual(
            [], slots.normalize_slots([]),
            '[] is the expected response to ([])'
        )

    def test_normalize_a(self):
        """UNIT test: services.common.slots.normalize_slots (case A)
        Case A for normalizing slots.
        """
        if self.__verbose_testing:
            print('$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$')
            print('TESTING NORMALIZE, CASE A')
            print('$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$')

        s = (misc.get_today_utc(),
             misc.get_today_utc() + timedelta(hours=1))
        t = (misc.get_today_utc() + timedelta(hours=2),
             misc.get_today_utc() + timedelta(hours=4))

        expected_s = [s, t]
        actual_s = slots.normalize_slots([s, t])

        if self.__verbose_testing:
            misc.print_list([s, t], name='RAW slots')
            misc.print_list(actual_s, name='(A) slots')
            misc.print_list(expected_s, name='(EXPECTED) slots')

        self.assertCountEqual(expected_s, actual_s, 'CASE A: Wrong result!')

    def test_normalize_b(self):
        """UNIT test: services.common.slots.normalize_slots (case B)
        Case B for normalizing slots.
        """
        if self.__verbose_testing:
            print('$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$')
            print('TESTING NORMALIZE, CASE B')
            print('$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$')

        s = (misc.get_today_utc(),
             misc.get_today_utc() + timedelta(hours=2))
        t = (misc.get_today_utc() + timedelta(hours=1),
             misc.get_today_utc() + timedelta(hours=4))

        expected_s = [(s[0], t[1])]
        actual_s = slots.normalize_slots([s, t])

        if self.__verbose_testing:
            misc.print_list([s, t], name='RAW slots')
            misc.print_list(actual_s, name='(A) slots')
            misc.print_list(expected_s, name='(EXPECTED) slots')

        self.assertCountEqual(expected_s, actual_s, 'CASE B: Wrong result!')

    def test_normalize_c(self):
        """UNIT test: services.common.slots.normalize_slots (case C)
        Case C for normalizing slots.
        """
        if self.__verbose_testing:
            print('$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$')
            print('TESTING NORMALIZE, CASE C')
            print('$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$')

        s = (misc.get_today_utc(),
             misc.get_today_utc() + timedelta(hours=5))
        t = (misc.get_today_utc() + timedelta(hours=1),
             misc.get_today_utc() + timedelta(hours=4))

        expected_s = [s]
        actual_s = slots.normalize_slots([s, t])

        if self.__verbose_testing:
            misc.print_list([s, t], name='RAW slots')
            misc.print_list(actual_s, name='(A) slots')
            misc.print_list(expected_s, name='(EXPECTED) slots')

        self.assertCountEqual(expected_s, actual_s, 'CASE C: Wrong result!')

    def test_normalize_complex_1(self):
        """UNIT test: services.common.slots.normalize_slots (complex case #1)
        Case COMPLEX#1 for normalizing slots.
        """
        if self.__verbose_testing:
            print('$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$')
            print('TESTING NORMALIZE, CASE COMPLEX#1: ABC')
            print('$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$')

        s = (misc.get_today_utc(),
             misc.get_today_utc() + timedelta(hours=1))
        t = (misc.get_today_utc() + timedelta(hours=2),
             misc.get_today_utc() + timedelta(hours=4))

        u = (misc.get_today_utc() + timedelta(hours=5),
             misc.get_today_utc() + timedelta(hours=7))
        v = (misc.get_today_utc() + timedelta(hours=6),
             misc.get_today_utc() + timedelta(hours=9))

        w = (misc.get_today_utc() + timedelta(hours=10),
             misc.get_today_utc() + timedelta(hours=15))
        x = (misc.get_today_utc() + timedelta(hours=11),
             misc.get_today_utc() + timedelta(hours=14))

        expected_s = [s, t, (u[0], v[1]), w]
        actual_s = slots.normalize_slots([s, t, u, v, w, x])

        if self.__verbose_testing:
            misc.print_list([s, t, u, v, w, x], name='RAW slots')
            misc.print_list(actual_s, name='(A) slots')
            misc.print_list(expected_s, name='(EXPECTED) slots')

        self.assertCountEqual(
            expected_s, actual_s, 'CASE COMPLEX#1: Wrong result!'
        )

    def test_normalize_complex_2(self):
        """UNIT test: services.common.slots.normalize_slots (complex case #2)
        Case COMPLEX#2 for normalizing slots.
        """
        if self.__verbose_testing:
            print('$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$')
            print('TESTING NORMALIZE, CASE COMPLEX#2: continuous ABC')
            print('$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$')

        s = (misc.get_today_utc(),
             misc.get_today_utc() + timedelta(hours=1))
        t = (misc.get_today_utc() + timedelta(hours=2),
             misc.get_today_utc() + timedelta(hours=4))
        u = (misc.get_today_utc() + timedelta(hours=3),
             misc.get_today_utc() + timedelta(hours=5))
        v = (misc.get_today_utc() + timedelta(hours=4),
             misc.get_today_utc() + timedelta(hours=4, minutes=10))

        expected_s = [s, (t[0], u[1])]
        actual_s = slots.normalize_slots([s, t, u, v])

        if self.__verbose_testing:
            misc.print_list([s, t, u, v], name='RAW slots')
            misc.print_list(actual_s, name='(A) slots')
            misc.print_list(expected_s, name='(EXPECTED) slots')

        self.assertCountEqual(
            expected_s, actual_s, 'CASE COMPLEX#1: Wrong result!'
        )
