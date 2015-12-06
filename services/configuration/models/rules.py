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

import datetime
from django.db import models as django_models
from django.utils import timezone as django_tz
import logging
import pytz
from pytz import reference as pytz_ref

from services.common import misc, simulation, slots
from services.configuration.models import segments as segment_models
from website import settings as satnet_settings

logger = logging.getLogger('configuration')

ADD_SLOTS = '+'
REMOVE_SLOTS = '-'
# Definition of the types of periods supported
ONCE_PERIODICITY = 'O'
DAILY_PERIODICITY = 'D'
WEEKLY_PERIODICITY = 'W'

DEFAULT_GROUNDSTATION = 1


class AvailabilityRuleManager(django_models.Manager):
    """
    Manager that contains all the methods required for easing the access to
    the database AvailabilityRule objects.
    """
    __periodicity2class__ = {
        ONCE_PERIODICITY: 'AvailabilityRuleOnce',
        DAILY_PERIODICITY: 'AvailabilityRuleDaily',
        WEEKLY_PERIODICITY: 'AvailabilityRuleWeekly',
    }

    def create(self, groundstation, operation, periodicity, dates):
        """
        This method creates a new rule with the given parameters.
        :param groundstation: The groundstation that owns this rule
        :param operation: The type of operation for the rule to be added.
        :param periodicity: The periodicity for the rule.
        :param dates: The dates for the definition of the time intervales in
        accordance with the periodicity of the rule (ISO8601).
        :return: A reference to the object that holds the new rule.
        """
        if periodicity not in self.__periodicity2class__:
            raise Exception('Periodicity ' + periodicity + 'not supported.')

        db_obj_classname = self.__periodicity2class__[periodicity]
        db_obj_class = globals()[db_obj_classname]

        rule_child = db_obj_class.objects.create(
            groundstation, operation, periodicity, dates
        )

        # ### Generate availability slots and write them in the table.
        return AvailabilityRule.objects.get(
            id=rule_child.availabilityrule_ptr_id
        )

    @staticmethod
    def create_test_window():
        """
        Creates a window to use as a reference for testing.
        :return: Tuple with the start and end dates of the window
        """
        return (
            misc.get_today_utc(),
            misc.get_today_utc(
            ) + simulation.OrbitalSimulator.get_window_duration()
        )

    @staticmethod
    def get_specific_rule(rule_id):
        """
        Returns all the specific rules that inherit from this generic one.
        :param rule_id: Identifier of the generic rule.
        :returns: Specific object that inherits from this rule.
        """
        try:
            return AvailabilityRuleOnce.objects.get(pk=rule_id)
        except AvailabilityRuleOnce.DoesNotExist:
            try:
                return AvailabilityRuleDaily.objects.get(pk=rule_id)
            except AvailabilityRuleDaily.DoesNotExist:
                try:
                    return AvailabilityRuleWeekly.objects.get(pk=rule_id)
                except AvailabilityRuleWeekly.DoesNotExist:
                    raise Exception(
                        'Cannot find rule with id = ' + str(rule_id)
                    )

    @staticmethod
    def get_applicable_rule_values(groundstation, interval=None):
        """
        This method finds all applicable rules within the database whose
        initial_date and ending_date range within the given interval.
        :param groundstation: Ground station owning this rule
        :param interval: Duration of the interval for matching applicable
        rules. This is a tuple with the first value being the begin_date for
        the interval and the second (and last) object being the end_date for
        the interval.
        :returns: Two separate lists with all the applicable rules as objects
        read from the database directly, the first list contains the rules
        that add slots and the second one contains those that remove slots.
        """
        add_r = []
        remove_r = []

        if interval is None:
            interval = simulation.OrbitalSimulator.get_simulation_window()

        for c in AvailabilityRule.__subclasses__():

            r_list = list(
                c.objects.filter(
                    availabilityrule_ptr__groundstation=groundstation
                ).filter(
                    availabilityrule_ptr__operation=ADD_SLOTS
                ).filter(
                    availabilityrule_ptr__starting_date__lte=interval[1].date()
                ).filter(
                    availabilityrule_ptr__ending_date__gte=interval[0].date()
                ).values()
            )
            if r_list:
                add_r += r_list
            r_list = list(
                c.objects.filter(
                    availabilityrule_ptr__groundstation=groundstation
                ).filter(
                    availabilityrule_ptr__operation=REMOVE_SLOTS
                ).filter(
                    availabilityrule_ptr__starting_date__lte=interval[1].date()
                ).filter(
                    availabilityrule_ptr__ending_date__gte=interval[0].date()
                ).values()
            )
            if r_list:
                remove_r += r_list

        return add_r, remove_r

    @staticmethod
    def is_applicable(rule_values, interval):
        """
        This method checks whether this rule can generate slots for the given
        interval.
        :param rule_values: Values for this rule as obtained
        :param interval: The interval for the check.
        :returns: In case the interval is applicable, it returns a tuple with
        the initial and final datetime objects.
        """
        if interval is None:
            interval = simulation.OrbitalSimulator.get_simulation_window()

        print('XXXX 2')
        print('### HELLLLL: ' + str(rule_values.get('starting_time')))

        if rule_values.get('starting_time') > interval[1]:
            raise Exception('Not applicable to this interval [FUTURE].')
        if rule_values['ending_time'] < interval[0]:
            raise Exception('Not applicable to this interval [PAST].')

        return rule_values['starting_time'], rule_values['ending_time']

    @staticmethod
    def generate_available_slots_once(rule_values, interval=None):
        """
        This method generates the available slots for a only-once rule that
        starts and ends in the given dates, during the specified interval.
        :param interval: Interval of applicability
        :param rule_values: The values for the ONCE availability rule
        """
        if interval is None:
            interval = simulation.OrbitalSimulator.get_simulation_window()

        r = AvailabilityRuleOnce.objects.get(
            availabilityrule_ptr=rule_values['availabilityrule_ptr_id']
        )

        if r.starting_time < interval[0]:
            r.starting_time = interval[0]
        if r.ending_time > interval[1]:
            r.ending_time = interval[1]

        return [(r.starting_time, r.ending_time)]

    @staticmethod
    def generate_available_slots_daily(rule_values, interval=None):
        """
        This method generates the available slots for a daily rule that
        starts and ends in the given dates, during the specified interval.
        :param interval: Interval of applicability
        :param rule_values: The values for the ONCE availability rule
        """
        if interval is None:
            interval = simulation.OrbitalSimulator.get_simulation_window()

        print('@@@ generate_available_slots_daily.interval = ' + str(interval))
        print('@@@  OrbitalSimulator.get_simulation_window = ' + str(
            simulation.OrbitalSimulator.get_simulation_window()
        ))

        first = True
        r = AvailabilityRuleDaily.objects.get(
            availabilityrule_ptr=rule_values['availabilityrule_ptr_id']
        )
        result = []
        rule_starting_dt = misc.localize_date_utc(rule_values['starting_date'])

        if rule_starting_dt > interval[0]:
            i_day = rule_starting_dt
        else:
            i_day = interval[0]

        ii_time = r.starting_time.timetz()
        ff_time = r.ending_time.timetz()

        while i_day < interval[1]:

            slot_s = datetime.datetime.combine(i_day, ii_time)
            slot_e = datetime.datetime.combine(i_day, ff_time)

            # We might have to truncate the first slot...
            if first:
                first = False

                if slot_e <= interval[0]:
                    i_day += datetime.timedelta(days=1)
                    continue

                if slot_s <= interval[0]:
                    slot_s = interval[0]

            result.append((slot_s, slot_e))
            i_day += datetime.timedelta(days=1)

        return result

    # noinspection PyUnusedLocal
    @staticmethod
    def generate_available_slots_weekly(i_date, f_date, rule_values, interval):
        """
        This method generates the available slots for a weekly rule that
        starts and ends in the given dates, during the specified interval.
        TODO :: implement this weekly method for convenience.
        :param i_date: Starting date
        :param f_date: Finish date
        :param interval: Interval of applicability
        :param rule_values: The values for the ONCE availability rule
        """
        logger.warn('generate_available_slots_weekly: still not implemented')
        return []

    @staticmethod
    def generate_available_slots(r_values, interval=None):
        """
        This method generates the available slots defined by this rule.
        :param interval: Interval of applicability
        :param r_values: The values for the ONCE availability rule
        :return: Initial slots array, initial datetime and final datetime.
        """
        if interval is None:
            interval = simulation.OrbitalSimulator.get_simulation_window()

        i_date, f_date = AvailabilityRuleManager.is_applicable(
            r_values, interval
        )

        periodicity = r_values['periodicity']

        if periodicity == ONCE_PERIODICITY:
            return AvailabilityRuleManager.generate_available_slots_once(
                r_values, interval
            )
        if periodicity == DAILY_PERIODICITY:
            return AvailabilityRuleManager.generate_available_slots_daily(
                r_values, interval
            )
        if periodicity == WEEKLY_PERIODICITY:
            return AvailabilityRuleManager.generate_available_slots_weekly(
                i_date, f_date, r_values, interval
            )

        raise Exception(
            'Rule periodicity = <' + periodicity + '> is not supported'
        )

    @staticmethod
    def get_availability_slots(groundstation, interval=None):
        """
        This method generates the availability slots for this set of rules.
        :param groundstation; Reference to the ground station
        :param interval: Time interval for slot generation
        """
        if interval is None:
            if satnet_settings.TESTING:
                interval = AvailabilityRuleManager.create_test_window()
            else:
                interval = simulation.OrbitalSimulator.get_simulation_window()

        print('### @get_availability_slots.interval = ' + str(interval))
        print('### @OrbitalSimulator.get_simulation_window = ' + str(
            simulation.OrbitalSimulator.get_simulation_window()
        ))

        add_rules, remove_rules = AvailabilityRuleManager\
            .get_applicable_rule_values(groundstation, interval=interval)

        # 0) We obtain the applicable slots from the database
        add_slots = []
        for r in add_rules:
            add_slots += AvailabilityRuleManager.generate_available_slots(
                r, interval=interval
            )

        remove_slots = []
        for r in remove_rules:
            remove_slots += AvailabilityRuleManager.generate_available_slots(
                r, interval=interval
            )

        # 1) First, raw slots must be sorted and normalized.
        add_slots = slots.normalize_slots(
            sorted(add_slots, key=lambda s: s[1])
        )
        remove_slots = slots.normalize_slots(
            sorted(remove_slots, key=lambda s: s[0])
        )

        # 2) Sorted and normalized slots can be merged to generated the final
        # availability slots.
        results = slots.merge_slots(add_slots, remove_slots)

        misc.print_list(results, name='@@@ get_availability_slots.results')

        return results


