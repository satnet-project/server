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

from datetime import timedelta
from django.test import TestCase
from common.misc import print_list, get_today_utc
from common.slots import normalize_slots


class NormalizeSlotsTest(TestCase):

    def setUp(self):

        self.__verbose_testing = False

    def test_normalize_none(self):
        """
        Nones and empties test.
        """
        self.assertItemsEqual(
            [], normalize_slots(None),
            '[] is the expected response to (None)'
        )
        self.assertItemsEqual(
            [], normalize_slots([]),
            '[] is the expected response to ([])'
        )

    def test_normalize_a(self):
        """
        Case A for normalizing slots.
        """
        if self.__verbose_testing:
            print '$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$'
            print 'TESTING NORMALIZE, CASE A'
            print '$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$'

        s = (get_today_utc(),
             get_today_utc() + timedelta(hours=1))
        t = (get_today_utc() + timedelta(hours=2),
             get_today_utc() + timedelta(hours=4))

        expected_s = [s, t]
        actual_s = normalize_slots([s, t])

        if self.__verbose_testing:
            print_list([s, t], list_name='RAW slots')
            print_list(actual_s, list_name='(A) slots')
            print_list(expected_s, list_name='(EXPECTED) slots')

        self.assertItemsEqual(expected_s, actual_s, 'CASE A: Wrong result!')

    def test_normalize_b(self):
        """
        Case B for normalizing slots.
        """
        if self.__verbose_testing:
            print '$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$'
            print 'TESTING NORMALIZE, CASE B'
            print '$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$'

        s = (get_today_utc(),
             get_today_utc() + timedelta(hours=2))
        t = (get_today_utc() + timedelta(hours=1),
             get_today_utc() + timedelta(hours=4))

        expected_s = [(s[0], t[1])]
        actual_s = normalize_slots([s, t])

        if self.__verbose_testing:
            print_list([s, t], list_name='RAW slots')
            print_list(actual_s, list_name='(A) slots')
            print_list(expected_s, list_name='(EXPECTED) slots')

        self.assertItemsEqual(expected_s, actual_s, 'CASE B: Wrong result!')

    def test_normalize_c(self):
        """
        Case C for normalizing slots.
        """
        if self.__verbose_testing:
            print '$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$'
            print 'TESTING NORMALIZE, CASE C'
            print '$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$'

        s = (get_today_utc(),
             get_today_utc() + timedelta(hours=5))
        t = (get_today_utc() + timedelta(hours=1),
             get_today_utc() + timedelta(hours=4))

        expected_s = [s]
        actual_s = normalize_slots([s, t])

        if self.__verbose_testing:
            print_list([s, t], list_name='RAW slots')
            print_list(actual_s, list_name='(A) slots')
            print_list(expected_s, list_name='(EXPECTED) slots')

        self.assertItemsEqual(expected_s, actual_s, 'CASE C: Wrong result!')

    def test_normalize_complex_1(self):
        """
        Case COMPLEX#1 for normalizing slots.
        """
        if self.__verbose_testing:
            print '$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$'
            print 'TESTING NORMALIZE, CASE COMPLEX#1: ABC'
            print '$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$'

        s = (get_today_utc(),
             get_today_utc() + timedelta(hours=1))
        t = (get_today_utc() + timedelta(hours=2),
             get_today_utc() + timedelta(hours=4))

        u = (get_today_utc() + timedelta(hours=5),
             get_today_utc() + timedelta(hours=7))
        v = (get_today_utc() + timedelta(hours=6),
             get_today_utc() + timedelta(hours=9))

        w = (get_today_utc() + timedelta(hours=10),
             get_today_utc() + timedelta(hours=15))
        x = (get_today_utc() + timedelta(hours=11),
             get_today_utc() + timedelta(hours=14))

        expected_s = [s, t, (u[0], v[1]), w]
        actual_s = normalize_slots([s, t, u, v, w, x])

        if self.__verbose_testing:
            print_list([s, t, u, v, w, x], list_name='RAW slots')
            print_list(actual_s, list_name='(A) slots')
            print_list(expected_s, list_name='(EXPECTED) slots')

        self.assertItemsEqual(
            expected_s, actual_s, 'CASE COMPLEX#1: Wrong result!'
        )

    def test_normalize_complex_2(self):
        """
        Case COMPLEX#2 for normalizing slots.
        """
        if self.__verbose_testing:
            print '$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$'
            print 'TESTING NORMALIZE, CASE COMPLEX#2: continuous ABC'
            print '$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$'

        s = (get_today_utc(),
             get_today_utc() + timedelta(hours=1))
        t = (get_today_utc() + timedelta(hours=2),
             get_today_utc() + timedelta(hours=4))
        u = (get_today_utc() + timedelta(hours=3),
             get_today_utc() + timedelta(hours=5))
        v = (get_today_utc() + timedelta(hours=4),
             get_today_utc() + timedelta(hours=4, minutes=10))

        expected_s = [s, (t[0], u[1])]
        actual_s = normalize_slots([s, t, u, v])

        if self.__verbose_testing:
            print_list([s, t, u, v], list_name='RAW slots')
            print_list(actual_s, list_name='(A) slots')
            print_list(expected_s, list_name='(EXPECTED) slots')

        self.assertItemsEqual(
            expected_s, actual_s, 'CASE COMPLEX#1: Wrong result!'
        )