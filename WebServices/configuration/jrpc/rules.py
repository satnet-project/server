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
__RULE_OP = 'rule_operation'
__RULE_OP_ADD = '+'
__RULE_OP_REMOVE = '-'
__RULE_PERIODICITY = 'rule_periodicity'
__RULE_PERIODICITY_ONCE = 'rule_periodicity_once'
__RULE_PERIODICITY_DAILY = 'rule_periodicity_daily'
__RULE_PERIODICITY_WEEKLY = 'rule_periodicity_weekly'
__RULE_DATES = 'rule_dates'
__RULE_ONCE_DATE = 'rule_once_date'
__RULE_ONCE_S_TIME = 'rule_once_starting_time'
__RULE_ONCE_E_TIME = 'rule_once_ending_time'
__RULE_DAILY_I_DATE = 'rule_daily_initial_date'
__RULE_DAILY_F_DATE = 'rule_daily_final_date'
__RULE_S_TIME = 'rule_starting_time'
__RULE_E_TIME = 'rule_ending_time'
__RULE_WEEKLY_DATE = 'rule_weekly_date'
__RULE_WEEKLY_DATE_DAY = 'rule_weekly_date_day'
__RULE_WEEKLY_WEEKDAYS = ('monday', 'tuesday', 'wednesday', 'thursday',
                          'friday', 'saturday', 'sunday')

# ### Conversion in between network keys and database keys. Notice that some
# of the keys required for the transmission of data through the network are
# not required for storing/retrieving data to/from the database, since that
# information is already stored within the hiearchy of the structure of the
# database.
__net2db__ = {
    __RULE_OP_ADD: rules.ADD_SLOTS,
    __RULE_OP_REMOVE: rules.REMOVE_SLOTS,
    __RULE_PERIODICITY_ONCE: rules.ONCE_PERIODICITY,
    __RULE_PERIODICITY_DAILY: rules.DAILY_PERIODICITY,
    __RULE_PERIODICITY_WEEKLY: rules.WEEKLY_PERIODICITY,
}
# ... from database 2 network:
__db2net__ = {
    rules.ADD_SLOTS: __RULE_OP_ADD,
    rules.REMOVE_SLOTS: __RULE_OP_REMOVE,
    rules.ONCE_PERIODICITY: __RULE_PERIODICITY_ONCE,
    rules.DAILY_PERIODICITY: __RULE_PERIODICITY_DAILY,
    rules.WEEKLY_PERIODICITY: __RULE_PERIODICITY_WEEKLY,
}

# ### Dictionary with the operations supported
__supported_operations__ = {
    __RULE_OP_ADD: True,
    __RULE_OP_REMOVE: True,
}

# ### Dictionary with the periodicities supported:
__supported_periodicities__ = {
    __RULE_PERIODICITY_ONCE: True,
    __RULE_PERIODICITY_DAILY: True,
    __RULE_PERIODICITY_WEEKLY: True,
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


@rpcmethod(name='configuration.gs.channel.removeRule',
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
    return {
        __RULE_ONCE_DATE: once_rule.date,
        __RULE_ONCE_S_TIME: once_rule.starting_time,
        __RULE_ONCE_E_TIME: once_rule.ending_time,
    }


def serialize_daily_dates():
    pass


def serialize_weekly_dates():
    pass


__date_serializers__ = {
    __RULE_PERIODICITY_ONCE: serialize_once_dates,
    __RULE_PERIODICITY_DAILY: serialize_daily_dates,
    __RULE_PERIODICITY_WEEKLY: serialize_weekly_dates,
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
            __RULE_OP: __db2net__[r.operation],
            __RULE_PERIODICITY: r.periodicity,
            __RULE_DATES: dates,
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
    if period == __RULE_PERIODICITY_ONCE:
        return deserialize_once_dates(dates)
    if period == __RULE_PERIODICITY_DAILY:
        return deserialize_daily_dates(dates)
    if period == __RULE_PERIODICITY_WEEKLY:
        return deserialize_weekly_dates(dates)


def deserialize_once_dates(dates):
    """
    Deserializes the dates as expected within a once dates object.
    :param dates: The dates object.
    :return: A 3-tuple containing all the deserialized date parameters.
    """
    return dates[__RULE_ONCE_DATE], dates[__RULE_ONCE_S_TIME], \
        dates[__RULE_ONCE_E_TIME]


def deserialize_daily_dates(dates):
    """
    Deserializes the dates as expected within a daily dates object.
    :param dates: The dates object.
    :return: A 4-tuple containing all the deserialized date parameters (
    initial date, final date, starting daily hour and ending daily hour.
    """
    return dates[__RULE_DAILY_I_DATE], dates[__RULE_DAILY_F_DATE], \
        dates[__RULE_S_TIME], dates[__RULE_E_TIME]


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

    check_weekdays = list(__RULE_WEEKLY_WEEKDAYS)
    if dates is None or len(dates) == 0:
        raise Exception('Weekly dates provided is empty.')
    for d in dates:
        if not d in __RULE_WEEKLY_WEEKDAYS:
            raise Exception('Day <' + d + '> not supported.')
        if not d in check_weekdays:
            raise Exception('Day <' + d + '> is duplicated.')
        else:
            check_weekdays.remove(d)
    return dates

# Switch-like dictionary for date deserialization functions
__dates_deserialization__ = {
    __RULE_PERIODICITY_ONCE: deserialize_once_dates,
    __RULE_PERIODICITY_DAILY: deserialize_daily_dates,
    __RULE_PERIODICITY_WEEKLY: deserialize_weekly_dates,
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
    operation = rule_cfg[__RULE_OP]
    if not operation in __supported_operations__:
        raise Exception('Operation ' + operation + ' not supported.')

    periodicity = rule_cfg[__RULE_PERIODICITY]
    if not periodicity in __supported_periodicities__:
        raise Exception('Period ' + periodicity + ' not supported.')

    dates_reader = __dates_deserialization__[periodicity]
    dates = dates_reader(rule_cfg[__RULE_DATES])
    print dates
    return __net2db__[operation], __net2db__[periodicity], dates
