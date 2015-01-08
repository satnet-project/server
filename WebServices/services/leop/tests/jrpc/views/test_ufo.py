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
import datadiff
from django import test, db as django_db
from django.core import exceptions as django_ex
from services.common.testing import helpers as db_tools
from services.leop.models import leop as leop_models
from services.leop.models import ufo as ufo_models
from services.leop.jrpc.views import cluster as jrpc_leop
from services.leop.jrpc.views import ufo as jrpc_ufo
from services.leop.jrpc.serializers import cluster as cluster_serial


class TestUFOViews(test.TestCase):
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
        self.__leop_id = 'leop_cluster_4testing'
        self.__leop = db_tools.create_cluster(
            admin=self.__admin, identifier=self.__leop_id
        )

        if not self.__verbose_testing:
            logging.getLogger('leop').setLevel(level=logging.CRITICAL)

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
        pass