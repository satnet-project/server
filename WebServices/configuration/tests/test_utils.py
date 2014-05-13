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

from datetime import datetime, timedelta
from django.test import TestCase
from configuration.utils import get_remote_user_location, print_dictionary,\
    define_interval, normalize_slots, print_list, merge_slots
from configuration.tests.utils import testdb_create_jrpc_once_rule


class UtilsTest(TestCase):
    
    inp_grul = "129.65.136.182"
    out_grul_latitude = 35.347099
    out_grul_longitude = -120.455299
    
    def test_get_remote_user_location(self):
        """
        Function test.

        This test checks whether the "testing" function is capable of getting
        the location information for a given user by using the WebService from
        GeoPlugin's website.
        """
        latitude, longitude = get_remote_user_location(ip=self.inp_grul)
        
        self.assertAlmostEqual(float(latitude),
                               self.out_grul_latitude, places=4,
                               msg="Wrong latitude!")
        self.assertAlmostEqual(float(longitude),
                               self.out_grul_longitude, places=4,
                               msg="Wrong longitude!")

    def test_print_dictionary(self):
        """
        This function tests the function from the utils module that
        recursively prints out the contents of a dictionary object that may
        or may not have additional dictionary objects nested.
        """
        jrpc_dict = testdb_create_jrpc_once_rule()
        print_dictionary(jrpc_dict)

    def test_define_interval(self):
        """
        This function tests the method for the definition of the interval of
        time that spans from today at 00:00am for D days, until today+D days
        00:00am.
        """
        begin_interval, end_interval = define_interval(days=7)
        print str(begin_interval)
        print str(end_interval)

    def xx_normalize_slots(self):
        """
        THis function tets the method for the normalization of an array of
        slot datetime tuples.
        """
        slots = [
            ((datetime.today()).replace(microsecond=0),
             (datetime.today() + timedelta(hours=2)).replace(microsecond=0)),

            ((datetime.today() + timedelta(hours=3)).replace(microsecond=0),
             (datetime.today() + timedelta(hours=4)).replace(microsecond=0)),

            ((datetime.today() + timedelta(hours=5)).replace(microsecond=0),
             (datetime.today() + timedelta(hours=6)).replace(microsecond=0)),

            ((datetime.today() + timedelta(hours=5)).replace(microsecond=0),
             (datetime.today() + timedelta(hours=5, minutes=30)).replace(microsecond=0)),

            ((datetime.today() + timedelta(hours=5)).replace(microsecond=0),
             (datetime.today() + timedelta(hours=6)).replace(microsecond=0)),

            ((datetime.today() + timedelta(hours=5, minutes=20)).replace(microsecond=0),
             (datetime.today() + timedelta(hours=7)).replace(microsecond=0)),

            ((datetime.today() + timedelta(hours=9)).replace(microsecond=0),
             (datetime.today() + timedelta(hours=10,minutes=5))
             .replace(microsecond=0)),

            ((datetime.today() + timedelta(hours=9, minutes=10))
             .replace(microsecond=0),
             (datetime.today() + timedelta(hours=10,minutes=0))
             .replace(microsecond=0)),

            ((datetime.today() + timedelta(hours=10, minutes=20))
             .replace(microsecond=0),
             (datetime.today() + timedelta(hours=10,minutes=30))
             .replace(microsecond=0)),
            ((datetime.today() + timedelta(hours=10, minutes=25))
             .replace(microsecond=0),
             (datetime.today() + timedelta(hours=10,minutes=35))
             .replace(microsecond=0)),

        ]

        print 'Original Slots...' + str(len(slots))
        print_list(slots)
        n_slots = normalize_slots(slots)
        print 'Normalization...' + str(len(n_slots))
        print_list(n_slots)
        self.assertEquals(len(n_slots), 5,
                          'Wrong slots no, got = ' + str(len(n_slots)))

    def test_merge_none(self):
        """
        Nones and empties test.
        """
        self.assertItemsEqual([], merge_slots(None, None),
                                '[] is the expected response to (None, None)')
        self.assertItemsEqual([], merge_slots([], []),
                                '[] is the expected response to ([], [])')

    def test_merge_case_a(self):
        """
        Case A for merging slots.
        """
        print '$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$'
        print 'TESTING MERGE, CASE A'
        print '$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$'

        p = (datetime.today().replace(microsecond=0),
             datetime.today().replace(microsecond=0)+timedelta(hours=1))
        m = (datetime.today().replace(microsecond=0)+timedelta(hours=1),
             datetime.today().replace(microsecond=0)+timedelta(hours=4))

        expected_s = [p]
        actual_s = merge_slots([p], [m])

        print_list(p, list_name='(+) slots')
        print_list(m, list_name='(-) slots')
        print_list(actual_s, list_name='(A) slots')
        print_list(expected_s, list_name='(EXPECTED) slots')

        self.assertItemsEqual(expected_s, actual_s, 'CASE A: Wrong result!')

    def test_merge_case_b(self):
        """
        Case B for merging slots.
        """
        print '$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$'
        print 'TESTING MERGE, CASE B'
        print '$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$'

        p = (datetime.today().replace(microsecond=0),
             datetime.today().replace(microsecond=0)
             + timedelta(hours=1, minutes=20))
        m = (datetime.today().replace(microsecond=0)+timedelta(hours=1),
             datetime.today().replace(microsecond=0)+timedelta(hours=4))

        expected_s = [(p[0], m[0])]
        actual_s = merge_slots([p], [m])

        print_list(p, list_name='(+) slots')
        print_list(m, list_name='(-) slots')
        print_list(actual_s, list_name='(A) slots')
        print_list(expected_s, list_name='(EXPECTED) slots')

        self.assertItemsEqual(expected_s, actual_s, 'CASE B: Wrong result!')

    def test_merge_case_c(self):
        """
        Case C for merging slots.
        """
        print '$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$'
        print 'TESTING MERGE, CASE C'
        print '$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$'

        p = (datetime.today().replace(microsecond=0),
             datetime.today().replace(microsecond=0) + timedelta(hours=5))
        m = (datetime.today().replace(microsecond=0) + timedelta(hours=1),
             datetime.today().replace(microsecond=0) + timedelta(hours=4))

        expected_s = [(p[0], m[0]), (m[1], p[1])]
        actual_s = merge_slots([p], [m])

        print_list(p, list_name='(+) slots')
        print_list(m, list_name='(-) slots')
        print_list(actual_s, list_name='(A) slots')
        print_list(expected_s, list_name='(EXPECTED) slots')

        self.assertItemsEqual(expected_s, actual_s, 'CASE C: Wrong result!')

    def test_merge_case_d(self):
        """
        Case D for merging slots.
        """
        print '$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$'
        print 'TESTING MERGE, CASE D'
        print '$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$'

        p = (datetime.today().replace(microsecond=0) + timedelta(hours=2),
             datetime.today().replace(microsecond=0) + timedelta(hours=5))
        m = (datetime.today().replace(microsecond=0) + timedelta(hours=1),
             datetime.today().replace(microsecond=0) + timedelta(hours=4))

        expected_s = [(m[1], p[1])]
        actual_s = merge_slots([p], [m])

        print_list(p, list_name='(+) slots')
        print_list(m, list_name='(-) slots')
        print_list(actual_s, list_name='(A) slots')
        print_list(expected_s, list_name='(EXPECTED) slots')

        self.assertItemsEqual(expected_s, actual_s, 'CASE D: Wrong result!')

    def test_merge_case_e(self):
        """
        Case E for merging slots.
        """
        print '$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$'
        print 'TESTING MERGE, CASE E'
        print '$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$'

        p = (datetime.today().replace(microsecond=0) + timedelta(hours=2),
             datetime.today().replace(microsecond=0) + timedelta(hours=3))
        m = (datetime.today().replace(microsecond=0) + timedelta(hours=1),
             datetime.today().replace(microsecond=0) + timedelta(hours=4))

        expected_s = []
        actual_s = merge_slots([p], [m])

        print_list(p, list_name='(+) slots')
        print_list(m, list_name='(-) slots')
        print_list(actual_s, list_name='(A) slots')
        print_list(expected_s, list_name='(EXPECTED) slots')

        self.assertItemsEqual(expected_s, actual_s, 'CASE E: Wrong result!')

    def test_merge_case_f(self):
        """
        Case F for merging slots.
        """
        print '$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$'
        print 'TESTING MERGE, CASE F'
        print '$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$'

        p = (datetime.today().replace(microsecond=0) + timedelta(hours=2),
             datetime.today().replace(microsecond=0) + timedelta(hours=3))
        m = (datetime.today().replace(microsecond=0) + timedelta(hours=0),
             datetime.today().replace(microsecond=0) + timedelta(hours=1))
        expected_s = [p]
        actual_s = merge_slots([p], [m])

        print_list(p, list_name='(+) slots')
        print_list(m, list_name='(-) slots')
        print_list(actual_s, list_name='(A) slots')
        print_list(expected_s, list_name='(EXPECTED) slots')

        self.assertItemsEqual(expected_s, actual_s, 'CASE F: Wrong result!')

    def test_merge_case_no_m_slots(self):
        """
        Case merging p slots without m slots.
        """
        print '$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$'
        print 'TESTING MERGE, CASE NONE M SLOTS'
        print '$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$'

        p = (datetime.today().replace(microsecond=0) + timedelta(hours=2),
             datetime.today().replace(microsecond=0) + timedelta(hours=3))
        q = (datetime.today().replace(microsecond=0) + timedelta(hours=4),
             datetime.today().replace(microsecond=0) + timedelta(hours=5))
        r = (datetime.today().replace(microsecond=0) + timedelta(hours=6),
             datetime.today().replace(microsecond=0) + timedelta(hours=7))
        s = (datetime.today().replace(microsecond=0) + timedelta(hours=8),
             datetime.today().replace(microsecond=0) + timedelta(hours=9))

        expected_s = [p, q, r, s]
        actual_s = merge_slots([p, q, r, s], [])

        print_list(p, list_name='(+) slots')
        print_list([], list_name='(-) slots')
        print_list(actual_s, list_name='(A) slots')
        print_list(expected_s, list_name='(EXPECTED) slots')

        self.assertItemsEqual(expected_s, actual_s, 'CASE NONE M: Wrong '
                                                    'result!')

    def test_merge_case_multiple_end(self):
        """
        Case merging multiple ending (+) slots.
        """
        print '$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$'
        print 'TESTING MERGE, CASE MULITPLE (+)'
        print '$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$'

        p = (datetime.today().replace(microsecond=0) + timedelta(hours=2),
             datetime.today().replace(microsecond=0) + timedelta(hours=3))
        q = (datetime.today().replace(microsecond=0) + timedelta(hours=4),
             datetime.today().replace(microsecond=0) + timedelta(hours=5))
        r = (datetime.today().replace(microsecond=0) + timedelta(hours=6),
             datetime.today().replace(microsecond=0) + timedelta(hours=7))
        s = (datetime.today().replace(microsecond=0) + timedelta(hours=8),
             datetime.today().replace(microsecond=0) + timedelta(hours=9))

        m = (datetime.today().replace(microsecond=0) + timedelta(hours=0),
             datetime.today().replace(microsecond=0) + timedelta(hours=1))
        expected_s = [p, q, r, s]
        actual_s = merge_slots([p, q, r, s], [m])

        print_list(p, list_name='(+) slots')
        print_list(m, list_name='(-) slots')
        print_list(actual_s, list_name='(A) slots')
        print_list(expected_s, list_name='(EXPECTED) slots')

        self.assertItemsEqual(expected_s, actual_s, 'CASE MULTIPLE: Wrong '
                                                    'result!')

    def test_merge_case_complex_1(self):
        """
        Complex case #1.
        """
        print '$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$'
        print 'TESTING MERGE, COMPLEX CASE #1'
        print '$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$'

        p = (datetime.today().replace(microsecond=0) + timedelta(hours=0),
             datetime.today().replace(microsecond=0) + timedelta(hours=1))
        q = (datetime.today().replace(microsecond=0) + timedelta(hours=2),
             datetime.today().replace(microsecond=0) + timedelta(hours=3))
        r = (datetime.today().replace(microsecond=0) + timedelta(hours=2),
             datetime.today().replace(microsecond=0) + timedelta(hours=4))
        s = (datetime.today().replace(microsecond=0) + timedelta(hours=3),
             datetime.today().replace(microsecond=0) + timedelta(hours=5))

        m = (datetime.today().replace(microsecond=0) + timedelta(hours=0),
             datetime.today().replace(microsecond=0) + timedelta(hours=3))

        n = (datetime.today().replace(microsecond=0) + timedelta(hours=3,
                                                                 minutes=30),
             datetime.today().replace(microsecond=0) + timedelta(hours=4))

        expected_s = [(m[1], n[0]), (s[0], n[0]), (n[1], s[1])]
        actual_s = merge_slots([p, q, r, s], [m, n])

        print_list([p, q, r, s], list_name='(+) slots')
        print_list([m, n], list_name='(-) slots')
        print_list(actual_s, list_name='(A) slots')
        print_list(expected_s, list_name='(EXPECTED) slots')

        self.assertItemsEqual(expected_s, actual_s, 'COMPLEX CASE #1: Wrong '
                                                    'result!')


    def test_merge_case_complex_2(self):
        """
        Complex case #2.
        """
        print '$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$'
        print 'TESTING MERGE, COMPLEX CASE #2'
        print '$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$'

        p = (datetime.today().replace(microsecond=0) + timedelta(hours=0),
             datetime.today().replace(microsecond=0) + timedelta(hours=1))
        q = (datetime.today().replace(microsecond=0) + timedelta(hours=2),
             datetime.today().replace(microsecond=0) + timedelta(hours=3))
        r = (datetime.today().replace(microsecond=0) + timedelta(hours=2),
             datetime.today().replace(microsecond=0) + timedelta(hours=4))
        s = (datetime.today().replace(microsecond=0) + timedelta(hours=3),
             datetime.today().replace(microsecond=0) + timedelta(hours=5))

        m = (datetime.today().replace(microsecond=0) + timedelta(hours=0),
             datetime.today().replace(microsecond=0) + timedelta(hours=3))

        expected_s = [(m[1], r[1]), s]
        actual_s = merge_slots([p, q, r, s], [m])

        print_list([p, q, r, s], list_name='(+) slots')
        print_list([m], list_name='(-) slots')
        print_list(actual_s, list_name='(A) slots')
        print_list(expected_s, list_name='(EXPECTED) slots')

        self.assertItemsEqual(expected_s, actual_s, 'COMPLEX CASE #2: Wrong '
                                                    'result!')

    def test_merge_case_complex_3(self):
        """
        Complex case #3.
        """
        print '$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$'
        print 'TESTING MERGE, COMPLEX CASE #3'
        print '$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$'

        p = (datetime.today().replace(microsecond=0) + timedelta(hours=0),
             datetime.today().replace(microsecond=0) + timedelta(hours=1))
        q = (datetime.today().replace(microsecond=0) + timedelta(hours=2),
             datetime.today().replace(microsecond=0) + timedelta(hours=3))
        r = (datetime.today().replace(microsecond=0) + timedelta(hours=2),
             datetime.today().replace(microsecond=0) + timedelta(hours=4))
        s = (datetime.today().replace(microsecond=0) + timedelta(hours=3),
             datetime.today().replace(microsecond=0) + timedelta(hours=5))

        t = (datetime.today().replace(microsecond=0) + timedelta(hours=6),
             datetime.today().replace(microsecond=0) + timedelta(hours=7))
        u = (datetime.today().replace(microsecond=0) + timedelta(hours=8),
             datetime.today().replace(microsecond=0) + timedelta(hours=9))
        v = (datetime.today().replace(microsecond=0) + timedelta(hours=10),
             datetime.today().replace(microsecond=0) + timedelta(hours=11))

        m = (datetime.today().replace(microsecond=0) + timedelta(hours=0),
             datetime.today().replace(microsecond=0) + timedelta(hours=3))

        n = (datetime.today().replace(microsecond=0) + timedelta(hours=3,
                                                                 minutes=30),
             datetime.today().replace(microsecond=0) + timedelta(hours=4))

        expected_s = [(m[1], n[0]), (s[0], n[0]), (n[1], s[1]), t, u, v]
        actual_s = merge_slots([p, q, r, s, t, u, v], [m, n])

        print_list([p, q, r, s], list_name='(+) slots')
        print_list([m, n], list_name='(-) slots')
        print_list(actual_s, list_name='(A) slots')
        print_list(expected_s, list_name='(EXPECTED) slots')

        self.assertItemsEqual(expected_s, actual_s, 'COMPLEX CASE #1: Wrong '
                                                    'result!')
