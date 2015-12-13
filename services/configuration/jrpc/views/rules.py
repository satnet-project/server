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

from services.configuration.models import rules as rule_models
from services.configuration.models import segments as segment_models
from services.configuration.jrpc.serializers import rules as rule_serializers
from website import settings as satnet_settings


@rpc4django.rpcmethod(
    name='configuration.gs.rules.list',
    signature=['String'],
    login_required=satnet_settings.JRPC_LOGIN_REQUIRED
)
def list_channel_rules(groundstation_id):
    """
    JRPC method that returns the configuration for all the rules of the
    requested channel from the requested ground station.
    :param groundstation_id: The identifier of the Ground Station.
    :return: Array with JSON objects that contain the configuration for each
    of the rules of this pair Ground Station, Channel.
    """
    return rule_serializers.serialize_rules(
        rule_models.AvailabilityRule.objects.filter(
            groundstation=segment_models.GroundStation.objects.get(
                identifier=groundstation_id
            )
        )
    )


@rpc4django.rpcmethod(
    name='configuration.gs.rules.add',
    signature=['String', 'Object'],
    login_required=satnet_settings.JRPC_LOGIN_REQUIRED
)
def add_rule(groundstation_id, rule_cfg):
    """
    JRPC method that permits adding a new rule (with the given configuration)
    to an existing channel of the given Ground Station.
    :param groundstation_id: The identifier of the Ground Station.
    :param rule_cfg: The configuration of the rule to be added.
    :return: Identifier of the rule that has just been added.
    """
    op, periodicity, dates = rule_serializers.deserialize_rule_cfg(rule_cfg)
    rule = rule_models.AvailabilityRule.objects.create(
        segment_models.GroundStation.objects.get(identifier=groundstation_id),
        op, periodicity, dates
    )
    return rule.pk


@rpc4django.rpcmethod(
    name='configuration.gs.rules.delete',
    signature=['String', 'String'],
    login_required=satnet_settings.JRPC_LOGIN_REQUIRED
)
def remove_rule(groundstation_id, rule_id):
    """
    JRPC method for removing the rule that is identified by the given rule_id
    from the channel of a ground station.
    :param groundstation_id: The identifier of the Ground Station.
    :param rule_id: Identifier of the rule to be removed.
    :return: 'True' in case the rule could be removed.
    """
    rule_models.AvailabilityRule.objects.get(
        pk=rule_id,
        groundstation=segment_models.GroundStation.objects.get(
            identifier=groundstation_id
        )
    ).delete()
    return True
