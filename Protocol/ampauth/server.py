from twisted.internet.protocol import ServerFactory
from twisted.protocols.amp import AMP
from twisted.cred.credentials import UsernamePassword
from twisted.protocols.amp import IBoxReceiver

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

    """
    portal = None
    logout = None

    def passwordLogin(self, sUsername, sPassword):
        """
        Generate a new challenge for the given username.
        """
        print "Login attempt: " + sUsername
        self.username = sUsername
        d = self.portal.login(UsernamePassword(sUsername, sPassword), None, IBoxReceiver)
        def cbLoggedIn((interface, avatar, logout)):
            self.logout = logout
            self.boxReceiver = avatar
            self.boxReceiver.startReceivingBoxes(self.boxSender)
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
    """
    protocol = CredReceiver

    def __init__(self, portal):
        self.portal = portal


    def buildProtocol(self, addr):
        proto = ServerFactory.buildProtocol(self, addr)
        proto.portal = self.portal
        return proto
