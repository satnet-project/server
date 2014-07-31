from twisted.protocols import amp
from twisted.internet import reactor, ssl
from twisted.internet.protocol import Factory
from prototipes import *
from twisted.python import log
import sys


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

    pf = Factory()
    pf.protocol = Server
    cert = ssl.PrivateCertificate.loadPEM(open('key/private.pem').read())

    reactor.listenSSL(1234, pf, cert.options())
    print 'Server running...'
    reactor.run()

if __name__ == '__main__':
    main()
