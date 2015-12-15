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

:Author:
    Ricardo Tubio-Pardavila (rtubiopa@calpoly.edu)
"""
__author__ = 'rtubiopa@calpoly.edu'

import datetime
import logging

from django import test
from django.forms.models import model_to_dict

from services.common import misc, simulation
from services.common import helpers as db_tools
from services.configuration.jrpc.serializers import rules as jrpc_serial
from services.configuration.jrpc.views import rules as jrpc_rules_if
from services.configuration.models import rules as rule_models
from services.scheduling.models import availability


class TestAvailability(test.TestCase):

    def setUp(self):

        self.__verbose_testing = False

        if not self.__verbose_testing:
            logging.getLogger('configuration').setLevel(level=logging.CRITICAL)
            logging.getLogger('scheduling').setLevel(level=logging.CRITICAL)

        self.__rule_date = misc.get_today_utc()
        self.__rule_s_time = misc.get_today_utc().replace(
            hour=12, minute=0, second=0, microsecond=0
        )
        self.__rule_e_time = self.__rule_s_time + datetime.timedelta(hours=5)

        self.__utc_s_date = self.__rule_date - datetime.timedelta(days=1)
        self.__utc_e_date = self.__rule_date + datetime.timedelta(days=365)
        self.__utc_s_time = self.__rule_s_time
        self.__utc_e_time = self.__rule_e_time

        self.__gs_1_id = 'gs-castrelos'
        self.__gs_1_ch_1_id = 'chan-cas-1'
        self.__gs_2_id = 'gs-cuvi'

        # noinspection PyUnresolvedReferences
        from services.scheduling.signals import availability, compatibility

        self.__band = db_tools.create_band()
        self.__user_profile = db_tools.create_user_profile()
        self.__gs = db_tools.create_gs(
            user_profile=self.__user_profile, identifier=self.__gs_1_id,
        )
        self.__gs_2 = db_tools.create_gs(
            user_profile=self.__user_profile, identifier=self.__gs_2_id,
        )
        self.__gs_1_ch_1 = db_tools.gs_add_channel(
            self.__gs, self.__band, self.__gs_1_ch_1_id
        )

    def _test_0_add_slots_no_rules(self):
        """INTR test: services.scheduling - add slots without rules
        This method tests the addition of new availability slots to the
        AvailabilitySlots table in the database, when no rule has still been
        defined. Therefore, no slot should be generated or added.
        """
        if self.__verbose_testing:
            print('##### test_add_slots: no rules')

        a_slots = rule_models.AvailabilityRule.objects.get_availability_slots(
            self.__gs
        )
        self.assertEqual(
            len(a_slots), 0, 'No new available slots should\'ve been created.'
        )
        self.assertEqual(
            len(availability.AvailabilitySlot.objects.all()), 0,
            'No AvailabilitySlots expected.'
        )

    def _test_1a_add_slots_once_rule(self):
        """INTR test: services.scheduling - add slots w/single ONCE rule (1A)
        This method tests the addition of new availability slots when there
        is only a single applicable ONCE-type rule in the database.
        Therefore, a single slot should be generated and added to the database.
        """
        if self.__verbose_testing:
            print('##### test_add_slots (A): single once rule (ADD)')

        rule_cfg = db_tools.create_jrpc_once_rule(
            starting_time=self.__rule_s_time, ending_time=self.__rule_e_time
        )
        jrpc_rules_if.add_rule(self.__gs_1_id, rule_cfg)
        a_slots = rule_models.AvailabilityRule.objects.get_availability_slots(
            self.__gs
        )

        self.assertEqual(len(a_slots), 1)

        db_a_slots = availability.AvailabilitySlot.objects.all()
        self.assertEqual(len(db_a_slots), 1)
        self.assertEquals(
            model_to_dict(
                db_a_slots[0], exclude=['id', 'groundstation', 'identifier']
            ), {
                'start': self.__rule_s_time, 'end': self.__rule_e_time
            }
        )

    def _test_1b_add_slots_once_rule(self):
        """INTR test: services.scheduling - add slots w/single ONCE rule (1B)
        This method tests the addition of new availability slots when there
        is only a single applicable ONCE-type rule in the database.
        Therefore, a single slot should be generated and added to the database.
        """
        if self.__verbose_testing:
            print('##### test_add_slots (B): single once rule (ADD and DEL)')

        jrpc_rules_if.add_rule(
            self.__gs_1_id,
            db_tools.create_jrpc_once_rule(
                starting_time=self.__rule_s_time, ending_time=self.__rule_e_time
            )
        )

        a_slots = rule_models.AvailabilityRule.objects.get_availability_slots(
            self.__gs
        )
        self.assertEqual(len(a_slots), 1)

        db_a_slots = availability.AvailabilitySlot.objects.all()
        self.assertEqual(len(db_a_slots), 1)
        self.assertEquals(
            model_to_dict(
                db_a_slots[0], exclude=['id', 'groundstation', 'identifier']
            ), {
                'start': self.__rule_s_time,
                'end': self.__rule_e_time
            }
        )

        jrpc_rules_if.add_rule(
            self.__gs_1_id,
            db_tools.create_jrpc_once_rule(
                operation=jrpc_rules_if.rule_serializers.RULE_OP_REMOVE,
                starting_time=self.__rule_s_time,
                ending_time=self.__rule_e_time
            )
        )

        self.assertListEqual(
            rule_models.AvailabilityRule.objects.get_availability_slots(
                self.__gs
            ),
            []
        )

        db_a_slots = availability.AvailabilitySlot.objects.all()
        self.assertEquals(len(db_a_slots), 0)

    def _test_1c_add_slots_once_rule(self):
        """INTR test: services.scheduling - add slots w/single ONCE rule (1C)
        This method tests the addition of new availability slots when there
        is only a single applicable ONCE-type rule in the database.
        Therefore, a single slot should be generated and added to the database.
        """
        if self.__verbose_testing:
            print('##### test_add_slots (C): single once rule (ADD), GSx2')

        jrpc_rules_if.add_rule(
            self.__gs_1_id,
            db_tools.create_jrpc_once_rule(
                starting_time=self.__rule_s_time,
                ending_time=self.__rule_e_time
            )
        )

        a_slots = rule_models.AvailabilityRule.objects.get_availability_slots(
            self.__gs
        )
        self.assertEqual(len(a_slots), 1)

        db_a_slots = availability.AvailabilitySlot.objects.all()
        self.assertEqual(len(db_a_slots), 1)
        self.assertEquals(
            model_to_dict(
                db_a_slots[0], exclude=['id', 'groundstation', 'identifier']
            ), {
                'start': self.__rule_s_time,
                'end': self.__rule_e_time
            }
        )

        self.assertEquals(len(rule_models.AvailabilityRule.objects.all()), 1)
        jrpc_rules_if.add_rule(
            self.__gs_2_id,
            db_tools.create_jrpc_once_rule(
                starting_time=self.__rule_s_time,
                ending_time=self.__rule_e_time
            )
        )
        self.assertEquals(len(rule_models.AvailabilityRule.objects.all()), 2)

        a_slots = rule_models.AvailabilityRule.objects.get_availability_slots(
            self.__gs_2
        )
        self.assertEqual(len(a_slots), 1)

        db_a_slots = availability.AvailabilitySlot.objects.all()
        self.assertEqual(len(db_a_slots), 2)
        self.assertEquals(
            model_to_dict(
                db_a_slots[0], exclude=['id', 'groundstation', 'identifier']
            ), {
                'start': self.__rule_s_time,
                'end': self.__rule_e_time
            }
        )
        self.assertEquals(
            model_to_dict(
                db_a_slots[1], exclude=['id', 'groundstation', 'identifier']
            ), {
                'start': self.__rule_s_time,
                'end': self.__rule_e_time
            }
        )

    def _test_2_generate_slots_daily_rule(self):
        """INTR test: services.scheduling - add slots with a DAILY rule (2)
        Tests the generation of slots for a given daily rule.
        """
        if self.__verbose_testing:
            print('##### test_generate_slots_daily_rule')

        jrpc_rules_if.add_rule(
            self.__gs_1_id,
            db_tools.create_jrpc_daily_rule(
                date_i=self.__utc_s_date,
                date_f=self.__utc_e_date,
                starting_time=self.__utc_s_time,
                ending_time=self.__utc_e_time
            )
        )

        a_slots = rule_models.AvailabilityRule.objects.get_availability_slots(
            self.__gs
        )

        self.assertEqual(len(a_slots), 3)
        db_a_slots = availability.AvailabilitySlot.objects.all()
        self.assertEqual(len(db_a_slots), 3)

        self.assertEquals(
            model_to_dict(
                db_a_slots[0], exclude=['id', 'groundstation', 'identifier']
            ), {
                'start': self.__rule_s_time,
                'end': self.__rule_e_time
            }
        )

        self.assertEquals(
            model_to_dict(
                db_a_slots[1], exclude=['id', 'groundstation', 'identifier']
            ), {
                'start': self.__rule_s_time + datetime.timedelta(days=1),
                'end': self.__rule_e_time + datetime.timedelta(days=1)
            }
        )

    def _test_3_generate_slots_several_rules_1(self):
        """INTR test: services.scheduling - add slots with several rules (3)
        This method tests the addition of new availability slots when there
        are several availability rules in the database.
        """
        if self.__verbose_testing:
            print('##### test_add_slots: several rules (1)')

        # R1) ADD+ONCE (+1 slot)
        rule_1_id = jrpc_rules_if.add_rule(
            self.__gs_1_id,
            db_tools.create_jrpc_once_rule(
                starting_time=self.__rule_s_time, ending_time=self.__rule_e_time
            )
        )
        a_slots = rule_models.AvailabilityRule.objects.get_availability_slots(
            self.__gs
        )
        self.assertEqual(
            len(a_slots), 1, 'Only 1 slot expected, got = ' + str(len(a_slots))
        )
        av_slots = availability.AvailabilitySlot.objects.all()
        self.assertEqual(
            len(av_slots), 1, '1 slot expected, got = ' + str(len(av_slots))
        )

        if self.__verbose_testing:
            misc.print_list(
                rule_models.AvailabilityRule.objects.all(), name='RULES@1'
            )
            misc.print_list(av_slots, name='AVAILABLE@1')

        # R2) ADD+DAILY (+2 slots)
        rule_2_id = jrpc_rules_if.add_rule(
            self.__gs_1_id,
            db_tools.create_jrpc_daily_rule(
                date_i=self.__utc_s_date,
                date_f=self.__utc_e_date,
                starting_time=self.__utc_s_time,
                ending_time=self.__utc_e_time
            )
        )

        a_slots = rule_models.AvailabilityRule.objects.get_availability_slots(
            self.__gs
        )
        av_slots = availability.AvailabilitySlot.objects.all()

        if self.__verbose_testing:
            print('>>> today_utc = ' + str(misc.get_today_utc()))
            print('>>> window = ' + str(
                simulation.OrbitalSimulator.get_simulation_window()
            ))
            misc.print_list(
                rule_models.AvailabilityRule.objects.all(), name='RULES@2'
            )
            misc.print_list(av_slots, name='AVAILABLE@2')

        expected_slots = 3
        self.assertEqual(len(a_slots), expected_slots)
        self.assertEqual(len(av_slots), expected_slots)

        # R3) ADD-ONCE (-1 slot)
        rule_3_id = jrpc_rules_if.add_rule(
            self.__gs_1_id,
            db_tools.create_jrpc_once_rule(
                operation=jrpc_serial.RULE_OP_REMOVE,
                starting_time=self.__rule_s_time, ending_time=self.__rule_e_time
            )
        )

        a_slots = rule_models.AvailabilityRule.objects.get_availability_slots(
            self.__gs
        )
        av_slots = availability.AvailabilitySlot.objects.all()

        if self.__verbose_testing:
            print('>>> today_utc = ' + str(misc.get_today_utc()))
            print('>>> window = ' + str(
                simulation.OrbitalSimulator.get_simulation_window()
            ))
            misc.print_list(
                rule_models.AvailabilityRule.objects.all(), name='RULES@3'
            )
            misc.print_list(av_slots, name='AVAILABLE@3')

        expected_slots = 2
        self.assertEqual(len(a_slots), expected_slots)
        self.assertEqual(len(av_slots), expected_slots)

        # R4) ADD-DAILY (-7 slots)
        rule_4_id = jrpc_rules_if.add_rule(
            self.__gs_1_id,
            db_tools.create_jrpc_daily_rule(
                operation=jrpc_serial.RULE_OP_REMOVE,
                date_i=self.__utc_s_date,
                date_f=self.__utc_e_date,
                starting_time=self.__utc_s_time,
                ending_time=self.__utc_e_time
            )
        )

        a_slots = rule_models.AvailabilityRule.objects.get_availability_slots(
            self.__gs
        )
        av_slots = availability.AvailabilitySlot.objects.all()

        if self.__verbose_testing:
            print('>>> today_utc = ' + str(misc.get_today_utc()))
            print('>>> window = ' + str(
                simulation.OrbitalSimulator.get_simulation_window()
            ))
            misc.print_list(
                rule_models.AvailabilityRule.objects.all(), name='RULES@4'
            )
            misc.print_list(av_slots, name='AVAILABLE@4')

        expected = 0
        self.assertEqual(len(a_slots), expected)
        self.assertEqual(len(av_slots), expected)

        # REMOVE R#4 (+6 slots)
        jrpc_rules_if.remove_rule(
            groundstation_id=self.__gs_1_id,
            rule_id=rule_4_id
        )

        a_slots = rule_models.AvailabilityRule.objects.get_availability_slots(
            self.__gs
        )
        av_slots = availability.AvailabilitySlot.objects.all()

        if self.__verbose_testing:
            print('>>> today_utc = ' + str(misc.get_today_utc()))
            print('>>> window = ' + str(
                simulation.OrbitalSimulator.get_simulation_window()
            ))
            misc.print_list(
                rule_models.AvailabilityRule.objects.all(), name='RULES@5'
            )
            misc.print_list(av_slots, name='AVAILABLE@5')

        expected = 2
        self.assertEqual(len(a_slots), expected)
        self.assertEqual(len(av_slots), expected)

        # REMOVE R#3 (+1 slot)
        jrpc_rules_if.remove_rule(
            groundstation_id=self.__gs_1_id,
            rule_id=rule_3_id
        )

        a_slots = rule_models.AvailabilityRule.objects.get_availability_slots(
            self.__gs
        )
        av_slots = availability.AvailabilitySlot.objects.all()

        if self.__verbose_testing:
            print('>>> today_utc = ' + str(misc.get_today_utc()))
            print('>>> window = ' + str(
                simulation.OrbitalSimulator.get_simulation_window()
            ))
            misc.print_list(
                rule_models.AvailabilityRule.objects.all(), name='RULES@6'
            )
            misc.print_list(av_slots, name='AVAILABLE@6')

        expected = 3
        self.assertEqual(len(a_slots), expected)
        self.assertEqual(len(av_slots), expected)

        # REMOVE R#2 (-7 slots)
        jrpc_rules_if.remove_rule(
            groundstation_id=self.__gs_1_id,
            rule_id=rule_2_id
        )
        a_slots = rule_models.AvailabilityRule.objects.get_availability_slots(
            self.__gs
        )
        self.assertEqual(len(a_slots), 1)
        av_slots = availability.AvailabilitySlot.objects.all()
        self.assertEqual(len(av_slots), 1)

        if self.__verbose_testing:
            misc.print_list(
                rule_models.AvailabilityRule.objects.all(), name='RULES@7'
            )
            misc.print_list(av_slots, name='AVAILABLE@7')

        # REMOVE R#1 (-1 slot)
        jrpc_rules_if.remove_rule(
            groundstation_id=self.__gs_1_id,
            rule_id=rule_1_id
        )
        a_slots = rule_models.AvailabilityRule.objects.get_availability_slots(
            self.__gs
        )
        self.assertEqual(len(a_slots), 0)
        av_slots = availability.AvailabilitySlot.objects.all()
        self.assertEqual(len(av_slots), 0)

        if self.__verbose_testing:
            misc.print_list(
                rule_models.AvailabilityRule.objects.all(), name='RULES@8'
            )
            misc.print_list(av_slots, name='AVAILABLE@8')

        self.__verbose_testing = False

    def _test_4_get_availability_slots(self):
        """INTR test: services.scheduling - availability slot generation (4)
        Validates the method that gathers the AvailabilitySlots that are
        applicable within a defined interval.
        """
        if self.__verbose_testing:
            print('##### test_get_availability_slots:')

        # 0) Stability with None...
        self.assertEqual(
            availability.AvailabilitySlot.objects.get_applicable(None), [],
            '[] should be the result!'
        )
        # 1) Stability with []...
        self.assertEqual(
            availability.AvailabilitySlot.objects.get_applicable(
                groundstation=self.__gs,
            ), [],
            '[] should be the result!'
        )

        # 2) Single daily rule, adds availability slots...
        jrpc_rules_if.add_rule(
            self.__gs_1_id,
            db_tools.create_jrpc_daily_rule(
                date_i=self.__utc_s_date,
                date_f=self.__utc_e_date,
                starting_time=self.__utc_s_time,
                ending_time=self.__utc_e_time
            )
        )

        a_slots = list(
            availability.AvailabilitySlot.objects.values_list(
                'start', 'end'
            )
        )
        # ### the identifier is included as it is obtained from the actual
        # ### execution of the method
        x_slots = [
            (
                self.__rule_s_time,
                self.__rule_e_time
            ),
            (
                self.__rule_s_time + datetime.timedelta(days=1),
                self.__rule_e_time + datetime.timedelta(days=1)
            ),
            (
                self.__rule_s_time + datetime.timedelta(days=2),
                self.__rule_e_time + datetime.timedelta(days=2)
            )
        ]

        if self.__verbose_testing:
            print('>>> window = ' + str(
                simulation.OrbitalSimulator.get_simulation_window()
            ))
            misc.print_list(
                rule_models.AvailabilityRule.objects.all(), name='RULES@1'
            )
            misc.print_list(a_slots, name='AVAILABLE@1')

        self.assertEqual(a_slots, x_slots)

        # 3) Period ending in the middle of an AvailabilitySlot, should
        # return the applicable half of that slot...
        a_slots = availability.AvailabilitySlot.objects.get_applicable(
            groundstation=self.__gs,
            start=self.__rule_s_time,
            end=self.__rule_s_time + datetime.timedelta(hours=3)
        )
        x_slots = [
            (
                self.__rule_s_time,
                self.__rule_s_time + datetime.timedelta(hours=3),
                a_slots[0][2]
            )
        ]

        if self.__verbose_testing:
            print('>>> window = ' + str(
                simulation.OrbitalSimulator.get_simulation_window()
            ))
            misc.print_list(x_slots, name='XSLOTS@2')
            misc.print_list(a_slots, name='AVAILABLE@2')

        self.assertEqual(a_slots, x_slots)

        # 4) Period starting in the middle of an AvailabilitySlot, should
        # return the applicable half of that slot...
        a_slots = availability.AvailabilitySlot.objects.get_applicable(
            groundstation=self.__gs,
            start=self.__rule_s_time + datetime.timedelta(hours=2),
            end=self.__rule_s_time + datetime.timedelta(hours=8)
        )
        x_slots = [(
            (
                self.__rule_s_time + datetime.timedelta(hours=2),
                self.__rule_s_time + datetime.timedelta(hours=5),
                a_slots[0][2]
            )
        )]
        self.assertEqual(a_slots, x_slots)

        # 5) Period starting after an AvailabilitySlot, should not return any
        #  slot at all...
        a_slots = availability.AvailabilitySlot.objects.get_applicable(
            groundstation=self.__gs,
            start=self.__rule_s_time + datetime.timedelta(hours=8),
            end=self.__rule_s_time + datetime.timedelta(hours=10)
        )
        self.assertEqual(a_slots, [])

        # 6) Period starting JUST after an AvailabilitySlot, should not return
        #  any slot at all...
        a_slots = availability.AvailabilitySlot.objects.get_applicable(
            groundstation=self.__gs,
            start=self.__rule_s_time + datetime.timedelta(hours=5),
            end=self.__rule_s_time + datetime.timedelta(hours=8)
        )
        self.assertEqual(a_slots, [])

        # 7) Period starting after an AvailabilitySlot, should not return any
        #  slot at all...
        a_slots = availability.AvailabilitySlot.objects.get_applicable(
            groundstation=self.__gs,
            start=self.__rule_s_time + datetime.timedelta(hours=7),
            end=self.__rule_s_time + datetime.timedelta(hours=8)
        )
        self.assertEqual(a_slots, [])

        # 8) Period starting JUST before an AvailabilitySlot, should not return
        #  any slot at all...
        a_slots = availability.AvailabilitySlot.objects.get_applicable(
            groundstation=self.__gs,
            start=self.__rule_s_time - datetime.timedelta(hours=2),
            end=self.__rule_s_time - datetime.timedelta(hours=1)
        )
        self.assertEqual(a_slots, [])

    def test_california_rule(self):
        """INTR test: services.scheduling - California rule
        This test is intended to validate the generation of availability slots
        whenever an Availability rule whose ending time extends to the
        following day is added to the system.
        MISC: this happens pretty usually when you add a rule with the
        California local timezone that, therefore, gets translated into a
        rule with an UTC starting date of today and an UTC ending date of
        tomorrow.
        """
        if self.__verbose_testing:
            print('##### test_california_rule:')

        s_time = misc.get_next_midnight() - datetime.timedelta(hours=10)
        e_time = misc.get_next_midnight() + datetime.timedelta(hours=4)

        # 1) Single once rule
        jrpc_rules_if.add_rule(
            self.__gs_1_id, {
                jrpc_serial.RULE_OP: jrpc_serial.RULE_OP_ADD,
                jrpc_serial.RULE_PERIODICITY: jrpc_serial.RULE_PERIODICITY_ONCE,
                jrpc_serial.RULE_DATES: {
                    jrpc_serial.RULE_ONCE_S_TIME: s_time.isoformat(),
                    jrpc_serial.RULE_ONCE_E_TIME: e_time.isoformat()
                },
            }
        )

        # 2) Generated Availability Slots
        self.assertEquals(
            availability.AvailabilitySlot.objects.values_list(
                'start', 'end'
            )[0],
            (s_time, e_time)
        )
