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

from datetime import timedelta as py_timedelta
import logging
from django import test
from django.db.models import signals as django_signals

from services.common import misc as sn_misc
from services.common import helpers as sn_helpers
from services.configuration.jrpc.views import rules as rule_jrpc
from services.configuration.models import rules as rule_models
from services.scheduling.signals import availability as availability_signals


class TestRulesAvailability(test.TestCase):
    """
    Test class for the channel model testing process. It helps in managing the
    required testing database.
    """

    def setUp(self):
        """
        Populates the initial database with a set of objects required to run
        the following tests.
        """
        self.__verbose_testing = False

        if not self.__verbose_testing:
            logging.getLogger('configuration').setLevel(level=logging.CRITICAL)
            logging.getLogger('simulation').setLevel(level=logging.CRITICAL)

        self.__gs_1_id = 'gs-castrelos'
        self.__gs_1_ch_1_id = 'chan-cas-1'

        self.__sc_1_id = 'sc-xatcobeo'
        self.__sc_1_ch_1_id = 'xatco-fm-1'
        self.__sc_1_ch_2_id = 'xatco-fm-2'
        self.__sc_1_ch_3_id = 'xatco-fm-3'
        self.__sc_1_ch_4_id = 'xatco-afsk-1'

        self.__band = sn_helpers.create_band()
        self.__test_user_profile = sn_helpers.create_user_profile()
        self.__gs = sn_helpers.create_gs(
            user_profile=self.__test_user_profile, identifier=self.__gs_1_id,
        )
        self.__sc = sn_helpers.create_sc(
            user_profile=self.__test_user_profile, identifier=self.__sc_1_id
        )

    def test_generate_slots_daily_rule(self):
        """UNIT test: services.configuration.models.rules - DAILY slots
        This test validates that a DAILY rule generates the right amount of
        slots depending on the interval relation with the start/end moments of
        the rule itself.
        """
        if self.__verbose_testing:
            print('>>> test_generate_slots_once_rule:')

        #######################################################################
        # ### XXXX SIGNAL DISCONNECTED
        django_signals.post_save.disconnect(
            availability_signals.daily_rule_saved,
            sender=rule_models.AvailabilityRuleDaily
        )

        #######################################################################
        # ### 1) rule starts ends interval, no slot the first day
        rule_id = rule_jrpc.add_rule(
            self.__gs_1_id,
            sn_helpers.create_jrpc_daily_rule(
                starting_time=sn_misc.get_next_midnight() + py_timedelta(
                    hours=2
                ),
                ending_time=sn_misc.get_next_midnight() + py_timedelta(
                    hours=3
                )
            )
        )

        rule_db_values = rule_models.AvailabilityRule.objects.filter(
            pk=rule_id
        ).values()

        interval = (
            sn_misc.get_next_midnight() + py_timedelta(days=300, hours=4),
            sn_misc.get_next_midnight() + py_timedelta(days=303)
        )

        print('>>> interval = ' + str(interval))
        slots = rule_models.AvailabilityRuleManager\
            .generate_available_slots_daily(
                rule_db_values[0], interval=interval
            )
        sn_misc.print_list(slots, name='SLOTS')

        expected = [
            (
                sn_misc.get_next_midnight() + py_timedelta(days=301, hours=2),
                sn_misc.get_next_midnight() + py_timedelta(days=301, hours=3)
            ),
            (
                sn_misc.get_next_midnight() + py_timedelta(days=302, hours=2),
                sn_misc.get_next_midnight() + py_timedelta(days=302, hours=3)
            ),
        ]

        sn_misc.print_list(slots, name='EXPECTED')

        self.assertListEqual(slots, expected)

        #######################################################################
        # ### 2) rule starts before interval, ends within,
        #           first day slot truncated
        rule_id = rule_jrpc.add_rule(
            self.__gs_1_id,
            sn_helpers.create_jrpc_daily_rule(
                starting_time=sn_misc.get_next_midnight() + py_timedelta(
                    hours=2
                ),
                ending_time=sn_misc.get_next_midnight() + py_timedelta(
                    hours=6
                )
            )
        )

        rule_db_values = rule_models.AvailabilityRule.objects.filter(
            pk=rule_id
        ).values()

        interval = (
            sn_misc.get_next_midnight() + py_timedelta(days=300, hours=4),
            sn_misc.get_next_midnight() + py_timedelta(days=303)
        )

        print('>>> interval = ' + str(interval))
        slots = rule_models.AvailabilityRuleManager\
            .generate_available_slots_daily(
                rule_db_values[0], interval=interval
            )
        sn_misc.print_list(slots, name='SLOTS')

        expected = [
            (
                sn_misc.get_next_midnight() + py_timedelta(days=300, hours=4),
                sn_misc.get_next_midnight() + py_timedelta(days=300, hours=6)
            ),
            (
                sn_misc.get_next_midnight() + py_timedelta(days=301, hours=2),
                sn_misc.get_next_midnight() + py_timedelta(days=301, hours=6)
            ),
            (
                sn_misc.get_next_midnight() + py_timedelta(days=302, hours=2),
                sn_misc.get_next_midnight() + py_timedelta(days=302, hours=6)
            ),
        ]

        sn_misc.print_list(slots, name='EXPECTED')

        self.assertListEqual(slots, expected)

        #######################################################################
        # ### XXXX SIGNAL RECONNECTED
        django_signals.post_save.connect(
            availability_signals.daily_rule_saved,
            sender=rule_models.AvailabilityRuleDaily
        )

    def test_generate_slots_once_rule(self):
        """UNIT test: services.configuration.models.rules - ONCE slots
        This test validates that a ONCE rule generates the right amount of
        slots depending on the interval relation with the start/end moments of
        the rule itself.
        """
        if self.__verbose_testing:
            print('>>> test_generate_slots_once_rule:')

        #######################################################################
        # ### XXXX SIGNAL DISCONNECTED
        django_signals.post_save.disconnect(
            availability_signals.once_rule_saved,
            sender=rule_models.AvailabilityRuleOnce
        )

        #######################################################################
        # ### 1) rule after interval
        rule_1_id = rule_jrpc.add_rule(
            self.__gs_1_id,
            sn_helpers.create_jrpc_once_rule(
                starting_time=sn_misc.get_next_midnight(),
                ending_time=sn_misc.get_next_midnight() + py_timedelta(hours=4)
            )
        )
        rule_1_db_values = rule_models.AvailabilityRule.objects.filter(
            pk=rule_1_id
        ).values()

        self.assertListEqual(
            rule_models.AvailabilityRuleManager.generate_available_slots_once(
                rule_1_db_values[0], (
                    sn_misc.get_next_midnight() - py_timedelta(hours=12),
                    sn_misc.get_next_midnight() - py_timedelta(hours=3)
                )
            ),
            []
        )

        self.assertTrue(rule_jrpc.remove_rule(self.__gs_1_id, rule_1_id))

        #######################################################################
        # ### 2) rule before interval

        rule_2_id = rule_jrpc.add_rule(
            self.__gs_1_id,
            sn_helpers.create_jrpc_once_rule(
                starting_time=sn_misc.get_next_midnight() - py_timedelta(
                    hours=6
                ),
                ending_time=sn_misc.get_next_midnight() - py_timedelta(
                    hours=4
                )
            )
        )
        rule_2_db_values = rule_models.AvailabilityRule.objects.filter(
            pk=rule_2_id
        ).values()

        self.assertListEqual(
            rule_models.AvailabilityRuleManager.generate_available_slots_once(
                rule_2_db_values[0], (
                    sn_misc.get_next_midnight(),
                    sn_misc.get_next_midnight() + py_timedelta(hours=9)
                )
            ),
            []
        )

        self.assertTrue(rule_jrpc.remove_rule(self.__gs_1_id, rule_2_id))

        #######################################################################
        # ### 3) rule FULLY inside interval

        rule_3_id = rule_jrpc.add_rule(
            self.__gs_1_id,
            sn_helpers.create_jrpc_once_rule(
                starting_time=sn_misc.get_next_midnight() + py_timedelta(
                    hours=2
                ),
                ending_time=sn_misc.get_next_midnight() + py_timedelta(
                    hours=4
                )
            )
        )
        rule_3_db_values = rule_models.AvailabilityRule.objects.filter(
            pk=rule_3_id
        ).values()

        self.assertListEqual(
            rule_models.AvailabilityRuleManager.generate_available_slots_once(
                rule_3_db_values[0], (
                    sn_misc.get_next_midnight(),
                    sn_misc.get_next_midnight() + py_timedelta(hours=9)
                )
            ), [(
                sn_misc.get_next_midnight() + py_timedelta(hours=2),
                sn_misc.get_next_midnight() + py_timedelta(hours=4)
            )]
        )

        self.assertTrue(rule_jrpc.remove_rule(self.__gs_1_id, rule_3_id))

        #######################################################################
        # ### 4) rule start before the interval

        rule_4_id = rule_jrpc.add_rule(
            self.__gs_1_id,
            sn_helpers.create_jrpc_once_rule(
                starting_time=sn_misc.get_next_midnight() - py_timedelta(
                    hours=1
                ),
                ending_time=sn_misc.get_next_midnight() + py_timedelta(
                    hours=4
                )
            )
        )
        rule_4_db_values = rule_models.AvailabilityRule.objects.filter(
            pk=rule_4_id
        ).values()

        self.assertListEqual(
            rule_models.AvailabilityRuleManager.generate_available_slots_once(
                rule_4_db_values[0], (
                    sn_misc.get_next_midnight(),
                    sn_misc.get_next_midnight() + py_timedelta(hours=9)
                )
            ), [(
                sn_misc.get_next_midnight(),
                sn_misc.get_next_midnight() + py_timedelta(hours=4)
            )]
        )

        self.assertTrue(rule_jrpc.remove_rule(self.__gs_1_id, rule_4_id))

        #######################################################################
        # ### 5) rule ends after the interval

        rule_5_id = rule_jrpc.add_rule(
            self.__gs_1_id,
            sn_helpers.create_jrpc_once_rule(
                starting_time=sn_misc.get_next_midnight() + py_timedelta(
                    hours=2
                ),
                ending_time=sn_misc.get_next_midnight() + py_timedelta(
                    hours=12
                )
            )
        )
        rule_5_db_values = rule_models.AvailabilityRule.objects.filter(
            pk=rule_5_id
        ).values()

        self.assertListEqual(
            rule_models.AvailabilityRuleManager.generate_available_slots_once(
                rule_5_db_values[0], (
                    sn_misc.get_next_midnight(),
                    sn_misc.get_next_midnight() + py_timedelta(hours=9)
                )
            ), [(
                sn_misc.get_next_midnight() + py_timedelta(hours=2),
                sn_misc.get_next_midnight() + py_timedelta(hours=9)
            )]
        )

        self.assertTrue(rule_jrpc.remove_rule(self.__gs_1_id, rule_5_id))

        #######################################################################
        # ### XXXX SIGNAL RECONNECTED
        django_signals.post_save.connect(
            availability_signals.once_rule_saved,
            sender=rule_models.AvailabilityRuleOnce
        )
