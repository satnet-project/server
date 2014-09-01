import sys

from twisted.python import log
from twisted.internet import reactor, ssl, defer, protocol, endpoints
from twisted.internet.protocol import ClientCreator
from twisted.internet.error import ReactorNotRunning
from twisted.protocols.amp import AMP
from twisted.cred.credentials import UsernamePassword

from ampauth.client import login
from commands import *


def connected(d):
    d.callRemote(StartRemote, iClientId=13, iSlotId=81)
    log.err("Successful connection")

def notConnected(failure):
    log.err("Error during connection")
    reactor.stop()


class ClientProtocol(AMP):

    """
    CLIENT
    def connectionMade(self):
        d = login(self, UsernamePassword('xabi.crespo', 'pwd4django'))
        d.addCallback(connected)
        d.addErrback(notConnected)
        return d
    """

    def connectionLost(self, reason):
        log.err(reason)
        super(ClientProtocol, self).connectionLost(reason)

    def vNotifyError(self, sDescription):
        print "NotifyError"
        return {}
    NotifyError.responder(vNotifyError)

    def vNotifyConnection(self, iClientId):
        print "NotifyConnection"
        return {}
    NotifyConnection.responder(vNotifyConnection)

    def vNotifyMsg(self, bMsg):
        print "NotifyMsg"
        return {}
    NotifyMsg.responder(vNotifyMsg)

    def vNotifySlotEnd(self, iSlotId):
        print "NotifySlotEnd"
        return {}
    NotifySlotEnd.responder(vNotifySlotEnd)


def beginTest(d, proto):

    def connected(_ignored):
        return proto.callRemote(StartRemote, iClientId=13, iSlotId=81)
    d.addCallback(connected)
    
    def done(result):
        print 'Done'
        reactor.stop()
    d.addCallback(done)


class Client():
    def __init__(self):
        log.startLogging(sys.stdout)

        cert = ssl.Certificate.loadPEM(open('key/public.pem').read())
        options = ssl.optionsForClientTLS(u'humsat.org', cert)

        factory = protocol.Factory.forProtocol(ClientProtocol)
        endpoint = endpoints.SSL4ClientEndpoint(reactor, 'localhost', 1234,
                                                options)
        d = endpoint.connect(factory)
        def endPointConnected(clientAMP):
            self.proto = clientAMP
            return clientAMP
        d.addCallback(endPointConnected)        
        d.addCallback(login, UsernamePassword('xasbi.crespo', 'pwd4django'))

        d.addCallback(connected)
        d.addErrback(notConnected)

        reactor.run()


if __name__ == '__main__':
    c = Client()