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
from errors import SlotNotAvailable

"""
Commandes implemented by the N-server which will be invoked by a
G- or M- clients.
"""


class StartRemote(amp.Command):
    arguments = [('iClientId', amp.Integer()),
                 ('iSlotId', amp.Integer())]
    response = [('iResult', amp.Integer())]
    errors = {
        SlotNotAvailable: 'SLOT_NOT_AVAILABLE'}    
    """
    Invoked when a client wants to connect to an N-server.
    
    :param iClientId:
        Local client identification number
    :type iClientId:
        int
    :param iClientId:

    :type iClientId:
        int

    :returns iResult:
        Code indicating whether the slot has ended or not, and whether the
        other client required for the remote operation is still connected or not.
    :rtype:
        int or L{SlotNotAvailable}
    """


class EndRemote(amp.Command):
    arguments = []
    requiresAnswer = False
    """
    Invoked to send a message to a remote entity.
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
by a N- server.
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
    arguments = [('iClientId', amp.Integer())]
    requiresAnswer = False
    """
    Notifies to a client the connecton of an aditional remote client.
    
    :param iClientId:
        Client identification number
    :type iClientId:
        int
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
    arguments = [('iSlotId', amp.Integer())]
    requiresAnswer = False
    """
    Notifies to a client the end of the operations slot.
    
    :param iSlotId:
        Slot identification number
    :type iSlotId:
        int
    """
