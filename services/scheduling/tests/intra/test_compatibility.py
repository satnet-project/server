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

from django import test

from services.common import helpers as db_tools
from services.configuration.models import bands as band_models
from services.scheduling.models import compatibility as compat_models


class SegmentCompatibilityTest(test.TestCase):
    """
    Class with the UNIT tests for validating the compatibility models.
    """

    def setUp(self):

        self.__verbose_testing = False

        if not self.__verbose_testing:
            logging.getLogger('configuration').setLevel(level=logging.CRITICAL)
            logging.getLogger('scheduling').setLevel(level=logging.CRITICAL)
            logging.getLogger('simulation').setLevel(level=logging.CRITICAL)

        # noinspection PyUnresolvedReferences
        from services.scheduling.signals import compatibility

        self.__gs_1_id = 'gs-castrelos'
        self.__gs_1_ch_1_id = 'chan-cas-1'
        self.__gs_1_ch_2_id = 'chan-cas-2'
        self.__gs_1_ch_3_id = 'chan-cas-3'

        self.__sc_1_id = 'sc-xatcobeo'
        self.__sc_1_ch_1_id = 'xatco-fm-1'
        self.__sc_1_ch_1_f = 437000000
        self.__sc_1_ch_2_id = 'xatco-fm-2'
        self.__sc_1_ch_3_id = 'xatco-fm-3'
        self.__sc_1_ch_4_id = 'xatco-afsk-1'

        self.__band = db_tools.create_band()
        self.__user_profile = db_tools.create_user_profile()
        self.__gs = db_tools.create_gs(
            user_profile=self.__user_profile, identifier=self.__gs_1_id,
        )
        self.__sc = db_tools.create_sc(
            user_profile=self.__user_profile, identifier=self.__sc_1_id
        )

    def test_compatibility_case_1(self):
        """INTR test: services.scheduling - basic SC_CH compatibility test (1)
        (CHANGE-1) +SC_CH
        (CHECK-1) len(SegmentCompatibility) = 0
        (CHANGE-2) -SC_CH
        (CHECK-2) len(SegmentCompatibility) = 0
        """
        if self.__verbose_testing:
            print('##### test_compatibility_case_1')

        db_tools.sc_add_channel(
            self.__sc, self.__sc_1_ch_1_f, self.__sc_1_ch_1_id,
        )
        self.assertEqual(
            len(compat_models.ChannelCompatibility.objects.all()), 0,
            'Table must be empty!'
        )
        db_tools.remove_sc_channel(self.__sc_1_ch_1_id)
        self.assertEqual(
            len(compat_models.ChannelCompatibility.objects.all()), 0,
            'Table must be empty!'
        )

    def test_compatibility_case_2(self):
        """INTR test: services.scheduling - basic GS_CH compatibility test (2)
        (CHANGE-1) +GS_CH
        (CHECK-1) len(SegmentCompatibility) = 0
        (CHANGE-2) -GS_CH
        (CHECK-2) len(SegmentCompatibility) = 0
        """
        if self.__verbose_testing:
            print('##### test_compatibility_case_2')

        db_tools.gs_add_channel(
            self.__gs, self.__band, self.__gs_1_ch_1_id,
        )
        self.assertEqual(
            len(compat_models.ChannelCompatibility.objects.all()), 0,
            'Table must be empty!'
        )
        db_tools.remove_gs_channel(self.__gs_1_id, self.__gs_1_ch_1_id)

    def test_compatibility_case_3(self):
        """INTR test: services.scheduling - basic MIXED compatibility test (1)
        (CHANGE-1) +SC_CH
        (CHANGE-2) +GS_CH (Non compatible)
        (CHECK-1) len(SegmentCompatibility) = 0
        (CHANGE-3) -SC_CH
        (CHECK-2) len(SegmentCompatibility) = 0
        (CHANGE-4) +SC_CH (Non compatible)
        (CHANGE-5) -GS_CH
        (CHECK-3) len(SegmentCompatibility) = 0
        """
        if self.__verbose_testing:
            print('##### test_compatibility_case_3')

        # (CHANGE-1)
        db_tools.sc_add_channel(
            self.__sc, self.__sc_1_ch_1_f, self.__sc_1_ch_1_id,
        )
        # (CHANGE-2)
        db_tools.gs_add_channel(
            self.__gs, self.__band, self.__gs_1_ch_1_id,
            polarizations=[
                band_models.AvailablePolarizations.objects.get(
                    polarization='LHCP'
                )
            ]
        )
        # (CHECK-1)
        self.assertEqual(
            len(compat_models.ChannelCompatibility.objects.all()), 0,
            'Table must be empty!'
        )
        # (CHANGE-3)
        db_tools.remove_sc_channel(self.__sc_1_ch_1_id)
        # (CHECK-2)
        self.assertEqual(
            len(compat_models.ChannelCompatibility.objects.all()), 0,
            'Table must be empty!'
        )
        # (CHANGE-4)
        db_tools.sc_add_channel(
            self.__sc, self.__sc_1_ch_1_f, self.__sc_1_ch_1_id,
        )
        # (CHANGE-5)
        db_tools.remove_gs_channel(self.__gs_1_id, self.__gs_1_ch_1_id)
        # (CHECK-3)
        self.assertEqual(
            len(compat_models.ChannelCompatibility.objects.all()), 0,
            'Table must be empty!'
        )
        # Unchecked change, just for cleaning the database.
        db_tools.remove_sc_channel(self.__sc_1_ch_1_id)

    def test_compatibility_case_4(self):
        """INTR test: services.scheduling - basic MIXED compatibility test (2)
        (CHANGE-1) +SC_CH
        (CHANGE-2) +GS_CH (Compatible)
        (CHECK-1) len(SegmentCompatibility) = 1
        (CHANGE-3) -SC_CH
        (CHECK-2) len(SegmentCompatibility) = 0
        (CHANGE-4) +SC_CH (Compatible)
        (CHECK-3) len(SegmentCompatibility) = 1
        (CHANGE-5) -GS_CH
        (CHECK-3) len(SegmentCompatibility) = 0
        """
        if self.__verbose_testing:
            print('##### test_compatibility_case_4')

        # (CHANGE-1)
        db_tools.sc_add_channel(
            self.__sc, self.__sc_1_ch_1_f, self.__sc_1_ch_1_id,
        )
        # (CHANGE-2)
        db_tools.gs_add_channel(
            self.__gs, self.__band, self.__gs_1_ch_1_id,
        )
        # (CHECK-1)
        self.assertEqual(
            len(compat_models.ChannelCompatibility.objects.all()), 1,
            'Table must have 1 entr(ies)!'
        )
        # (CHANGE-3)
        db_tools.remove_sc_channel(self.__sc_1_ch_1_id)
        # (CHECK-2)
        self.assertEqual(
            len(compat_models.ChannelCompatibility.objects.all()), 0,
            'Table must be empty!'
        )
        # (CHANGE-4)
        db_tools.sc_add_channel(
            self.__sc, self.__sc_1_ch_1_f, self.__sc_1_ch_1_id,
        )
        # (CHECK-3)
        self.assertEqual(
            len(compat_models.ChannelCompatibility.objects.all()), 1,
            'Table must have 1 entr(ies)!'
        )
        # (CHANGE-5)
        db_tools.remove_gs_channel(self.__gs_1_id, self.__gs_1_ch_1_id)
        # (CHECK-4)
        self.assertEqual(
            len(compat_models.ChannelCompatibility.objects.all()), 0,
            'Table must be empty!'
        )
        # Unchecked change, just for cleaning the database.
        db_tools.remove_sc_channel(self.__sc_1_ch_1_id)

    def test_compatibility_case_5(self):
        """INTR test: services.scheduling - complex MIXED compatibility test (1)
        (CHANGE-1) +SC_CH
        (CHANGE-2) +GS_CH (Compatible)
        (CHANGE-3) +GS_CH
        (CHANGE-4) +GS_CH (Compatible)
        (CHECK-1)   len(SegmentCompatibility) = 2
        (CHANGE-5) -GS_CH (Compatible)
        (CHECK-2)   len(SegmentCompatibility) = 1
        (CHANGE-6) -GS_CH
        (CHECK-3)   len(SegmentCompatibility) = 1
        (CHANGE-7) -GS_CH (Compatible)
        (CHECK-4)   len(SegmentCompatibility) = 0
        (CHANGE-8) -SC_CH
        (CHECK-5)   len(SegmentCompatibility) = 0
        (CHANGE-9) +GS_CH (GS-1)
        (CHANGE-A) +GS_CH (GS-2)
        (CHANGE-B) +SC_CH (Compatible with GS-2)
        (CHECK-6)   len(SegmentCompatibility) = 1
        (CHANGE-C) -GS_CH (GS-1)
        (CHECK-7)   len(SegmentCompatibility) = 1
        (CHANGE-D) +GS_CH (GS-3, Compatible)
        (CHECK-8)   len(SegmentCompatibility) = 2
        (CHANGE-E) -SC_CH
        (CHECK-9)   len(SegmentCompatibility) = 0
        (CHANGE-F) +SC_CH (Compatible with GS-2 & GS-3)
        (CHECK-A)   len(SegmentCompatibility) = 2
        """
        if self.__verbose_testing:
            print('##### test_compatibility_case_5')

        # (CHANGE-1)
        self.__sc_1_ch_1 = db_tools.sc_add_channel(
            self.__sc, self.__sc_1_ch_1_f, self.__sc_1_ch_1_id,
        )
        # (CHANGE-2)
        db_tools.gs_add_channel(
            self.__gs, self.__band, self.__gs_1_ch_1_id,
        )
        # (CHANGE-3)
        db_tools.gs_add_channel(
            self.__gs, self.__band, self.__gs_1_ch_2_id,
            polarizations=[
                band_models.AvailablePolarizations.objects.get(
                    polarization='LHCP'
                )
            ]
        )
        # (CHANGE-4)
        db_tools.gs_add_channel(
            self.__gs, self.__band, self.__gs_1_ch_3_id,
        )
        # >>>>> (CHECK-1) <<<<< #
        self.assertEqual(
            compat_models.ChannelCompatibility.objects.filter(
                spacecraft_channel__identifier=self.__sc_1_ch_1_id
            ).count(),
            2,
            'Table must have 2 entr(ies)!'
        )
        # (CHANGE-5)
        db_tools.remove_gs_channel(self.__gs_1_id, self.__gs_1_ch_1_id)
        # >>>>> (CHECK-2) <<<<< #
        self.assertEqual(
            compat_models.ChannelCompatibility.objects.filter(
                spacecraft_channel__identifier=self.__sc_1_ch_1_id
            ).count(),
            1,
            'Table must have 1 entr(ies)!'
        )
        # (CHANGE-6)
        db_tools.remove_gs_channel(self.__gs_1_id, self.__gs_1_ch_2_id)
        # >>>>> (CHECK-3) <<<<< #
        self.assertEqual(
            compat_models.ChannelCompatibility.objects.filter(
                spacecraft_channel__identifier=self.__sc_1_ch_1_id
            ).count(),
            1,
            'Table must have 1 entr(ies)!'
        )
        # (CHANGE-7)
        db_tools.remove_gs_channel(self.__gs_1_id, self.__gs_1_ch_3_id)
        # >>>>> (CHECK-4) <<<<< #
        self.assertEqual(
            len(compat_models.ChannelCompatibility.objects.all()), 0,
            'Table must have 0 entr(ies)!'
        )
        # (CHANGE-8)
        db_tools.remove_sc_channel(self.__sc_1_ch_1_id)
        # >>>>> (CHECK-5) <<<<< #
        self.assertEqual(
            len(compat_models.ChannelCompatibility.objects.all()), 0,
            'Table must have 0 entr(ies)!'
        )
        # (CHANGE-9)
        db_tools.gs_add_channel(
            self.__gs, self.__band, self.__gs_1_ch_1_id,
            polarizations=[
                band_models.AvailablePolarizations.objects.get(
                    polarization='LHCP'
                )
            ]
        )
        # (CHANGE-A)
        db_tools.gs_add_channel(
            self.__gs, self.__band, self.__gs_1_ch_2_id,
        )
        # (CHANGE-B)
        self.__sc_1_ch_1 = db_tools.sc_add_channel(
            self.__sc, self.__sc_1_ch_1_f, self.__sc_1_ch_1_id,
        )
        # >>>>> (CHECK-6) <<<<< #
        self.assertEqual(
            compat_models.ChannelCompatibility.objects.filter(
                spacecraft_channel__identifier=self.__sc_1_ch_1_id
            ).count(),
            1,
            'Table must have 1 entr(ies)!'
        )
        # (CHANGE-C)
        db_tools.remove_gs_channel(self.__gs_1_id, self.__gs_1_ch_1_id)
        # >>>>> (CHECK-7) <<<<< #
        self.assertEqual(
            compat_models.ChannelCompatibility.objects.filter(
                spacecraft_channel__identifier=self.__sc_1_ch_1_id
            ).count(),
            1,
            'Table must have 1 entr(ies)!'
        )
        # (CHANGE-D)
        db_tools.gs_add_channel(
            self.__gs, self.__band, self.__gs_1_ch_3_id,
        )
        # >>>>> (CHECK-8) <<<<< #
        self.assertEqual(
            compat_models.ChannelCompatibility.objects.filter(
                spacecraft_channel__identifier=self.__sc_1_ch_1_id
            ).count(),
            2,
            'Table must have 2 entr(ies)!'
        )
        # (CHANGE-E)
        db_tools.remove_sc_channel(self.__sc_1_ch_1_id)
        # >>>>> (CHECK-9) <<<<< #
        self.assertEqual(
            len(compat_models.ChannelCompatibility.objects.all()), 0,
            'Table must have 0 entr(ies)!'
        )
        # (CHANGE-F)
        self.__sc_1_ch_1 = db_tools.sc_add_channel(
            self.__sc, self.__sc_1_ch_1_f, self.__sc_1_ch_1_id,
        )
        # >>>>> (CHECK-A) <<<<< #
        self.assertEqual(
            compat_models.ChannelCompatibility.objects.filter(
                spacecraft_channel__identifier=self.__sc_1_ch_1_id
            ).count(),
            2,
            'Table must have 2 entr(ies)!'
        )
        # Unchecked change, just for cleaning the database.
        db_tools.remove_sc_channel(self.__sc_1_ch_1_id)
        db_tools.remove_gs_channel(self.__gs_1_id, self.__gs_1_ch_2_id)
        db_tools.remove_gs_channel(self.__gs_1_id, self.__gs_1_ch_3_id)

    def test_compatibility_case_6(self):
        """INTR test: services.scheduling - complex MIXED compatibility test (2)
        (CHANGE-1) +SC-1
        (CHANGE-2) +SC-2
        (CHANGE-3) +GS-1 (SC-1 & SC-2 compatible)
        (CHANGE-4) +GS-2 (SC-1 & SC-2 compatible)
        (CHECK-1)   len(SegmentCompatibility) = 4
        (CHANGE-5) +SC-3 (GS-1 & GS-2 compatible)
        (CHANGE-6) +SC-4 (GS-1 & GS-2 compatible)
        (CHECK-2)   len(SegmentCompatibility) = 8
        (CHANGE-7) -GS-1
        (CHECK-3)   len(SegmentCompatibility) = 4
        (CHANGE-8) -GS-2
        (CHECK-4)   len(SegmentCompatibility) = 0
        """
        if self.__verbose_testing:
            print('##### test_compatibility_case_6')

        # (CHANGE-1)
        self.__sc_1_ch_1 = db_tools.sc_add_channel(
            self.__sc, self.__sc_1_ch_1_f, self.__sc_1_ch_1_id,
        )
        # (CHANGE-2)
        self.__sc_1_ch_2 = db_tools.sc_add_channel(
            self.__sc, self.__sc_1_ch_1_f, self.__sc_1_ch_2_id,
        )
        # (CHANGE-3)
        db_tools.gs_add_channel(
            self.__gs, self.__band, self.__gs_1_ch_1_id,
        )
        # (CHANGE-4)
        db_tools.gs_add_channel(
            self.__gs, self.__band, self.__gs_1_ch_2_id,
        )
        # >>>>> (CHECK-1) <<<<< #
        self.assertEqual(
            len(compat_models.ChannelCompatibility.objects.all()),
            4,
            'Table must have 4 entr(ies)!'
        )
        # (CHANGE-5)
        self.__sc_1_ch_3 = db_tools.sc_add_channel(
            self.__sc, self.__sc_1_ch_1_f, self.__sc_1_ch_3_id,
        )
        # (CHANGE-6)
        self.__sc_1_ch_4 = db_tools.sc_add_channel(
            self.__sc, self.__sc_1_ch_1_f, self.__sc_1_ch_4_id,
        )
        # >>>>> (CHECK-2) <<<<< #
        self.assertEqual(
            len(compat_models.ChannelCompatibility.objects.all()),
            8,
            'Table must have 8 entr(ies)!'
        )
        # (CHANGE-7)
        db_tools.remove_gs_channel(self.__gs_1_id, self.__gs_1_ch_1_id)
        # >>>>> (CHECK-3) <<<<< #
        self.assertEqual(
            len(compat_models.ChannelCompatibility.objects.all()),
            4,
            'Table must have 4 entr(ies)!'
        )
        # (CHANGE-8)
        db_tools.remove_gs_channel(self.__gs_1_id, self.__gs_1_ch_2_id)
        # >>>>> (CHECK-4) <<<<< #
        self.assertEqual(
            len(compat_models.ChannelCompatibility.objects.all()), 0,
            'Table must have 0 entr(ies)!'
        )
        # Unchecked change, just for cleaning the database.
        db_tools.remove_sc_channel(self.__sc_1_ch_1_id)
        db_tools.remove_sc_channel(self.__sc_1_ch_2_id)
        db_tools.remove_sc_channel(self.__sc_1_ch_3_id)
        db_tools.remove_sc_channel(self.__sc_1_ch_4_id)