class AvailabilityRule(django_models.Model):
    """
    This model permits the definition of a rule for the definition of the
    available slots for a given Ground Station.

    An availability rule is defined as a periodically repeated ammount of
    time, with an operation associated. This way, users can manage the set of
    existing operation slots through the definition of new availability rules
    . These rules can either 'add' or 'remove' operation slots.

    This is the basic availability rule, that can be extended through specific
    availability rules classes. Some of them have already been included for
    this release of the software (see all classes in this file that extend this
    generic rule). Therefore, this class only defines the basic common aspects
    for all the availability rules, being those extensions the responsibles for
    the definition of the specific types of periods.
    """
    class Meta:
        app_label = 'configuration'
        ordering = ['id']

    objects = AvailabilityRuleManager()

    groundstation = django_models.ForeignKey(
        segment_models.GroundStation,
        verbose_name='Reference to the Ground Station that owns this rule',
        default=1
    )

    OPERATION_CHOICES = (
        (ADD_SLOTS, 'Operation for adding new slots'),
        (REMOVE_SLOTS, 'Operation for removing existing slots')
    )
    operation = django_models.CharField(
        'Rule operation', choices=OPERATION_CHOICES, max_length=1
    )

    PERIODICITY_CHOICES = (
        (ONCE_PERIODICITY, 'Rule that occurs only once.'),
        (DAILY_PERIODICITY, 'Rule that defines daily repetition pattern.'),
        (WEEKLY_PERIODICITY, 'Rule that defines a weekly repetition pattern.'),
    )
    periodicity = django_models.CharField(
        'Rule periodicity', choices=PERIODICITY_CHOICES, max_length=1
    )

    starting_date = django_models.DateField(
        'Starting date for the applicability period of the rule',
        default=django_tz.now, null=True
    )
    ending_date = django_models.DateField(
        'Ending date for the applicability period of the rule',
        default=django_tz.now, null=True
    )

    __operation2unicode__ = {
        ADD_SLOTS: '+',
        REMOVE_SLOTS: '-',
    }
    __periodicity2unicode__ = {
        ONCE_PERIODICITY: '(O)',
        DAILY_PERIODICITY: '(D)',
        WEEKLY_PERIODICITY: '(W)'
    }

    def __unicode__(self):
        """
        Unicode string representation of the contents of this object.
        """
        child = AvailabilityRule.objects.get_specific_rule(self.pk)

        result = self.__operation2unicode__[str(self.operation)]\
            + self.__periodicity2unicode__[str(self.periodicity)]\
            + ':' + str(self.starting_date)\
            + '>>' + str(self.ending_date)\
            + '_T_' + str(child)

        return result

    def __str__(self):
        """
        UTF-8 string representing this object.
        """
        return self.__unicode__()


