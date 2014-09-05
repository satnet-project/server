# coding=utf-8
"""
   Copyright 2014 Xabier Crespo Álvarez

   Licensed under the Apache License, Version 2.0 (the "License");
   you may not use this file except in compliance with the License.
   You may obtain a copy of the License at

       http://www.apache.org/licenses/LICENSE-2.0

   Unless required by applicable law or agreed to in writing, software
   distributed under the License is distributed on an "AS IS" BASIS,
   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
   See the License for the specific language governing permissions and
   limitations under the License.

:Author:
    Xabier Crespo Álvarez (xabicrespog@gmail.com)
"""
__author__ = 'xabicrespog@gmail.com'


import sys

from twisted.python import log
from twisted.internet import reactor, ssl, defer, protocol, endpoints
from twisted.internet.protocol import ClientCreator
from twisted.internet.error import ReactorNotRunning
from twisted.protocols.amp import AMP
from twisted.cred.credentials import UsernamePassword

from ampauth.client import login
from commands import *


def connected(_ignored, proto):
    d = proto.callRemote(StartRemote, iClientId=13, iSlotId=1)
    def printError(error):
        print error
    d.addErrback(printError)
    log.err("Successful connection")

def notConnected(failure):
    log.err("Error during connection")
    reactor.stop()


class ClientProtocol(AMP):

    def connectionMade(self):
        d = login(self, UsernamePassword('xabi', 'pwdxabi'))
        d.addCallback(connected, self)
        d.addErrback(notConnected)
        return d

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

        reactor.run()


if __name__ == '__main__':
    c = Client()