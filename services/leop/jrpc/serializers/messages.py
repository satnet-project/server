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

from services.leop.jrpc.serializers import launch as launch_serializers

PUSH_K_FRAME = 'frame'
JRPC_K_TS = 'timestamp'
JRPC_K_MESSAGE = 'message'


def serialize_push_frame(message):
    """PUSH serialization
    Serializes the given message into a JRPC-like structure.
    :param message: Message object as read from the database.
    :return: JSON structure that can be transported
    """
    return {
        PUSH_K_FRAME: serialize_message(message)
    }


def serialize_message(message):
    """JRPC serialization
    Serializes the given message into a JRPC-like structure.
    :param message: Message object as read from the database.
    :return: JSON structure that can be transported
    """
    return {
        launch_serializers.JRPC_K_GS_ID: message.groundstation.identifier,
        JRPC_K_TS: message.groundstation_timestamp,
        JRPC_K_MESSAGE: message.message.decode('utf-8')
    }


def serialize_messages(messages):
    """JRPC serialization
    Method that serializes an array of messages as read from the database
    through a query.
    :param messages: The message objects as read from the database
    :return: JSON serialiazible array
    """
    serial_messages = []

    for m in messages:
        serial_messages.append(serialize_message(m))

    return serial_messages
