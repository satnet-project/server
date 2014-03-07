"""
   Copyright 2013, 2014 Ricardo Tubio-Pardavila

   Licensed under the Apache License, Version 2.0 (the "License")
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
from configuration.models import rules
from configuration.models.segments import GroundStationConfiguration
from configuration.utils import print_dictionary
from rpc4django import rpcmethod

# ### Main logger for this package
logger = logging.getLogger(__name__)

# JRPC keys for data exchange with clients through key-indexed objects.
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
RULE_WEEKLY_WEEKDAYS = ('monday', 'tuesday', 'wednesday', 'thursday',
                        'friday', 'saturday', 'sunday')

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


@rpcmethod(name='configuration.gs.channel.addRule',
           signature=['String', 'String', 'Object'], login_required=True)
def add_rule(ground_station_id, channel_id, rule_cfg):
    """
    JRPC method that permits adding a new rule (with the given configuration)
    to an existing channel of the given Ground Station.
    :param ground_station_id: The identifier of the Ground Station.
    :param channel_id: The identifier of the channel.
    :param rule_cfg: The configuration of the rule to be added.
    :return: Identifier of the rule that has just been added.
    """
    ch = GroundStationConfiguration.objects.get_channel(ground_station_id,
                                                        channel_id)
    op, periodicity, dates = deserialize_rule_cfg(rule_cfg)
    rule = ch.add_rule(operation=op, periodicity=periodicity, dates=dates)
    return rule.pk


@rpcmethod(name='configuration.gs.channel.removeRule',
           signature=['String', 'String', 'String'], login_required=True)
def remove_rule(ground_station_id, channel_id, rule_id):
    """
    JRPC method for removing the rule that is identified by the given rule_id
    from the channel of a ground station.
    :param ground_station_id: The identifier of the Ground Station.
    :param channel_id: The identifier of the channel.
    :param rule_id: Identifier of the rule to be removed.
    :return: 'True' in case the rule could be removed.
    """
    ch = GroundStationConfiguration.objects.get_channel(ground_station_id,
                                                        channel_id)
    ch.remove_rule(rule_id)
    return True


@rpcmethod(name='configuration.gs.channel.getRules',
           signature=['String', 'String'], login_required=True)
def get_rules(ground_station_id, channel_id):
    """
    JRPC method that returns the configuration for all the rules of the
    requested channel from the requested ground station.
    :param ground_station_id: The identifier of the Ground Station.
    :param channel_id: The identifier of the channel.
    :return: Array with JSON objects that contain the configuration for each
    of the rules of this pair Ground Station, Channel.
    """
    ch = GroundStationConfiguration.objects.get_channel(ground_station_id,
                                                        channel_id)
    ch_rules = ch.get_rules()
    return serialize_rules(ch_rules)


def serialize_once_dates(once_rule):
    """
    Function that serializes the dates from a once rule object as taken from
    the database.
    :param once_rule: The only once rule to be serialized.
    :return: An object serializable structure.
    """
    return {
        RULE_ONCE_DATE: once_rule.date,
        RULE_ONCE_S_TIME: once_rule.starting_time,
        RULE_ONCE_E_TIME: once_rule.ending_time,
    }


def serialize_daily_dates(daily_rule):
    """
    Function that serializes the dates from a daily rule object as taken from
    the database.
    :param daily_rule: The daily rule to be serialized.
    :return: An object serializable structure.
    """
    return {
        RULE_DAILY_I_DATE: daily_rule.initial_date,
        RULE_DAILY_F_DATE: daily_rule.final_date,
        RULE_S_TIME: daily_rule.starting_time,
        RULE_E_TIME: daily_rule.ending_time,
    }


def serialize_weekly_dates(weekly_rule):
    """
    Function that serializes the dates from a weekly rule object as taken from
    the database.
    :param weekly_rule: The reference to the dates as taken from the database.
    :return: An object serializable structure.
    """
    dates = []
    for d in RULE_WEEKLY_WEEKDAYS:
        dates.append({
            RULE_WEEKLY_DATE_DAY: d,
            RULE_S_TIME: weekly_rule[d + '_starting_time'],
            RULE_E_TIME: weekly_rule[d + '_ending_time'],
        })
    return dates


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
        dates = __date_serializers__[periodicity](r)
        jrules.append({
            RULE_OP: __db2net__[r.operation],
            RULE_PERIODICITY: r.periodicity,
            RULE_DATES: dates,
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
    :param dates: The dates object.
    :return: A 3-tuple containing all the deserialized date parameters.
    """
    return dates[RULE_ONCE_DATE], dates[RULE_ONCE_S_TIME], \
        dates[RULE_ONCE_E_TIME]


def deserialize_daily_dates(dates):
    """
    Deserializes the dates as expected within a daily dates object.
    :param dates: The dates object.
    :return: A 4-tuple containing all the deserialized date parameters (
    initial date, final date, starting daily hour and ending daily hour.
    """
    return dates[RULE_DAILY_I_DATE], dates[RULE_DAILY_F_DATE], \
        dates[RULE_S_TIME], dates[RULE_E_TIME]


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
        if not d in RULE_WEEKLY_WEEKDAYS:
            raise Exception('Day <' + d + '> not supported.')
        if not d in check_weekdays:
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

    print_dictionary(rule_cfg)
    operation = rule_cfg[RULE_OP]
    if not operation in __supported_operations__:
        raise Exception('Operation ' + operation + ' not supported.')

    periodicity = rule_cfg[RULE_PERIODICITY]
    if not periodicity in __supported_periodicities__:
        raise Exception('Period ' + periodicity + ' not supported.')

    dates_reader = __dates_deserialization__[periodicity]
    dates = dates_reader(rule_cfg[RULE_DATES])
    return __net2db__[operation], __net2db__[periodicity], dates
