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
from common.slots import merge_slots


class MergeSlotsTest(TestCase):

    def setUp(self):

        self.__verbose_testing = False

    def test_merge_none(self):
        """
        Nones and empties test.
        """
        self.assertItemsEqual(
            [], merge_slots(None, None),
            '[] is the expected response to (None, None)'
        )
        self.assertItemsEqual(
            [], merge_slots([], []), '[] is the expected response to ([], [])'
        )

    def test_merge_case_a(self):
        """
        Case A for merging slots.
        """
        if self.__verbose_testing:
            print '$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$'
            print 'TESTING MERGE, CASE A'
            print '$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$'

        p = (get_today_utc(),
             get_today_utc() + timedelta(hours=1))
        m = (get_today_utc() + timedelta(hours=1),
             get_today_utc() + timedelta(hours=4))

        expected_s = [p]
        actual_s = merge_slots([p], [m])

        if self.__verbose_testing:
            print_list(p, list_name='(+) slots')
            print_list(m, list_name='(-) slots')
            print_list(actual_s, list_name='(A) slots')
            print_list(expected_s, list_name='(EXPECTED) slots')

        self.assertItemsEqual(expected_s, actual_s, 'CASE A: Wrong result!')

    def test_merge_case_b(self):
        """
        Case B for merging slots.
        """
        if self.__verbose_testing:
            print '$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$'
            print 'TESTING MERGE, CASE B'
            print '$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$'

        p = (get_today_utc(),
             get_today_utc() + timedelta(hours=1, minutes=20))
        m = (get_today_utc() + timedelta(hours=1),
             get_today_utc() + timedelta(hours=4))

        expected_s = [(p[0], m[0])]
        actual_s = merge_slots([p], [m])

        if self.__verbose_testing:
            print_list(p, list_name='(+) slots')
            print_list(m, list_name='(-) slots')
            print_list(actual_s, list_name='(A) slots')
            print_list(expected_s, list_name='(EXPECTED) slots')

        self.assertItemsEqual(expected_s, actual_s, 'CASE B: Wrong result!')

    def test_merge_case_c(self):
        """
        Case C for merging slots.
        """
        if self.__verbose_testing:
            print '$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$'
            print 'TESTING MERGE, CASE C'
            print '$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$'

        p = (get_today_utc(),
             get_today_utc() + timedelta(hours=5))
        m = (get_today_utc() + timedelta(hours=1),
             get_today_utc() + timedelta(hours=4))

        expected_s = [(p[0], m[0]), (m[1], p[1])]
        actual_s = merge_slots([p], [m])

        if self.__verbose_testing:
            print_list(p, list_name='(+) slots')
            print_list(m, list_name='(-) slots')
            print_list(actual_s, list_name='(A) slots')
            print_list(expected_s, list_name='(EXPECTED) slots')

        self.assertItemsEqual(expected_s, actual_s, 'CASE C: Wrong result!')

    def test_merge_case_d(self):
        """
        Case D for merging slots.
        """
        if self.__verbose_testing:
            print '$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$'
            print 'TESTING MERGE, CASE D'
            print '$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$'

        p = (get_today_utc() + timedelta(hours=2),
             get_today_utc() + timedelta(hours=5))
        m = (get_today_utc() + timedelta(hours=1),
             get_today_utc() + timedelta(hours=4))

        expected_s = [(m[1], p[1])]
        actual_s = merge_slots([p], [m])

        if self.__verbose_testing:
            print_list(p, list_name='(+) slots')
            print_list(m, list_name='(-) slots')
            print_list(actual_s, list_name='(A) slots')
            print_list(expected_s, list_name='(EXPECTED) slots')

        self.assertItemsEqual(expected_s, actual_s, 'CASE D: Wrong result!')

    def test_merge_case_e(self):
        """
        Case E for merging slots.
        """
        if self.__verbose_testing:
            print '$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$'
            print 'TESTING MERGE, CASE E'
            print '$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$'

        p = (get_today_utc() + timedelta(hours=2),
             get_today_utc() + timedelta(hours=3))
        m = (get_today_utc() + timedelta(hours=1),
             get_today_utc() + timedelta(hours=4))

        expected_s = []
        actual_s = merge_slots([p], [m])

        if self.__verbose_testing:
            print_list(p, list_name='(+) slots')
            print_list(m, list_name='(-) slots')
            print_list(actual_s, list_name='(A) slots')
            print_list(expected_s, list_name='(EXPECTED) slots')

        self.assertItemsEqual(expected_s, actual_s, 'CASE E: Wrong result!')

    def test_merge_case_f(self):
        """
        Case F for merging slots.
        """
        if self.__verbose_testing:
            print '$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$'
            print 'TESTING MERGE, CASE F'
            print '$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$'

        p = (get_today_utc() + timedelta(hours=2),
             get_today_utc() + timedelta(hours=3))
        m = (get_today_utc() + timedelta(hours=0),
             get_today_utc() + timedelta(hours=1))
        expected_s = [p]
        actual_s = merge_slots([p], [m])

        if self.__verbose_testing:
            print_list(p, list_name='(+) slots')
            print_list(m, list_name='(-) slots')
            print_list(actual_s, list_name='(A) slots')
            print_list(expected_s, list_name='(EXPECTED) slots')

        self.assertItemsEqual(expected_s, actual_s, 'CASE F: Wrong result!')

    def test_merge_case_no_m_slots(self):
        """
        Case merging p slots without m slots.
        """
        if self.__verbose_testing:
            print '$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$'
            print 'TESTING MERGE, CASE NONE M SLOTS'
            print '$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$'

        p = (get_today_utc() + timedelta(hours=2),
             get_today_utc() + timedelta(hours=3))
        q = (get_today_utc() + timedelta(hours=4),
             get_today_utc() + timedelta(hours=5))
        r = (get_today_utc() + timedelta(hours=6),
             get_today_utc() + timedelta(hours=7))
        s = (get_today_utc() + timedelta(hours=8),
             get_today_utc() + timedelta(hours=9))

        expected_s = [p, q, r, s]
        actual_s = merge_slots([p, q, r, s], [])

        if self.__verbose_testing:
            print_list(p, list_name='(+) slots')
            print_list([], list_name='(-) slots')
            print_list(actual_s, list_name='(A) slots')
            print_list(expected_s, list_name='(EXPECTED) slots')

        self.assertItemsEqual(
            expected_s, actual_s, 'CASE NONE M: Wrong result!'
        )

    def test_merge_case_multiple_end(self):
        """
        Case merging multiple ending (+) slots.
        """
        if self.__verbose_testing:
            print '$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$'
            print 'TESTING MERGE, CASE MULITPLE (+)'
            print '$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$'

        p = (get_today_utc() + timedelta(hours=2),
             get_today_utc() + timedelta(hours=3))
        q = (get_today_utc() + timedelta(hours=4),
             get_today_utc() + timedelta(hours=5))
        r = (get_today_utc() + timedelta(hours=6),
             get_today_utc() + timedelta(hours=7))
        s = (get_today_utc() + timedelta(hours=8),
             get_today_utc() + timedelta(hours=9))

        m = (get_today_utc() + timedelta(hours=0),
             get_today_utc() + timedelta(hours=1))
        expected_s = [p, q, r, s]
        actual_s = merge_slots([p, q, r, s], [m])

        if self.__verbose_testing:
            print_list(p, list_name='(+) slots')
            print_list(m, list_name='(-) slots')
            print_list(actual_s, list_name='(A) slots')
            print_list(expected_s, list_name='(EXPECTED) slots')

        self.assertItemsEqual(
            expected_s, actual_s, 'CASE MULTIPLE: Wrong result!'
        )

    def test_merge_case_complex_1(self):
        """
        Complex case #1.
        """
        if self.__verbose_testing:
            print '$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$'
            print 'TESTING MERGE, COMPLEX CASE #1'
            print '$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$'

        p = (get_today_utc() + timedelta(hours=0),
             get_today_utc() + timedelta(hours=1))
        q = (get_today_utc() + timedelta(hours=2),
             get_today_utc() + timedelta(hours=3))
        r = (get_today_utc() + timedelta(hours=2),
             get_today_utc() + timedelta(hours=4))
        s = (get_today_utc() + timedelta(hours=3),
             get_today_utc() + timedelta(hours=5))

        m = (get_today_utc() + timedelta(hours=0),
             get_today_utc() + timedelta(hours=3))

        n = (get_today_utc() + timedelta(hours=3, minutes=30),
             get_today_utc() + timedelta(hours=4))

        expected_s = [(m[1], n[0]), (s[0], n[0]), (n[1], s[1])]
        actual_s = merge_slots([p, q, r, s], [m, n])

        if self.__verbose_testing:
            print_list([p, q, r, s], list_name='(+) slots')
            print_list([m, n], list_name='(-) slots')
            print_list(actual_s, list_name='(A) slots')
            print_list(expected_s, list_name='(EXPECTED) slots')

        self.assertItemsEqual(
            expected_s, actual_s, 'COMPLEX CASE #1: Wrong result!'
        )

    def test_merge_case_complex_2(self):
        """
        Complex case #2.
        """
        if self.__verbose_testing:
            print '$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$'
            print 'TESTING MERGE, COMPLEX CASE #2'
            print '$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$'

        p = (get_today_utc() + timedelta(hours=0),
             get_today_utc() + timedelta(hours=1))
        q = (get_today_utc() + timedelta(hours=2),
             get_today_utc() + timedelta(hours=3))
        r = (get_today_utc() + timedelta(hours=2),
             get_today_utc() + timedelta(hours=4))
        s = (get_today_utc() + timedelta(hours=3),
             get_today_utc() + timedelta(hours=5))

        m = (get_today_utc() + timedelta(hours=0),
             get_today_utc() + timedelta(hours=3))

        expected_s = [(m[1], r[1]), s]
        actual_s = merge_slots([p, q, r, s], [m])

        if self.__verbose_testing:
            print_list([p, q, r, s], list_name='(+) slots')
            print_list([m], list_name='(-) slots')
            print_list(actual_s, list_name='(A) slots')
            print_list(expected_s, list_name='(EXPECTED) slots')

        self.assertItemsEqual(
            expected_s, actual_s, 'COMPLEX CASE #2: Wrong result!'
        )

    def test_merge_case_complex_3(self):
        """
        Complex case #3.
        """
        if self.__verbose_testing:
            print '$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$'
            print 'TESTING MERGE, COMPLEX CASE #3'
            print '$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$'

        p = (get_today_utc() + timedelta(hours=0),
             get_today_utc() + timedelta(hours=1))
        q = (get_today_utc() + timedelta(hours=2),
             get_today_utc() + timedelta(hours=3))
        r = (get_today_utc() + timedelta(hours=2),
             get_today_utc() + timedelta(hours=4))
        s = (get_today_utc() + timedelta(hours=3),
             get_today_utc() + timedelta(hours=5))

        t = (get_today_utc() + timedelta(hours=6),
             get_today_utc() + timedelta(hours=7))
        u = (get_today_utc() + timedelta(hours=8),
             get_today_utc() + timedelta(hours=9))
        v = (get_today_utc() + timedelta(hours=10),
             get_today_utc() + timedelta(hours=11))

        m = (get_today_utc() + timedelta(hours=0),
             get_today_utc() + timedelta(hours=3))

        n = (get_today_utc() + timedelta(hours=3, minutes=30),
             get_today_utc() + timedelta(hours=4))

        expected_s = [(m[1], n[0]), (s[0], n[0]), (n[1], s[1]), t, u, v]
        actual_s = merge_slots([p, q, r, s, t, u, v], [m, n])

        if self.__verbose_testing:
            print_list([p, q, r, s], list_name='(+) slots')
            print_list([m, n], list_name='(-) slots')
            print_list(actual_s, list_name='(A) slots')
            print_list(expected_s, list_name='(EXPECTED) slots')

        self.assertItemsEqual(
            expected_s, actual_s, 'COMPLEX CASE #1: Wrong result!'
        )