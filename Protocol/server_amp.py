from twisted.protocols import amp
from twisted.internet import reactor
from twisted.internet.protocol import Factory
from prototipes import *


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
    pf = Factory()
    pf.protocol = Server
    reactor.listenTCP(1234, pf)
    print 'Server running...'
    reactor.run()

if __name__ == '__main__':
    main()
