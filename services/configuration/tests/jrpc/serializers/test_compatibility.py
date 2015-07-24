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
"""
__author__ = 'rtubiopa@calpoly.edu'

import logging
from django import test
from services.common.testing import helpers as db_tools
from services.configuration.jrpc.serializers import compatibility as \
    compatibility_serializers


class TestCompatibilitySerializers(test.TestCase):
    """
    Tests for the compatibility serializers
    """

    def setUp(self):
        """
        Populates the initial database with a set of objects required to run
        the following tests.
        """
        self.__verbose_testing = True

        if not self.__verbose_testing:
            logging.getLogger('configuration').setLevel(level=logging.CRITICAL)
            logging.getLogger('django.db.backends.schema')\
                .setLevel(level=logging.CRITICAL)

        self.__gs_1_id = 'gs-castrelos'
        self.__gs_1_ch_1_id = 'chan-cas-1'
        self.__gs_1_ch_2_id = 'chan-cas-2'

        self.__band = db_tools.create_band()
        self.__user_profile = db_tools.create_user_profile()
        self.__gs_1 = db_tools.create_gs(
            user_profile=self.__user_profile, identifier=self.__gs_1_id,
        )
        self.__gs_1_ch_1 = db_tools.gs_add_channel(
            self.__gs_1, self.__band, self.__gs_1_ch_1_id
        )
        self.__gs_1_ch_2 = db_tools.gs_add_channel(
            self.__gs_1, self.__band, self.__gs_1_ch_2_id
        )

        self.__sc_1_id = 'humd'
        self.__sc_1_ch_1_id = 'gmsk-sc-1'
        self.__sc_1_ch_1_f = 437000000
        self.__sc_1_ch_2_id = 'gmsk-sc-2'

        self.__sc_1 = db_tools.create_sc(
            user_profile=self.__user_profile,
            identifier=self.__sc_1_id
        )
        self.__sc_1_ch_1 = db_tools.sc_add_channel(
            self.__sc_1, self.__sc_1_ch_1_f, self.__sc_1_ch_1_id,
        )

    def test_sc_ch_compatibility_serializers(self):
        """JRPC serializers: compatibility tuples
        """

        test_tuples = [
            (self.__gs_1, self.__gs_1_ch_1)
        ]

        c = compatibility_serializers.CompatibilitySerializer\
            .serialize_gs_ch_compatibility_tuples(test_tuples)

        self.assertEquals(len(c), 1, "Wrong number of tuples generated!")

    def test_sc_compatibility_serializers(self):
        """JRPC serializers: compatibility for the spacecraft channels
        """

        test_tuples = [
            (self.__gs_1, self.__gs_1_ch_1)
        ]

        c = compatibility_serializers.CompatibilitySerializer\
            .serialize_gs_ch_compatibility_tuples(test_tuples)

        r = compatibility_serializers.CompatibilitySerializer\
            .serialize_sc_ch_compatibility(self.__sc_1_ch_1, c)

        self.assertEquals(
            r['ScChannel']['identifier'], 'gmsk-sc-1', "Wrong structure!"
        )
