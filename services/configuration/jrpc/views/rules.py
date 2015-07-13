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

import rpc4django

from services.configuration.models import rules, segments
from services.configuration.jrpc.serializers import serialization
from website import settings as satnet_settings


@rpc4django.rpcmethod(
    name='configuration.gs.rules.list',
    signature=['String'],
    login_required=satnet_settings.JRPC_LOGIN_REQUIRED
)
def list_rules(groundstation_id):
    """JRPC method
    JRPC method that returns the configuration for all the rules of the
    requested channel from the requested ground station
    :param groundstation_id: The identifier of the Ground Station
    :return: Array with JSON objects that contain the configuration for each
    of the rules of this pair Ground Station, Channel
    """
    ch_rules = rules.AvailabilityRule.objects.filter(
        ground_station=segments.GroundStation.objects.get(
            identifier=groundstation_id
        )
    )
    return serialization.serialize_rules(ch_rules)


@rpc4django.rpcmethod(
    name='configuration.gs.rules.add',
    signature=['String', 'Object'],
    login_required=satnet_settings.JRPC_LOGIN_REQUIRED
)
def add_rule(groundstation_id, rule_cfg):
    """JRPC method
    JRPC method that permits adding a new rule (with the given configuration)
    to an existing channel of the given Ground Station.
    :param groundstation_id: The identifier of the Ground Station
    :param rule_cfg: The configuration of the rule to be added
    :return: Identifier of the rule that has just been added
    """
    gs = segments.GroundStation.objects.get(identifier=groundstation_id)
    op, periodicity, dates = serialization.deserialize_rule_cfg(rule_cfg)
    rule = rules.AvailabilityRule.objects.create(gs, op, periodicity, dates)
    return rule.pk


@rpc4django.rpcmethod(
    name='configuration.gs.rules.delete',
    signature=['String', 'String'],
    login_required=satnet_settings.JRPC_LOGIN_REQUIRED
)
def delete_rule(groundstation_id, rule_id):
    """JRPC method
    JRPC method for removing the rule that is identified by the given rule_id
    from the channel of a ground station.
    :param groundstation_id: The identifier of the Ground Station
    :param rule_id: Identifier of the rule to be removed
    :return: 'True' in case the rule could be removed
    """
    segments.GroundStation.objects.get(identifier=groundstation_id)
    rule = rules.AvailabilityRule.objects.get(pk=rule_id)
    rule.delete()
    return True


@rpc4django.rpcmethod(
    name='configuration.gs.rules.get',
    signature=['String', 'String'],
    login_required=satnet_settings.JRPC_LOGIN_REQUIRED
)
def get_rule(groundstation_id, rule_pk):
    """JRPC method
    JRPC method that returns the configuration for all the rules of the
    requested channel from the requested ground station.
    :param groundstation_id: The identifier of the Ground Station.
    :return: Array with JSON objects that contain the configuration for each
    of the rules of this pair Ground Station, Channel.
    """
    ground_station = segments.GroundStation.objects.get(
        identifier=groundstation_id
    )
    r = rules.AvailabilityRule.objects\
        .filter(ground_station=ground_station)\
        .get(pk=rule_pk)
    return serialization.serialize_rule(r)
