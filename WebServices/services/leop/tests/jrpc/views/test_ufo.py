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

import logging
from django import test, db as django_db
from services.common.testing import helpers as db_tools
from services.configuration.models import segments as segment_models
from services.configuration.models import tle as tle_models
from services.leop.models import leop as leop_models
from services.leop.models import ufo as ufo_models
from services.leop.jrpc.views import ufo as jrpc_ufo


class TestUFOJRPCViews(test.TestCase):
    """Test class for the UFO JRPC methods.
    """

    def setUp(self):
        """Database setup
        """
        self.__verbose_testing = False

        self.__user = db_tools.create_user_profile()
        self.__admin = db_tools.create_user_profile(
            username='user_admin',
            email='admin@satnet.org',
            is_staff=True
        )

        self.__request = db_tools.create_request(user_profile=self.__user)
        self.__leop_id = 'elana'
        self.__leop = db_tools.create_cluster(
            admin=self.__admin, identifier=self.__leop_id
        )

        self.__ufo_id = 50
        self.__ufo_callsign = 'Scully'
        self.__ufo_tle_l1 = '1 27844U 03031E   15007.47529781  .00000328' \
                            '  00000-0  16930-3 0  1108'
        self.__ufo_tle_l2 = '2 27844  98.6976  18.3001 0010316' \
                            '  50.6742 104.9393 14.21678727597601'

        self.__ufo_2_id = 60

        if not self.__verbose_testing:
            logging.getLogger('leop').setLevel(level=logging.CRITICAL)
            logging.getLogger('simulation').setLevel(level=logging.CRITICAL)

    def test_add_ufo(self):
        """UNIT JRPC test
        Validates the creation of a new UFO object for a given LEOP cluster.
        """
        try:
            jrpc_ufo.add(None, -1)
            self.fail('An exception should have been rised, ufo_id < 0')
        except leop_models.LEOP.DoesNotExist:
            pass
        try:
            jrpc_ufo.add('', -1)
            self.fail('An exception should have been rised, ufo_id < 0')
        except leop_models.LEOP.DoesNotExist:
            pass
        try:
            jrpc_ufo.add('open:sesame', -1)
            self.fail('An exception should have been rised, ufo_id < 0')
        except leop_models.LEOP.DoesNotExist:
            pass
        try:
            jrpc_ufo.add(self.__leop_id, -1)
            self.fail('An exception should have been rised, ufo_id < 0')
        except django_db.IntegrityError:
            pass

        expected = 1
        actual = jrpc_ufo.add(self.__leop_id, expected)
        self.assertEquals(actual, expected, 'Identifiers should not differ')

        try:
            jrpc_ufo.add(self.__leop_id, expected)
            self.fail('UFO object exists, exception should have been raised')
        except django_db.IntegrityError:
            pass

    def test_remove_ufo(self):
        """UNIT JRPC test
        Validates the removal of an existing UFO object from a given LEOP
        cluster.
        """
        try:
            jrpc_ufo.remove(None, -1)
            self.fail('An exception should have been rised, ufo_id < 0')
        except leop_models.LEOP.DoesNotExist:
            pass
        try:
            jrpc_ufo.remove('', -1)
            self.fail('An exception should have been rised, ufo_id < 0')
        except leop_models.LEOP.DoesNotExist:
            pass
        try:
            jrpc_ufo.remove('open:sesame', -1)
            self.fail('An exception should have been rised, ufo_id < 0')
        except leop_models.LEOP.DoesNotExist:
            pass
        try:
            jrpc_ufo.remove(self.__leop_id, -1)
            self.fail('An exception should have been rised, ufo_id < 0')
        except ufo_models.UFO.DoesNotExist:
            pass

        expected = 1
        expected = jrpc_ufo.add(self.__leop_id, expected)
        actual = jrpc_ufo.remove(self.__leop_id, expected)
        self.assertEquals(actual, expected, 'Identifiers should not differ')

    def test_identify_ufo(self):
        """UNIT JRPC test
        Validates the identification of a given UFO.
        """
        self.assertEquals(
            jrpc_ufo.add(self.__leop_id, self.__ufo_id),
            self.__ufo_id,
            'Identifiers should not differ'
        )

        self.assertEquals(
            jrpc_ufo.identify(
                self.__leop_id, self.__ufo_id, self.__ufo_callsign,
                self.__ufo_tle_l1, self.__ufo_tle_l2,
                request=self.__request
            ),
            self.__ufo_id
        )
        t_id = (
            'leop:' + str(self.__leop_id) + ':ufo:' + str(self.__ufo_id) +
            ':cs:' + str(self.__ufo_callsign)
        )[0:23]
        self.assertTrue(
            tle_models.TwoLineElement.objects.filter(identifier=t_id).exists(),
            'A TLE should have been found, id = ' + str(t_id)
        )
        x_id = (
            'leop:' + str(self.__leop_id) + ':ufo:' + str(self.__ufo_id) +
            ':cs:' + str(self.__ufo_callsign)
        )[0:29]
        self.assertTrue(
            segment_models.Spacecraft.objects.filter(identifier=x_id).exists(),
            'A spacecraft should have been found, id = ' + str(x_id)
        )

    def test_forget_ufo(self):
        """UNIT JRPC test
        Validates the process for <forgetting> about a given UFO.
        """
        actual_id = jrpc_ufo.add(self.__leop_id, self.__ufo_2_id)
        self.assertEquals(actual_id, self.__ufo_2_id, 'Identifiers differ!')
        actual_id = jrpc_ufo.identify(
            self.__leop_id, self.__ufo_2_id, self.__ufo_callsign,
            self.__ufo_tle_l1, self.__ufo_tle_l2,
            request=self.__request
        )
        self.assertEquals(actual_id, self.__ufo_2_id, 'Wrong ID returned!')
        actual_id = jrpc_ufo.forget(self.__leop_id, self.__ufo_2_id)
        self.assertEquals(actual_id, self.__ufo_2_id, 'Wrong ID returned!')

        t_id = (
            'leop:' + str(self.__leop_id) + ':ufo:' + str(self.__ufo_2_id) +
            ':cs:' + str(self.__ufo_callsign)
        )[0:23]
        self.assertFalse(
            tle_models.TwoLineElement.objects.filter(identifier=t_id).exists(),
            'A TLE should NOT have been found, id = ' + str(t_id)
        )
        x_id = (
            'leop:' + str(self.__leop_id) + ':ufo:' + str(self.__ufo_2_id) +
            ':cs:' + str(self.__ufo_callsign)
        )[0:29]
        self.assertFalse(
            segment_models.Spacecraft.objects.filter(identifier=x_id).exists(),
            'A spacecraft should NOT have been found, id = ' + str(x_id)
        )

    def test_update_ufo(self):
        """UNIT JRPC test
        """
        self.assertEquals(
            jrpc_ufo.add(self.__leop_id, self.__ufo_id),
            self.__ufo_id,
            'Identifiers should not differ'
        )
        jrpc_ufo.identify(
            self.__leop_id, self.__ufo_id, self.__ufo_callsign,
            self.__ufo_tle_l1, self.__ufo_tle_l2,
            request=self.__request
        )
        jrpc_ufo.update(
            self.__leop_id, self.__ufo_id,
            'NEWXCCXXC', self.__ufo_tle_l1, self.__ufo_tle_l2
        )