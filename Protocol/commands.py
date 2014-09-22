# coding=utf-8
"""
   Copyright 2014 Xabier Crespo Álvarez

   Licensed under the Apache License, Version 2.0 (the "License");
   you may not use this file except in compliance with the License.
   You may obtain a copy of the License at

       http://www.apache.org/licenses/LICENSE-2.0

   Unless required by applicable law or agreed to in writing, software
   distributed under the License is distributed on an "AS IS" BASIS,
   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
   See the License for the specific language governing permissions and
   limitations under the License.

:Author:
    Xabier Crespo Álvarez (xabicrespog@gmail.com)
"""
__author__ = 'xabicrespog@gmail.com'


from twisted.protocols import amp
from errors import *

"""
Commandes implemented by the N-server which will be invoked by a
G- or M- clients.
"""


class StartRemote(amp.Command):
    arguments = [('iSlotId', amp.Integer())]
    response = [('iResult', amp.Integer())]
    errors = {
        SlotErrorNotification: 'SLOT_ERROR_NOTIFICATION'}    
    """
    Invoked when a client wants to connect to an N-server.
    
    :param iSlotId:
        ID number of the slot which should have been previously reserved through
        the web interface.
    :type iSlotId:
        int

    :returns iResult:
        Raises an error if the slot is not available yet or if it isn't assigned to 
        the calling client. Otherwise, returns a code indicating whether that the remote
        client is not connected or if the remote client is the same as the calling client.

        In case that any of the previous cases are detected, the slotId is returned.
    :rtype:
        int or L{SlotNotAvailable}
    """
    #Both MCC and GSS belong to the same client
    CLIENTS_COINCIDE = -1
    #Remote user not connected yet
    REMOTE_NOT_CONNECTED = -2

class EndRemote(amp.Command):
    arguments = []
    requiresAnswer = False
    """
    Invoked by a client whenever this one wants to finalize the remote operation.
    """


class SendMsg(amp.Command):
    arguments = [('sMsg', amp.String())]
    requiresAnswer = False
    """
    Invoked when a client wants to send a message to a remote entity.
    
    :param bMsg:
        Array containing the message
    :type bMsg:
        bytearray
    """

"""
Commandes implemented by G- or M- clients which will be invoked
by a N-server.
"""


class NotifyError(amp.Command):
    arguments = [('sDescription', amp.String())]
    requiresAnswer = False
    """
    Used to informed a client about an error in the network.
    
    :param sDescription:

    :type sDescription:
        string
    """


class NotifyConnection(amp.Command):
    arguments = [('sClientId', amp.String())]
    requiresAnswer = False
    """
    Notifies to a client when the remote client connects to the N-server.
    
    :param sClientId:
        Remote client username
    :type sClientId:
        string
    """


class NotifyMsg(amp.Command):
    arguments = [('sMsg', amp.String())]
    requiresAnswer = False
    """
    Used to send a message to a remote client.
    
    :param bMsg:
        Remote client identification number
    :type bMsg:
        bytearray
    """


class NotifySlotEnd(amp.Command):
    arguments = [('iReason', amp.Integer())]
    requiresAnswer = False
    """
    Notifies to a client the end of the operations slot.
    
    :param iSlotId:
        Slot identification number
    :type iSlotId:
        int
    """
    #Both MCC and GSS belong to the same client
    SLOT_END = -1
    #Remote user not connected yet
    REMOTE_DISCONNECTED = -2
