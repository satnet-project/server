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

from services.configuration.models import segments as segment_models
from services.configuration.models import compatibility as compatibility_models
from services.configuration.jrpc.serializers import compatibility as \
    compatibility_serializers
from website import settings as satnet_settings


@rpcmethod(
    name="configuration.sc.channel.getCompatible",
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

    # 1) Retrieve objects from database
    spacecraft_ch = segment_models.Spacecraft.objects.get(
        identifier=spacecraft_id
    ).channels.all().get(
        identifier=channel_id
    )

    # 2) Retrieve compatible ground station channels
    compatible_chs = compatibility_models.ChannelCompatibility.objects.filter(
        spacraft_channel=spacecraft_ch
    )

    # 3) Generate list with tuples (groundstation, gs_channel)
    compatible_tuples = []
    for gs_ch in compatible_chs:

        gs = segment_models.GroundStation.objects.get(channels__in=[gs_ch])
        compatible_tuples.append((gs, gs_ch))

    # 4) Serialization
    return compatibility_serializers.CompatibilitySerializer\
        .serialize_gs_ch_compatibility_tuples(compatible_tuples)
