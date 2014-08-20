from twisted.internet.protocol import ServerFactory
from twisted.protocols.amp import AMP
from twisted.cred.credentials import UsernamePassword
from twisted.protocols.amp import IBoxReceiver
from twisted.python import log

from commands import PasswordLogin
from twisted.cred.error import UnauthorizedLogin


class CredReceiver(AMP):
    """
    Integration between AMP and L{twisted.cred}. 

    :ivar portal: 
        The L{Portal} against which login will be performed.  This is
        expected to be set by the factory which creates instances of this
        class.
    :type portal:
        L{Portal}

    :ivar logout: 
        C{None} or a no-argument callable.  This is set to the logout object
        returned by L{Portal.login} and is set while an avatar is logged in.

    :ivar username:
        Each protocol belongs to a User. This field represents User.username
    :type username:
        L{String}

    :ivar last_command:
        The time the last command was received from the User
    :type last_command:
        L{int}

    """
    portal = None
    logout = None
    username = 'NOT_AUTHENTICATED'
    last_command = 0


    def connectionLost(self, reason):
        if self.username != 'NOT_AUTHENTICATED':
            self.factory.active_protocols.pop(self.username)
        log.err(reason.getErrorMessage())
        log.msg('Active connections: ' + str(len(self.factory.active_protocols)))

    def passwordLogin(self, sUsername, sPassword):
        """
        Generate a new challenge for the given username.
        """
        if self.factory.active_protocols.get(sUsername):
            raise UnauthorizedLogin('Client already logged in')
        else:
            self.username = sUsername

        d = self.portal.login(UsernamePassword(sUsername, sPassword), None, IBoxReceiver)
        def cbLoggedIn((interface, avatar, logout)):
            self.logout = logout
            self.boxReceiver = avatar
            self.boxReceiver.startReceivingBoxes(self.boxSender)
            self.factory.active_protocols[sUsername] = self
            log.msg('Connection made')
            log.msg('Active connections: ' + str(len(self.factory.active_protocols)))

            return {'bAuthenticated':True}
        d.addCallback(cbLoggedIn)
        return d
    PasswordLogin.responder(passwordLogin)


class CredAMPServerFactory(ServerFactory):
    """
    Server factory useful for creating L{CredReceiver} instances.

    This factory takes care of associating a L{Portal} with L{CredReceiver}
    instances it creates.

    :ivar portal: 
        The portal which will be used by L{CredReceiver} instances
        created by this factory.
    :type portal:
        L{Portal}

    :ivar active_protocols:
        A list containing a reference to all active protocols
    :type active_protocols:
        L{List}

    """
    protocol = CredReceiver
    active_protocols = {}

    def __init__(self, portal):
        self.portal = portal


    def buildProtocol(self, addr):
        proto = ServerFactory.buildProtocol(self, addr)
        proto.portal = self.portal
        return proto
