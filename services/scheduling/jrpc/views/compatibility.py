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

from rpc4django import rpcmethod

from services.configuration.models import channels as channel_models
from services.configuration.models import segments as segment_models
from services.scheduling.models import compatibility as compatibility_models
from services.scheduling.jrpc.serializers import compatibility\
    as compatibility_serializers
from website import settings as satnet_settings


def get_compatiblility(spacecraft_ch):
    """Common method
    Returns the tuples (GS, GS_CH) with the compatible Ground Station
    channels with the given spacecraft channel.

    :param spacecraft_ch: The channel for which the tuples are compatible with
    :return: List with the (GS, GS_CH) tuples
    """
    gs_chs = compatibility_models.ChannelCompatibility.objects.filter(
        spacecraft_channel=spacecraft_ch
    )

    for g in gs_chs:
        print(g)

    compatible_tuples = [
        (
            c.groundstation_channel.groundstation, c.groundstation_channel
        ) for c in gs_chs
    ]

    for c in compatible_tuples:
        print(c)

    serialized_result = compatibility_serializers\
        .serialize_gs_ch_compatibility_tuples(
            compatible_tuples
        )

    return serialized_result


@rpcmethod(
    name="scheduling.sc.channel.getCompatibility",
    signature=['String', 'String'],
    login_required=satnet_settings.JRPC_LOGIN_REQUIRED
)
def sc_channel_get_compatible(spacecraft_id, channel_id):
    """JRPC method
    It returns the list of available ground station channels that are
    compatible in terms of communications with this channel.
    :param spacecraft_id: Identifier of the spacecraft
    :param channel_id: Identifier of the channel
    :return: List with tuples (groundstation, gs_channel)
    """
    return get_compatiblility(
        channel_models.SpacecraftChannel.objects.get(
            identifier=channel_id,
            spacecraft=segment_models.Spacecraft.objects.get(
                identifier=spacecraft_id
            )
        )
    )


@rpcmethod(
    name="scheduling.sc.getCompatibility",
    signature=['String'],
    login_required=satnet_settings.JRPC_LOGIN_REQUIRED
)
def sc_get_compatible(spacecraft_id):
    """JRPC method
    It returns the list of available ground station channels that are
    compatible in terms of communications with all the channels of the
    segment.
    :param spacecraft_id: Identifier of the spacecraft
    :return: Dictionary with lists with tuples (groundstation, gs_channel)
    """

    results = []
    spacecraft = segment_models.Spacecraft.objects.get(
        identifier=spacecraft_id
    )

    for spacecraft_ch in channel_models.SpacecraftChannel.objects.filter(
        spacecraft=spacecraft
    ):

        r = compatibility_serializers.serialize_sc_ch_compatibility(
            spacecraft_ch,
            get_compatiblility(spacecraft_ch)
        )

        results.append(r)

    return compatibility_serializers.serialize_sc_compatibility(
        spacecraft, results
    )
