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

from services.configuration.models import rules as rule_models,\
    segments as segment_models
from services.configuration.jrpc.serializers import serialization
from website import settings as satnet_settings


@rpc4django.rpcmethod(
    name='configuration.gs.listRules',
    signature=['String'],
    login_required=satnet_settings.JRPC_LOGIN_REQUIRED
)
def list_grouped_rules(groundstation_id):
    """JRPC method
    Returns the configuration for the grouped rules of the given Ground
    Station.
    :param groundstation_id: The identifier of the Ground Station
    :return: JSON objects with the configuration of the rules within an array
    """
    rules = []
    groups = rule_models.GroupedAvailabilityRules.objects.filter(
        groundstation=segment_models.GroundStation.objects.get(
            identifier=groundstation_id
        )
    )

    # From each group, we only get the first rule since they are all equal
    for g in groups:
        rules.append(g.rules.all()[0])

    return serialization.serialize_rules(rules)


@rpc4django.rpcmethod(
    name='configuration.gs.channel.listRules',
    signature=['String', 'String'],
    login_required=satnet_settings.JRPC_LOGIN_REQUIRED
)
def list_channel_rules(groundstation_id, channel_id):
    """
    JRPC method that returns the configuration for all the rules of the
    requested channel from the requested ground station.
    :param groundstation_id: The identifier of the Ground Station.
    :param channel_id: The identifier of the channel.
    :return: Array with JSON objects that contain the configuration for each
    of the rules of this pair Ground Station, Channel.
    """
    ch = segment_models.GroundStation.objects.get(
        identifier=groundstation_id
    ).channels.all().get(
        identifier=channel_id
    )
    ch_rules = rule_models.AvailabilityRule.objects.filter(gs_channel=ch)
    return serialization.serialize_rules(ch_rules)


@rpc4django.rpcmethod(
    name='configuration.gs.addRule',
    signature=['String', 'Object'],
    login_required=satnet_settings.JRPC_LOGIN_REQUIRED
)
def add_grouped_rule(groundstation_id, rule_cfg):
    """JRPC method
    Adds the given rule to all the channels of the Ground Station.
    :param groundstation_id: The identifier of the Ground Station
    :param rule_cfg: The configuration of the rule to be added
    :return: List with the primary keys of the added rules.
    """
    op, periodicity, dates = serialization.deserialize_rule_cfg(rule_cfg)
    return rule_models.GroupedAvailabilityRules.objects.create(
        groundstation_id, op, periodicity, dates
    )


@rpc4django.rpcmethod(
    name='configuration.gs.channel.addRule',
    signature=['String', 'String', 'Object'],
    login_required=satnet_settings.JRPC_LOGIN_REQUIRED
)
def add_rule(groundstation_id, channel_id, rule_cfg):
    """
    JRPC method that permits adding a new rule (with the given configuration)
    to an existing channel of the given Ground Station.
    :param groundstation_id: The identifier of the Ground Station.
    :param channel_id: The identifier of the channel.
    :param rule_cfg: The configuration of the rule to be added.
    :return: Identifier of the rule that has just been added.
    """
    ch = segment_models.GroundStation.objects.get(
        identifier=groundstation_id
    ).channels.all().get(
        identifier=channel_id
    )
    op, periodicity, dates = serialization.deserialize_rule_cfg(rule_cfg)
    rule = rule_models.AvailabilityRule.objects.create(
        ch, op, periodicity, dates
    )
    return rule.pk


@rpc4django.rpcmethod(
    name='configuration.gs.removeRule',
    signature=['String', 'String'],
    login_required=satnet_settings.JRPC_LOGIN_REQUIRED
)
def remove_grouped_rule(groundstation_id, group_id):
    """JRPC method
    Removes all the rules belonging to the indicated group.
    :param groundstation_id: The identifier of the Ground Station
    :param group_id: Identifier of the group
    :return: 'True' in case the group of rules could be removed.
    """
    group = rule_models.GroupedAvailabilityRules.objects.get(id=group_id)

    for g in rule_models.GroupedAvailabilityRules.objects.all():
        print('>>> g = ' + str(g))

    # 1) we have to check that the group_id belongs to the indicated gs
    if group.groundstation.identifier != groundstation_id:
        raise Exception(
            'group_id <' + str(
                group_id
            ) + '>, does not belong to gs <' + str(
                groundstation_id
            ) + '>'
        )

    # 2) after these checks, we effectively delete the rules
    rule_models.AvailabilityRule.objects.filter(
        id__in=group.rules.all()
    ).delete()

    return True


@rpc4django.rpcmethod(
    name='configuration.gs.channel.removeRule',
    signature=['String', 'String', 'String'],
    login_required=satnet_settings.JRPC_LOGIN_REQUIRED
)
def remove_rule(groundstation_id, channel_id, rule_id):
    """
    JRPC method for removing the rule that is identified by the given rule_id
    from the channel of a ground station.
    :param groundstation_id: The identifier of the Ground Station.
    :param channel_id: The identifier of the channel.
    :param rule_id: Identifier of the rule to be removed.
    :return: 'True' in case the rule could be removed.
    """
    segment_models.GroundStation.objects.get(
        identifier=groundstation_id
    ).channels.all().get(
        identifier=channel_id
    )
    rule = rule_models.AvailabilityRule.objects.get(pk=rule_id)
    rule.delete()
    return True
