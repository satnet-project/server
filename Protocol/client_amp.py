import sys

from twisted.python import log
from twisted.internet import reactor, protocol, ssl, defer
from twisted.protocols.amp import AMP
from twisted.cred.credentials import UsernamePassword

from ampauth.client import login
from commands import *


class ClientProtocol(AMP):

    #def connectionMade(self):
    #    d = self.callRemote(StartRemote, iClientId=13, iSlotId=81)

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

def connected(d):
    d.callRemote(StartRemote, iClientId=13, iSlotId=81)
    log.err("Successful connection")

def notConnected(failure):
    log.err("Error during connection")
    reactor.stop()

if __name__ == '__main__':
    log.startLogging(sys.stdout)

    cert = ssl.Certificate.loadPEM(open('key/public.pem').read())
    options = ssl.optionsForClientTLS(u'humsat.org', cert)
    cc = protocol.ClientCreator(reactor, ClientProtocol)
    d = cc.connectSSL('localhost', 1234, options)
    d.addCallback(login, UsernamePassword('xabi.crespo', 'pwd4django'))
    d.addCallback(connected)
    d.addErrback(notConnected)
    reactor.run()