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

import base64
import rpc4django

from services.common import misc
from services.communications import models as comm_models
from services.configuration.models import segments as segment_models


@rpc4django.rpcmethod(
    name='communications.gs.storePassiveMessage',
    signature=['String', 'int', 'float', 'String'],
    login_required=True
)
def store_passive_message(groundstation_id, timestamp, doppler_shift, message):
    """Stores a passive message from a Ground Station.
    This method stores a message obtained in a passive manner (this is, without
    requiring from any remote operation to be scheduled) by a given Ground
    Station in the database.

    :param groundstation_id: Identifier of the GroundStation.
    :param timestamp: Moment of the reception of the message at the remote
                        Ground Station (seconds since
    :param doppler_shift: Doppler shift during the reception of the message.
    :param message: The message to be stored.
    :return: 'true' is returned whenever the message was correctly stored,
                otherwise, an exception is thrown.
    """
    if message is None:
        raise Exception('No message included')

    groundstation = segment_models.GroundStation.objects.get(
        identifier=groundstation_id
    )
    if not groundstation:
        raise Exception(
            'GroundStation does not exist! id = ' + str(groundstation_id)
        )

    # Tries to decode the message in BASE64, if wrong, an exception is thrown.
    # Otherwise, this is just a check for the message, the message will be
    # stored in BASE64 in the database anyway.
    base64.b64decode(message)

    message_o = comm_models.PassiveMessage.objects.create(
        groundstation=groundstation,
        groundstation_timestamp=timestamp,
        reception_timestamp=misc.get_utc_timestamp(
            misc.get_now_utc()
        ),
        doppler_shift=doppler_shift,
        message=message
    )

    return message_o.pk


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