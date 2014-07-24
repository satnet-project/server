from twisted.internet import reactor
from twisted.internet.endpoints import TCP4ClientEndpoint, connectProtocol
from twisted.protocols import amp
from prototipes import *


class Client(amp.AMP):

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

def beginTest():
    d = connectProtocol(destination, Client())

    def connected(ampProto):
        return ampProto.callRemote(StartRemote, iClientId=13, iSlotId=81)
    d.addCallback(connected)
    
    def done(result):
        print 'Done'
        reactor.stop()
    d.addCallback(done)


if __name__ == '__main__':
    destination = TCP4ClientEndpoint(reactor, '127.0.0.1', 1234)
    beginTest()
    reactor.run()
