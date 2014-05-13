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

from django.db import models
from datetime import datetime, timedelta
import pytz
from dateutil import parser
from configuration.utils import define_interval

# Definition of the availability operation through rules over existing
# operational slots.
ADD_SLOTS = '+'
REMOVE_SLOTS = '-'
# Definition of the types of periods supported
ONCE_PERIODICITY = 'O'
DAILY_PERIODICITY = 'D'
WEEKLY_PERIODICITY = 'W'


class AvailabilityRuleManager(models.Manager):
    """
    Manager that contains all the methods required for easing the access to
    the database AvailabilityRule objects.
    """

    __periodicity2class__ = {
        ONCE_PERIODICITY: 'AvailabilityRuleOnce',
        DAILY_PERIODICITY: 'AvailabilityRuleDaily',
        WEEKLY_PERIODICITY: 'AvailabilityRuleWeekly',
    }

    def create(self, operation, periodicity, dates):
        """
        This method creates a new rule with the given parameters.
        :param operation: The type of operation for the rule to be added.

        :param periodicity: The periodicity for the rule.
        :param dates: The dates for the definition of the time intervales in
        accordance with the periodicity of the rule (ISO8601).
        :return: A reference to the object that holds the new rule.
        """
        if not periodicity in self.__periodicity2class__:
            raise Exception('Periodicity ' + periodicity + 'not supported.')

        db_obj_classname = self.__periodicity2class__[periodicity]
        db_obj_class = globals()[db_obj_classname]
        rule_child = db_obj_class.objects.create(operation, periodicity, dates)
        return AvailabilityRule.objects\
            .get(id=rule_child.availabilityrule_ptr_id)

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
                    raise Exception('Cannot find rule with id = '
                                    + str(rule_id))

    @staticmethod
    def get_applicable_rule_values(interval=define_interval()):
        """
        This method finds all applicable rules within the database whose
        initial_date and ending_date range within the given interval.
        :param interval: Duration of the interval for matching applicable
        rules. This is a tuple with the first value being the begin_date for
        the interval and the second (and last) object being the end_date for
        the interval.
        :returns: Two separate lists with all the applicable rules as objects
        read from the database directly, the first list contains the rules
        that add slots and the second one contains those that remove slots.
        """
        add_slots = []
        remove_slots = []

        for c in AvailabilityRule.__subclasses__():
            r_list = c.objects\
                .filter(availabilityrule_ptr__operation=ADD_SLOTS)\
                .filter(availabilityrule_ptr__starting_date__lt=interval[1])\
                .filter(availabilityrule_ptr__ending_date__gt=interval[0])\
                .values()
            if r_list:
                add_slots += r_list
            r_list = c.objects\
                .filter(availabilityrule_ptr__operation=REMOVE_SLOTS)\
                .filter(availabilityrule_ptr__starting_date__lt=interval[1])\
                .filter(availabilityrule_ptr__ending_date__gt=interval[0])\
                .values()
            if r_list:
                remove_slots += r_list

        return add_slots, remove_slots

    @staticmethod
    def merge_slots(raw_add_slots, raw_remove_slots,
                    purge_small_slots=True,
                    small_slot_duration=timedelta(minutes=1)):
        """
        This method merges the slots of type ADD with the slots of type REMOVE,
        creating the list of availability slots for a given Ground Station. In
        case one REMOVE-type slot partially "colides" with an ADD-type slot,
        the result will be one or more availability slots with the remaining
        time after computing the effects of the colision.

        :param raw_add_slots: List with the slots of type ADD.
        :param raw_remove_slots: List with the slots of type REMOVE.
        :param purge_small_slots=true: Flag that provokes this algorithm to
                purge any of the resulting slots whose duration is inferior to
                the value of the parameter 'small_slot_duration'.
        :param small_slot_duration=timedelta(minutes=1): All slots whose
                duration is below the value of this parameter will be purged
                if the flag 'purge_small_slots' is activated.
        :return: List with the resulting availability slots for a given Ground
                Station.
        """
        final_slots = []
        a = raw_add_slots[0]
        r = raw_remove_slots[0]
        #for a in raw_add_slots:
        #    if
        return final_slots

    @staticmethod
    def get_availability_slots(interval):
        """
        This method generates the availability slots for this set of rules.
        :param interval:
        """
        add_rules, remove_rules = AvailabilityRuleManager\
            .get_applicable_rule_values(interval=interval)

        raw_add_slots = []
        raw_remove_slots = []

        for r in add_rules:
            raw_add_slots = AvailabilityRuleManager\
                .generate_available_slots(r, interval=interval)
        for r in remove_rules:
            raw_remove_slots += AvailabilityRuleManager\
                .generate_available_slots(r, interval=interval)

        raw_add_slots = sorted(raw_add_slots, key=lambda s: s[1])
        raw_remove_slots = sorted(raw_remove_slots, key=lambda s: s[0])

        raw_slots = AvailabilityRuleManager\
            .merge_slots(raw_add_slots, raw_remove_slots)

        return raw_slots

    @staticmethod
    def is_applicable(rule_values, interval=define_interval(days=14)):
        """
        This method checks whether this rule can generate slots for the given
        interval.
        :param interval: The interval for the check.
        :returns: In case the interval is applicable, it returns a tuple with
        the initial and final datetime objects.
        """

        i_date = pytz.utc\
            .localize(datetime
                      .combine(rule_values['starting_date'],
                               rule_values['starting_time']))
        f_date = pytz.utc\
            .localize(datetime
                      .combine(rule_values['ending_date'],
                               rule_values['ending_time']))

        print 'interval = ' + str(interval)
        print 'i_date = ' + str(i_date)
        print 'f_date = ' + str(f_date)

        if i_date > interval[1]:
            raise Exception('Not applicable to this interval [FUTURE].')
        if f_date < interval[0]:
            raise Exception('Not applicable to this interval [PAST].')

        return i_date, f_date

    @staticmethod
    def generate_available_slots_once(date, rule_values, interval):
        """
        This method generates the available slots for a only-once rule that
        starts and ends in the given dates, during the specified interval.
        """
        r = AvailabilityRuleOnce.objects\
            .get(availabilityrule_ptr=rule_values['availabilityrule_ptr_id'])

        return [(pytz.utc.localize(datetime
                 .combine(rule_values['starting_date'], r.starting_time)),
                pytz.utc.localize(datetime
                 .combine(rule_values['ending_date'], r.ending_time)))]

    @staticmethod
    def generate_available_slots_daily(i_date, f_date, rule_values, interval):
        """
        This method generates the available slots for a daily rule that
        starts and ends in the given dates, during the specified interval.
        """
        r = AvailabilityRuleDaily.objects\
            .get(availabilityrule_ptr=rule_values['availabilityrule_ptr_id'])
        days = (interval[1] - interval[0]).days
        slots = []
        i = 0

        while i < days:
            i_day = interval[0] + timedelta(days=i)
            i += 1
            ii_date = pytz.utc.localize(datetime
                                        .combine(i_day, r.starting_time))
            ff_date = pytz.utc.localize(datetime
                                        .combine(i_day, r.ending_time))
            slots.append((ii_date, ff_date))

        return slots

    @staticmethod
    def generate_available_slots_weekly(i_date, f_date, rule_values, interval):
        """
        This method generates the available slots for a weekly rule that
        starts and ends in the given dates, during the specified interval.
        TODO :: implement this weekly method for convenience.
        """
        pass

    @staticmethod
    def generate_available_slots(rule_values, interval):
        """
        This method generates the available slots defined by this rule.
        :param interval: The interval for the slots generation.
        :return: Initial slots array, initial datetime and final datetime.
        """
        print 'a'
        i_date, f_date = AvailabilityRuleManager\
            .is_applicable(rule_values, interval)
        print 'rule_values = ' + str(rule_values)

        op = rule_values['operation']
        periodicity = rule_values['periodicity']

        if periodicity == ONCE_PERIODICITY:
            return AvailabilityRuleManager\
                .generate_available_slots_once(i_date, rule_values, interval)
        if periodicity == DAILY_PERIODICITY:
            return AvailabilityRuleManager\
                .generate_available_slots_daily(i_date, f_date, rule_values,
                                                interval)
        if periodicity == WEEKLY_PERIODICITY:
            return AvailabilityRuleManager\
                .generate_available_slots_weekly(i_date, f_date, rule_values,
                                                 interval)

        raise Exception('Rule periodicity = <' + periodicity + '> is not '
                                                               'supported')


