from twisted.protocols import amp

"""
Commandes implemented by the N-server which will be invoked by a
G- or M- clients.
"""


class StartRemote(amp.Command):
    arguments = [('iClientId', amp.Integer()),
                 ('iSlotId', amp.Integer())]
    response = [('iResult', amp.Integer())]
    """
    Invoked when a client wants to connect to an N-server.
    :param iClientId:
        Remote client identification number
    :type iClientId:
        int
    :param iClientId:

    :type iClientId:
        int

    :returns:
        Code indicating whether the slot has ended or not, and whether the
        other client required for the remote operation is still connected or not.
    :rtype:
        int
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
