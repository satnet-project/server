import logging

from twisted.internet import defer, protocol
from twisted.trial import unittest
from twisted.cred.portal import Portal
from twisted.internet import reactor, ssl

from commands import *
from ampauth.credentials import *
from ampauth.server import *
from ampauth.client import login
from ampauth.server import CredReceiver
from client_amp import ClientProtocol
from errors import SlotNotAvailable

from services.common import testing as db_tools, misc, simulation

"""
To perform correct end to end tests:
1. The server must stop listening.
2. The client connection must disconnect.
3. The server connection must disconnect.

For more information about how to perform end to end
unit tests check http://blackjml.livejournal.com/23029.html
"""


class ServerProtocolTest(CredReceiver):

    def connectionLost(self, reason):
        super(ServerProtocolTest, self).connectionLost(reason)
        self.factory.onConnectionLost.callback(self)


class ClientProtocolTest(ClientProtocol):

    def connectionMade(self):
        self.factory.protoInstance = self
        self.factory.onConnectionMade.callback(self)

    def connectionLost(self, reason):
        self.factory.onConnectionLost.callback(self)


class TestRemoteConnection(unittest.TestCase):

    """
    Testing starting a remote connection
    """

    def setUp(self):
        log.startLogging(sys.stdout)
        self.serverDisconnected = defer.Deferred()
        self.serverPort = self._listenServer(self.serverDisconnected)
        self.connected = defer.Deferred()
        self.clientDisconnected = defer.Deferred()
        self.clientConnection = self._connectClient(self.connected,
                                                    self.clientDisconnected)
        return self.connected

    def _listenServer(self, d):
        checker = DjangoAuthChecker()
        realm = Realm()
        portal = Portal(realm, [checker])
        pf = CredAMPServerFactory(portal)
        pf.protocol = CredReceiver
        pf.onConnectionLost = d
        cert = ssl.PrivateCertificate.loadPEM(
            open('../key/private.pem').read())
        return reactor.listenSSL(1234, pf, cert.options())

    def _connectClient(self, d1, d2):
        self.factory = protocol.ClientFactory.forProtocol(ClientProtocolTest)
        self.factory.onConnectionMade = d1
        self.factory.onConnectionLost = d2

        cert = ssl.Certificate.loadPEM(open('../key/public.pem').read())
        options = ssl.optionsForClientTLS(u'humsat.org', cert)

        return reactor.connectSSL("localhost", 1234, self.factory, options)

    def tearDown(self):
        d = defer.maybeDeferred(self.serverPort.stopListening)
        self.clientConnection.disconnect()
        return defer.gatherResults([d,
                                    self.clientDisconnected])

    """
    Call StartRemote method with a non existing slot id
    """

    def test_wrongSlot(self):
        d = login(self.factory.protoInstance, UsernamePassword(
            'testuser', 'testuser.'))
        d.addCallback(lambda l : self.factory.protoInstance.callRemote(StartRemote, iClientId=13, iSlotId=100))
        def checkError(result):
            self.assertEqual(result.message, 'Slot 100 not operational yet')
        return self.assertFailure(d, SlotNotAvailable).addCallback(checkError)

    """
    Call StartRemote method with a existing slot id
    """

    def test_validSlot(self):
        d = login(self.factory.protoInstance, UsernamePassword(
            'testuser', 'testuser.'))
        d.addCallback(lambda l : self.factory.protoInstance.callRemote(StartRemote, iClientId=13, iSlotId=1))
        d.addCallback(lambda res : self.assertEqual(res['iResult'], 1))
        return d