class AvailabilityRule(models.Model):
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

    objects = AvailabilityRuleManager()

    OPERATION_CHOICES = (
        (ADD_SLOTS, 'Operation for adding new slots'),
        (REMOVE_SLOTS, 'Operation for removing existing slots')
    )
    operation = models.CharField('Operation that this rule defines',
                                 choices=OPERATION_CHOICES,
                                 max_length=1)

    PERIODICITY_CHOICES = (
        (ONCE_PERIODICITY, 'Rule that occurs only once.'),
        (DAILY_PERIODICITY, 'Rule that defines a period of time that is going '
                            'to be repeated on a daily-basis pattern.'),
        (WEEKLY_PERIODICITY, 'Rule that defines a period of time that is '
                             'going to be repeated on a wekkly-basis.'),
    )
    periodicity = models.CharField('Period of time that this rule occurs.',
                                   choices=PERIODICITY_CHOICES, max_length=1)

    starting_date = models\
        .DateField('Starting date for an availability period')
    ending_date = models\
        .DateField('Ending date for an availability period')

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
        return self.__operation2unicode__[self.operation]\
            + self.__periodicity2unicode__[self.periodicity] + ':'\
            + str(self.starting_date) + '>>' + str(self.ending_date) + ':'\
            + str(child)


class AvailabilityRuleOnceManager(models.Manager):
    """
    Manager with static methods for easing the handling of this kind of
    objects in the database.
    """

    def create(self, operation, periodicity, dates):
        """
        This method creates a new object in the database.
        """
        rule_once = super(AvailabilityRuleOnceManager, self)\
            .create(operation=operation,
                    periodicity=periodicity,
                    starting_date=parser.parse(dates[0]),
                    ending_date=parser.parse(dates[0]),
                    starting_time=dates[1],
                    ending_time=dates[2])
        return rule_once


