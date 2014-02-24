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
from dateutil import parser

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
        rule_child = db_obj_class.objects.create(operation, periodicity,
                                                 dates[0], dates[1], dates[2])
        return AvailabilityRule.objects\
            .get(id=rule_child.availabilityrule_ptr_id)


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
        ADD_SLOTS: '(add slots)',
        REMOVE_SLOTS: '(remove slots)',
    }

    def __unicode__(self):
        """
        Unicode string representation of the contents of this object.
        """
        return self.__operation2unicode__[self.operation]


class AvailabilityRuleOnceManager(models.Manager):
    """
    Manager with static methods for easing the handling of this kind of
    objects in the database.
    """

    def create(self, operation, periodicity, date,
               starting_time, ending_time):
        """
        This method creates a new object in the database.
        """
        rule_once = super(AvailabilityRuleOnceManager, self)\
            .create(operation=operation,
                    periodicity=periodicity,
                    starting_date=parser.parse(date),
                    ending_date=parser.parse(date),
                    starting_time=starting_time,
                    ending_time=ending_time)
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
        return ', ONCE, from: ' + self.starting_time\
               + ', to: ' + self.ending_time


class AvailabilityRuleDailyManager(models.Manager):
    pass


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


class AvailabilityRuleWeeklyManager(models.Manager):
    pass


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

