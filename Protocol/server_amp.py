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


# First of all we need to add satnet-release-1/WebServices to the path
# to import Django modules
import os, sys, logging
sys.path.append(os.path.dirname(os.getcwd())+"/WebServices")
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "website.settings")

from twisted.python import log
from twisted.protocols import amp
from twisted.internet import reactor, ssl
from twisted.internet import protocol
from twisted.cred.portal import Portal

from commands import *
from ampauth.credentials import *
from ampauth.server import *
from errors import SlotNotAvailable

from services.scheduling.models.operational import OperationalSlot
from services.configuration.models.channels import SpacecraftChannel


class Server(amp.AMP):

    def iStartRemote(self, iClientId, iSlotId):
        log.msg("--------- StartRemote ---------")
        slot = OperationalSlot.objects.filter(id=iSlotId)
        if not slot:
          log.err('Slot ' + str(iSlotId) + ' not operational yet')
          raise SlotNotAvailable('Slot ' + str(iSlotId) + ' not operational yet')
        elif len(slot) > 1:
          log.err('Multiple slots with the same id: ' + str(iSlotId))
          raise SlotNotAvailable('Incorrect slot number')
        else:
          #user_id = slot[0].groundstation_channel.user_id
          #print "user id: " + str(user_id)
          #self.callRemote(NotifyError, sDescription="CODE")
          return {'iResult': iSlotId}
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
    logger = logging.getLogger('server')

    log.startLogging(sys.stdout)

    checker = DjangoAuthChecker()
    realm = Realm()
    portal = Portal(realm, [checker])

    pf = CredAMPServerFactory(portal)
    cert = ssl.PrivateCertificate.loadPEM(open('key/private.pem').read())

    reactor.listenSSL(1234, pf, cert.options())
    print 'Server running...'
    reactor.run()

if __name__ == '__main__':
    main()