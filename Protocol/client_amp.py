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
    d = proto.callRemote(StartRemote, iSlotId=1)
    def printError(error):
        print error
    d.addErrback(printError)
    log.err("Successful connection")

def notConnected(failure):
    log.err("Error during connection")
    reactor.stop()


class ClientProtocol(AMP):
    USERNAME = 'crespo'
    PASSWORD = 'cre.spo'
    def connectionMade(self):
        d = login(self, UsernamePassword(self.USERNAME, self.PASSWORD))
        def connected(self, proto):
            proto.callRemote(StartRemote, iSlotId=1)
        d.addCallback(connected, self)
        d.addErrback(notConnected)
        return d

    def connectionLost(self, reason):
        log.err(reason)
        super(ClientProtocol, self).connectionLost(reason)

    def vNotifyMsg(self, sMsg):
        log.msg("(" + self.USERNAME + ") --------- Notify Message ---------")
        log.msg(sMsg)
        self.callRemote(EndRemote)                
        return {}
    NotifyMsg.responder(vNotifyMsg)

    def vNotifyEvent(self, iEvent, sDetails):
        log.msg("(" + self.USERNAME + ") --------- Notify Event ---------")
        if iEvent == NotifyEvent.SLOT_END:
            log.msg("Disconnection because the slot has ended")
        elif iEvent == NotifyEvent.REMOTE_DISCONNECTED:
            log.msg("Remote client has lost the connection")
        elif iEvent == NotifyEvent.END_REMOTE:
            log.msg("Disconnection because the remote client has been disconnected")
        elif iEvent == NotifyEvent.REMOTE_CONNECTED:
            log.msg("The remote client has just connected")

        return {}
    NotifyEvent.responder(vNotifyEvent)


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