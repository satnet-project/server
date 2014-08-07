import sys

from twisted.python import log
from twisted.protocols import amp
from twisted.internet import reactor, ssl
from twisted.internet import protocol
from twisted.cred.portal import Portal

from commands import *
from ampauth.credentials import *
from ampauth.server import *

class Server(amp.AMP):

    def iStartRemote(self, iClientId, iSlotId):
        print "StartRemote"
        self.callRemote(NotifyError, sDescription="CODE")
        return {'iResult': 1}
    StartRemote.responder(iStartRemote)
    
    def vEndRemote(self):
        print "EndRemote"
        return {}
    EndRemote.responder(vEndRemote)

    def vSendMsg(self, bMsg):
        print "SendMsg"
        return {}
    SendMsg.responder(vSendMsg)


def main():
    log.startLogging(sys.stdout)

    checker = DjangoAuthChecker()
    realm = Realm()
    portal = Portal(realm, [checker])

    pf = CredAMPServerFactory(portal)
    #pf.protocol = Server
    cert = ssl.PrivateCertificate.loadPEM(open('key/private.pem').read())

    reactor.listenSSL(1234, pf, cert.options())
    print 'Server running...'
    reactor.run()

if __name__ == '__main__':
    main()
