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

import dateutil.parser as du_parser

from services.common import serialization as common_serial
from services.configuration.models import rules


# JRPC keys for data exchange with clients through key-indexed objects.
RULE_PK_K = 'key'
RULE_OP = 'rule_operation'
RULE_OP_ADD = '+'
RULE_OP_REMOVE = '-'
RULE_PERIODICITY = 'rule_periodicity'
RULE_PERIODICITY_ONCE = 'rule_periodicity_once'
RULE_PERIODICITY_DAILY = 'rule_periodicity_daily'
RULE_PERIODICITY_WEEKLY = 'rule_periodicity_weekly'
RULE_DATES = 'rule_dates'
RULE_ONCE_DATE = 'rule_once_date'
RULE_ONCE_S_TIME = 'rule_once_starting_time'
RULE_ONCE_E_TIME = 'rule_once_ending_time'
RULE_DAILY_I_DATE = 'rule_daily_initial_date'
RULE_DAILY_F_DATE = 'rule_daily_final_date'
RULE_S_TIME = 'rule_starting_time'
RULE_E_TIME = 'rule_ending_time'
RULE_WEEKLY_DATE = 'rule_weekly_date'
RULE_WEEKLY_DATE_DAY = 'rule_weekly_date_day'
RULE_WEEKLY_WEEKDAYS = (
    'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday',
    'sunday'
)

# ### Conversion in between network keys and database keys. Notice that some
# of the keys required for the transmission of data through the network are
# not required for storing/retrieving data to/from the database, since that
# information is already stored within the hiearchy of the structure of the
# database.
__net2db__ = {
    RULE_OP_ADD: rules.ADD_SLOTS,
    RULE_OP_REMOVE: rules.REMOVE_SLOTS,
    RULE_PERIODICITY_ONCE: rules.ONCE_PERIODICITY,
    RULE_PERIODICITY_DAILY: rules.DAILY_PERIODICITY,
    RULE_PERIODICITY_WEEKLY: rules.WEEKLY_PERIODICITY,
}
# ... from database 2 network:
__db2net__ = {
    rules.ADD_SLOTS: RULE_OP_ADD,
    rules.REMOVE_SLOTS: RULE_OP_REMOVE,
    rules.ONCE_PERIODICITY: RULE_PERIODICITY_ONCE,
    rules.DAILY_PERIODICITY: RULE_PERIODICITY_DAILY,
    rules.WEEKLY_PERIODICITY: RULE_PERIODICITY_WEEKLY,
}

# ### Dictionary with the operations supported
__supported_operations__ = {
    RULE_OP_ADD: True,
    RULE_OP_REMOVE: True,
}

# ### Dictionary with the periodicities supported:
__supported_periodicities__ = {
    RULE_PERIODICITY_ONCE: True,
    RULE_PERIODICITY_DAILY: True,
    RULE_PERIODICITY_WEEKLY: True,
}


def serialize_once_dates(rule, child_rule):
    """
    Function that serializes the dates from a once rule object as taken from
    the database.
    :param rule: The parent rule to be fully serialized
    :param child_rule: Reference to the underlaying child object
    :return: An object serializable structure
    """
    return {
        RULE_ONCE_DATE: common_serial.serialize_iso8601_date(
            rule.starting_date
        ),
        RULE_ONCE_S_TIME: common_serial.serialize_iso8601_time(
            child_rule.starting_time
        ),
        RULE_ONCE_E_TIME: common_serial.serialize_iso8601_time(
            child_rule.ending_time
        )
    }


def serialize_daily_dates(rule, child_rule):
    """
    Function that serializes the dates from a daily rule object as taken from
    the database.
    :param rule: The daily rule to be serialized.
    :param child_rule: Refernce to the rule object
    :return: An object serializable structure.
    """
    return {
        RULE_DAILY_I_DATE: common_serial.serialize_iso8601_date(
            rule.starting_date
        ),
        RULE_DAILY_F_DATE: common_serial.serialize_iso8601_date(
            rule.ending_date
        ),
        RULE_S_TIME: common_serial.serialize_iso8601_time(
            child_rule.starting_time
        ),
        RULE_E_TIME: common_serial.serialize_iso8601_time(
            child_rule.ending_time
        )
    }


def serialize_weekly_dates(rule, child_rule):
    """
    Function that serializes the dates from a weekly rule object as taken from
    the database.
    :param rule: The reference to the dates as taken from the database
    :param child_rule: Reference to the underlaying child object
    :return: An object serializable structure
    """
    dates = []
    for d in RULE_WEEKLY_WEEKDAYS:
        dates.append({
            RULE_WEEKLY_DATE_DAY: d,
            RULE_S_TIME: common_serial.serialize_iso8601_time(
                child_rule[d + '_starting_time']
            ),
            RULE_E_TIME: common_serial.serialize_iso8601_time(
                child_rule[d + '_ending_time']
            )
        })
    return {
        RULE_DAILY_I_DATE: common_serial.serialize_iso8601_date(
            rule.starting_date
        ),
        RULE_DAILY_F_DATE: common_serial.serialize_iso8601_date(
            rule.ending_date
        ),
        RULE_DATES: dates
    }