class AvailabilityRuleOnceManager(django_models.Manager):
    """
    Manager with static methods for easing the handling of this kind of
    objects in the database.
    """

    def create(self, groundstation, operation, periodicity, dates):
        """
        This method creates a new object in the database.
        :param groundstation: reference to the ground station for the rule
        :param operation: type of operation (create or remove slots)
        :param periodicity: periodicity for the rule (once, daily, weekly)
        :param dates: applicability dates for the rule
        """
        localtime = pytz_ref.LocalTimezone()
        starting_tz = localtime.tzname(dates[0])
        ending_tz = localtime.tzname(dates[1])

        if starting_tz != ending_tz:
            raise ValueError(
                'Invalid ONCE rule, TZ differ: ' +
                '( starting_tz = ' + starting_tz +
                'ending_tz = ' + ending_tz + ' )'
            )

        starting_dt = dates[0].astimezone(pytz.utc)
        ending_dt = dates[1].astimezone(pytz.utc)

        if ending_dt <= starting_dt:
            raise ValueError(
                'Invalid ONCE rule, ending (' + ending_dt.isoformat() + ') ' +
                '<= starting (' + starting_dt.isoformat() + ')'
            )

        return super(AvailabilityRuleOnceManager, self).create(
            groundstation=groundstation,
            operation=operation,
            periodicity=periodicity,
            starting_date=starting_dt,
            ending_date=ending_dt,
            starting_time=starting_dt,
            ending_time=ending_dt
        )


