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

import rpc4django

from services.communications import models
from services.configuration.models import segments


@rpc4django.rpcmethod(
    name='communications.gs.storePassiveMessage',
    signature=['String', 'String', 'int', 'float', 'String'],
    login_required=True
)
def store_passive_message(
        groundstation_id, gs_channel_id,
        timestamp, doppler_shift,
        message
):
    """Stores a passive message from a Ground Station.

    This method stores a message obtained in a passive manner (this is, without
    requiring from any remote operation to be scheduled) by a given Ground
    Station in the database.

    :param groundstation_id: Identifier of the GroundStation.
    :param gs_channel_id: Identifier of the receiving channel of the
                            GroundStation.
    :param timestamp: Moment of the reception of the message at the remote
                        Ground Station (seconds since
    :param doppler_shift: Doppler shift during the reception of the message.
    :param message: The message to be stored.
    :return: 'true' is returned whenever the message was correctly stored,
                otherwise, an exception is thrown.
    """
    if not segments.GroundStation.objects\
            .get(identifier=groundstation_id)\
            .has_channel(gs_channel_id=gs_channel_id):

        raise Exception(
            'GroundStation <' + str(groundstation_id)
            + '> has no channel with identifier <' + str(gs_channel_id) + '>'
        )

    if message is None:
        raise Exception('No message included')

    return models.PassiveMessage.objects.create(
        gs_channel_id=gs_channel_id,
        gs_timestamp=timestamp,
        doppler_shift=doppler_shift,
        message=message
    )


@rpc4django.rpcmethod(
    name='communications.sc.getPassiveMessagesAvailable',
    signature=['String', 'String'],
    login_required=True
)
def get_available_passive_messages(groundstation_id):
    """Returns a list of the available passive messages.

    Returns a list with the identifiers of the passive messages received by
    this GroundStation.

    :param groundstation_id: The identifier of the GroundStation.
    :return: The list of the identifiers of the available messages or throws
                an exception.
    """
    pass


@rpc4django.rpcmethod(
    name='communications.sc.getPassiveMessage',
    signature=['String', 'String'],
    login_required=True
)
def get_passive_message(groundstation_id, passive_message_id):
    """Returns the selected passive message.

    Returns the requested passive message and marks it in the database as
    forwarded. From now on, it will not be shown as available in the list of
    available passive messages.

    :param groundstation_id: The identifier of the GroundStation.
    :param passive_message_id: The identifier of the passive message to be
                                retrieved.
    :return: The passive message (as 'String') or throws an exception.
    """
    pass