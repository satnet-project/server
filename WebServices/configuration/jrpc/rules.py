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

from rpc4django import rpcmethod

from configuration.models import rules
from configuration.models.segments import GroundStation
from configuration.jrpc.serialization import deserialize_rule_cfg, \
    serialize_rules


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
    ch = GroundStation.objects.get_channel(
        ground_station_id, channel_id
    )
    op, periodicity, dates = deserialize_rule_cfg(rule_cfg)
    rule = rules.AvailabilityRule.objects.create(ch, op, periodicity, dates)
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
    GroundStation.objects.get_channel(
        ground_station_id, channel_id
    )
    rule = rules.AvailabilityRule.objects.get(pk=rule_id)
    rule.delete()
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
    gs_ch = GroundStation.objects.get_channel(
        ground_station_id, channel_id
    )
    ch_rules = rules.AvailabilityRule.objects.filter(gs_channel=gs_ch)
    return serialize_rules(ch_rules)