class AvailabilityRuleOnce(AvailabilityRule):
    """
    This model describes the data necessary for describing an availability rule
    that defines an operation over the slots of a period that occurs only once.
    """
    class Meta:
        app_label = 'configuration'

    objects = AvailabilityRuleOnceManager()

    starting_time = django_models.DateTimeField(
        'Starting datetime for the rule', default=django_tz.now, null=True
    )
    ending_time = django_models.DateTimeField(
        'Ending datetime for the rule', default=django_tz.now, null=True
    )

    def __unicode__(self):
        """
        Unicode string representation of the contents of this object.
        """
        return str(self.starting_time) + '>>' + str(self.ending_time)

    def __str__(self):
        """
        Returns the string representation of this object.
        """
        return self.__unicode__()


class AvailabilityRuleDailyManager(django_models.Manager):
    """
    Manager with static methods for easing the handling of this kind of
    objects in the database.
    """

    def create(self, groundstation, operation, periodicity, dates):
        """
        This method creates a new object in the database.
        :param groundstation: reference to the ground station for the rule
        :param operation: type of operation (create or remove slots)
        :param periodicity: periodicity for the rule (once, daily, weekly)
        :param dates: applicability dates for the rule
        """
        localtime = pytz_ref.LocalTimezone()
        starting_date_tz = localtime.tzname(dates[0])
        ending_date_tz = localtime.tzname(dates[1])

        if starting_date_tz != ending_date_tz:
            raise ValueError(
                'Invalid DAILY rule, dates TZ differ: ' +
                '( starting_date_tz = ' + starting_date_tz +
                'ending_date_tz = ' + ending_date_tz + ' )'
            )

        starting_dt = dates[2].astimezone(pytz.utc)
        ending_dt = dates[3].astimezone(pytz.utc)
        diff_dt = ending_dt - starting_dt

        if diff_dt > datetime.timedelta(hours=24):
            raise ValueError(
                'Invalid DAILY rule, diff_dt = ' + str(diff_dt) + ' > 24 hours'
            )

        if ending_dt <= starting_dt:
            raise ValueError(
                'Invalid DAILY rule, ending (' + ending_dt.isoformat() + ') ' +
                '<= starting (' + starting_dt.isoformat() + ')'
            )

        return super(AvailabilityRuleDailyManager, self).create(
            groundstation=groundstation,
            operation=operation,
            periodicity=periodicity,
            starting_date=dates[0],
            ending_date=dates[1],
            starting_time=starting_dt,
            ending_time=ending_dt
        )