__date_serializers__ = {
    RULE_PERIODICITY_ONCE: serialize_once_dates,
    RULE_PERIODICITY_DAILY: serialize_daily_dates,
    RULE_PERIODICITY_WEEKLY: serialize_weekly_dates,
}


def serialize_rules(channel_rules):
    """
    This method serializes in JSON format all the rule objects contained in
    the list given as a parameter.
    :param channel_rules: The array of objects with the rules as read from the
    database.
    :return: JSON structure with all the rules.
    """
    jrules = []
    for r in channel_rules:

        periodicity = __db2net__[r.periodicity]
        child_r = rules.AvailabilityRule.objects.get_specific_rule(r.id)
        serializer = __date_serializers__[periodicity]

        if serializer is None:
            continue

        jrules.append({
            RULE_PK_K: r.id,
            RULE_OP: __db2net__[r.operation],
            RULE_PERIODICITY: __db2net__[r.periodicity],
            RULE_DATES: serializer(r, child_r),
        })

    return jrules


def deserialize_dates(period, dates):
    """
    This method deserializes the dates contained within the parameters required
    by a
    :param period: The period that this rule represents.
    :param dates: The dates object as obtained from the network.
    :return: All the date parameters returned as a N-tuple.
    """
    if period == RULE_PERIODICITY_ONCE:
        return deserialize_once_dates(dates)
    if period == RULE_PERIODICITY_DAILY:
        return deserialize_daily_dates(dates)
    if period == RULE_PERIODICITY_WEEKLY:
        return deserialize_weekly_dates(dates)


def deserialize_once_dates(dates):
    """
    Deserializes the dates as expected within a once dates object.
    :param dates: The dates object
    :return: A 2-tuple containing all the deserialized date parameters
    """
    return (
        du_parser.parse(dates[RULE_ONCE_S_TIME]),
        du_parser.parse(dates[RULE_ONCE_E_TIME])
    )

    # OLD code for de-serializing 3 elements
    # return\
    #    common_serial.deserialize_iso8601_date(dates[RULE_ONCE_DATE]),\
    #    common_serial.deserialize_iso8601_time(dates[RULE_ONCE_S_TIME]),\
    #    common_serial.deserialize_iso8601_time(dates[RULE_ONCE_E_TIME])


def deserialize_daily_dates(dates):
    """
    Deserializes the dates as expected within a daily dates object.
    :param dates: The dates object.
    :return: A 4-tuple containing all the deserialized date parameters (
    initial date, final date, starting daily hour and ending daily hour.
    """
    return\
        common_serial.deserialize_iso8601_date(dates[RULE_DAILY_I_DATE]), \
        common_serial.deserialize_iso8601_date(dates[RULE_DAILY_F_DATE]), \
        common_serial.deserialize_iso8601_time(dates[RULE_S_TIME]),\
        common_serial.deserialize_iso8601_time(dates[RULE_E_TIME])


def deserialize_weekly_dates(dates):
    """
    Since the value for the days of the weeks are not stored within the table
    in the database, in this case the object that is obtained directly from
    the network can be utilized for accessing the database. Therefore,
    only a brief validation of the data contained in that structure is
    necessary.
    :param dates: The days of the week with the time intervals per day.
    :return: The structure with the time intervals per weekday.
    """
    check_weekdays = list(RULE_WEEKLY_WEEKDAYS)
    if dates is None or len(dates) == 0:
        raise Exception('Weekly dates provided is empty.')
    for d in dates:
        if d not in RULE_WEEKLY_WEEKDAYS:
            raise Exception('Day <' + d + '> not supported.')
        if d not in check_weekdays:
            raise Exception('Day <' + d + '> is duplicated.')
        else:
            check_weekdays.remove(d)
    return dates

# Switch-like dictionary for date deserialization functions
__dates_deserialization__ = {
    RULE_PERIODICITY_ONCE: deserialize_once_dates,
    RULE_PERIODICITY_DAILY: deserialize_daily_dates,
    RULE_PERIODICITY_WEEKLY: deserialize_weekly_dates,
}


def deserialize_rule_cfg(rule_cfg):
    """
    This method deserializes the parameters required for the configuration
    of a given rule, as that configuration object is obtained from within the
    network.
    :param rule_cfg: Configuration object as obtained from the network.
    :return: All the parameteres returned as a N-tuple.
    """
    operation = rule_cfg[RULE_OP]
    if operation not in __supported_operations__:
        raise Exception('Operation ' + operation + ' not supported.')

    periodicity = rule_cfg[RULE_PERIODICITY]
    if periodicity not in __supported_periodicities__:
        raise Exception('Period ' + periodicity + ' not supported.')

    dates_reader = __dates_deserialization__[periodicity]
    dates = dates_reader(rule_cfg[RULE_DATES])
    return __net2db__[operation], __net2db__[periodicity], dates
