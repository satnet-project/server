from twisted.internet import reactor, protocol, ssl
from twisted.protocols.amp import AMP
from prototipes import *
from twisted.python import log
import sys


class ClientProtocol(AMP):

    def connectionMade(self):
        d = self.callRemote(StartRemote, iClientId=13, iSlotId=81)

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


class ClientFactory(protocol.ClientFactory):
    protocol = ClientProtocol


def beginTest(d, proto):

    def connected(_):
        return proto.callRemote(StartRemote, iClientId=13, iSlotId=81)
    d.addCallback(connected)
    
    def done(result):
        print 'Done'
        reactor.stop()
    d.addCallback(done)


if __name__ == '__main__':
    log.startLogging(sys.stdout)
    cert = ssl.Certificate.loadPEM(open('key/public.pem').read())
    options = ssl.optionsForClientTLS(u'humsat.org', cert)

    reactor.connectSSL('localhost', 1234, ClientFactory(), options)
    reactor.run()