class AvailabilityRuleDaily(AvailabilityRule):
    """
    This model describes the data necessary for describing an availability
    rule that defines an operation over the slots of a period that occurs
    everyday, in between the defined starting and ending dates.
    """
    class Meta:
        app_label = 'configuration'

    objects = AvailabilityRuleDailyManager()

    starting_time = django_models.DateTimeField(
        'Starting time for the rule', default=django_tz.now, null=True
    )
    ending_time = django_models.DateTimeField(
        'Ending time for the rule', default=django_tz.now, null=True
    )

    def __unicode__(self):
        """
        Unicode string representation of the contents of this object.
        """
        return str(self.starting_time.isoformat()) + '>>' + str(
            self.ending_time.isoformat()
        )

    def __str__(self):
        """
        Returns the string representation of this object.
        """
        return self.__unicode__()


class AvailabilityRuleWeeklyManager(django_models.Manager):
    """
    Manager with static methods for easing the handling of this kind of
    objects in the database.
    """

    def create(self, groundstation, operation, periodicity, dates):
        """
        This method creates a new object in the database.
        :param groundstation: reference to the ground station for the rule
        :param operation: type of operation (create or remove slots)
        :param periodicity: periodicity for the rule (once, daily, weekly)
        :param dates: applicability dates for the rule
        """
        return super(AvailabilityRuleWeeklyManager, self).create(
            groundstation=groundstation,
            operation=operation,
            periodicity=periodicity,
            starting_date=dates[0],
            ending_date=dates[1],
            m_s_time=dates[2],
            m_e_time=dates[3],
            t_s_time=dates[4],
            t_e_time=dates[5],
            w_s_time=dates[6],
            w_e_time=dates[7],
            r_s_time=dates[8],
            r_e_time=dates[9],
            f_s_time=dates[10],
            f_e_time=dates[11],
            s_s_time=dates[12],
            s_e_time=dates[13],
            x_s_time=dates[14],
            x_e_time=dates[15]
        )


class AvailabilityRuleWeekly(AvailabilityRule):
    """
    This model describes the data necessary for describing an availability
    rule that defines an operation over the slots of a period that occurs
    within a weekly pattern, in between the defined starting and ending dates.
    This weekly pattern is described by the user, which has to provide the
    ammount of time that the GroundStation will be available for each day of
    the week.
    """
    class Meta:
        app_label = 'configuration'

    objects = AvailabilityRuleWeeklyManager()

    m_s_time = django_models.DateTimeField(
        'Start time on Monday', default=django_tz.now, null=True
    )
    m_e_time = django_models.DateTimeField(
        'End time on Monday', default=django_tz.now, null=True
    )
    t_s_time = django_models.DateTimeField(
        'Start time on Tuesday', default=django_tz.now, null=True
    )
    t_e_time = django_models.DateTimeField(
        'End time on Tuesday', default=django_tz.now, null=True
    )
    w_s_time = django_models.DateTimeField(
        'Start time on Wednesday', default=django_tz.now, null=True
    )
    w_e_time = django_models.DateTimeField(
        'End t on Wednesday', default=django_tz.now, null=True
    )
    r_s_time = django_models.DateTimeField(
        'Start time on Thursday', default=django_tz.now, null=True
    )
    r_e_time = django_models.DateTimeField(
        'End time on Thursday', default=django_tz.now, null=True
    )
    f_s_time = django_models.DateTimeField(
        'Start time on Friday', default=django_tz.now, null=True
    )
    f_e_time = django_models.DateTimeField(
        'End time on Friday', default=django_tz.now, null=True
    )
    s_s_time = django_models.DateTimeField(
        'Start time on Saturday', default=django_tz.now, null=True
    )
    s_e_time = django_models.DateTimeField(
        'End time on Saturday', default=django_tz.now, null=True
    )
    x_s_time = django_models.DateTimeField(
        'Start time on Sunday', default=django_tz.now, null=True
    )
    x_e_time = django_models.DateTimeField(
        'End time on Sunday', default=django_tz.now, null=True
    )

    def __unicode__(self):
        """
        Unicode string representation of the contents of this object.
        """
        return '<WEEKLY PATTERN>'

    def __str__(self):
        """
        Returns the string representation of this object.
        """
        return self.__unicode__()