class AvailabilityRuleOnce(AvailabilityRule):
    """
    This model describes the data necessary for describing an availability
    rule that defines an operation over the slots of a period that occurs
    only once.
    """

    class Meta:
        app_label = 'configuration'

    objects = AvailabilityRuleOnceManager()

    starting_time = models.TimeField('Time at which this availability period '
                                     'starts.')
    ending_time = models.TimeField('Time at which this availability period '
                                   'ends.')

    def __unicode__(self):
        """
        Unicode string representation of the contents of this object.
        """
        return str(self.starting_time) + '>>' + str(self.ending_time)


class AvailabilityRuleDailyManager(models.Manager):
    """
    Manager with static methods for easing the handling of this kind of
    objects in the database.
    """

    def create(self, operation, periodicity, dates):
        """
        This method creates a new object in the database.
        """
        rule_daily = super(AvailabilityRuleDailyManager, self)\
            .create(operation=operation,
                    periodicity=periodicity,
                    starting_date=parser.parse(dates[0]),
                    ending_date=parser.parse(dates[1]),
                    starting_time=dates[2],
                    ending_time=dates[3])
        return rule_daily


class AvailabilityRuleDaily(AvailabilityRule):
    """
    This model describes the data necessary for describing an availability
    rule that defines an operation over the slots of a period that occurs
    everyday, in between the defined starting and ending dates.
    """
    class Meta:
        app_label = 'configuration'

    objects = AvailabilityRuleDailyManager()

    starting_time = models.TimeField('Starting time for a daily availability '
                                     'period')
    ending_time = models.TimeField('Ending time for a daily availability '
                                   'period')

    def __unicode__(self):
        """
        Unicode string representation of the contents of this object.
        """
        return str(self.starting_time) + '>>' + str(self.ending_time)


class AvailabilityRuleWeeklyManager(models.Manager):
    """
    Manager with static methods for easing the handling of this kind of
    objects in the database.
    """

    def create(self, operation, periodicity, dates):
        """
        This method creates a new object in the database.
        """
        rule_daily = super(AvailabilityRuleWeeklyManager, self)\
            .create(operation=operation,
                    periodicity=periodicity,
                    starting_date=parser.parse(dates[0]),
                    ending_date=parser.parse(dates[1]),
                    monday_starting_time=dates[2],
                    monday_ending_time=dates[3],
                    tuesday_starting_time=dates[4],
                    tuesday_ending_time=dates[5],
                    wednesday_starting_time=dates[6],
                    wednesday_ending_time=dates[7],
                    thursday_starting_time=dates[8],
                    thursday_ending_time=dates[9],
                    friday_starting_time=dates[10],
                    friday_ending_time=dates[11],
                    saturday_starting_time=dates[12],
                    saturday_ending_time=dates[13],
                    sunday_starting_time=dates[14],
                    sunday_ending_time=dates[15])
        return rule_daily


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

    monday_starting_time = models.TimeField('Starting time on Monday.')
    monday_ending_time = models.TimeField('Ending time on this Monday.')
    tuesday_starting_time = models.TimeField('Starting time on Tuesday.')
    tuesday_ending_time = models.TimeField('Ending time on this Tuesday.')
    wednesday_starting_time = models.TimeField('Starting time on Wednesday.')
    wednesday_ending_time = models.TimeField('Ending time on this Wednesday.')
    thursday_starting_time = models.TimeField('Starting time on Thursday.')
    thursday_ending_time = models.TimeField('Ending time on this Thursday.')
    friday_starting_time = models.TimeField('Starting time on Friday.')
    friday_ending_time = models.TimeField('Ending time on this Friday.')
    saturday_starting_time = models.TimeField('Starting time on Saturday.')
    saturday_ending_time = models.TimeField('Ending time on this Saturday.')
    sunday_starting_time = models.TimeField('Starting time on Sunday.')
    sunday_ending_time = models.TimeField('Ending time on this Sunday.')

    def __unicode__(self):
        """
        Unicode string representation of the contents of this object.
        """
        return '<WEEKLY PATTERN>'
