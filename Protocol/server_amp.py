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
import os
import sys
import logging
sys.path.append(os.path.dirname(os.getcwd()) + "/WebServices")
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "website.settings")

from twisted.python import log
from twisted.protocols.amp import AMP
from twisted.internet import reactor, ssl
from twisted.internet import protocol
from twisted.cred.portal import Portal

from commands import *
from ampauth.credentials import *
from ampauth.server import *
from errors import *

from services.scheduling.models import operational
from services.configuration.models.channels import SpacecraftChannel


class SATNETServer(AMP):

    """
    Integration between AMP and L{twisted.cred}. This class is only intended
    to be used for credentials purposes. The specific SATNET protocol will be
    implemented in L{SATNETServer} (see server_amp.py).

    :ivar sUsername:
        Each protocol belongs to a User. This field represents User.username
    :type sUsername:
        L{String}

    :ivar factory:
        CredAMPServerFactory instance which handles SATNETServer instances as well
        as CredReceiver instances    
    :type factory.active_protocols:
        L{ServerFactory}

    """

    factory = None
    sUsername = ""

    def dataReceived(self, data):
        log.msg(self.sUsername + ' session timeout reset')
        self.resetTimeout()
        super(SATNETServer, self).dataReceived(data)

    def iStartRemote(self, iSlotId):
        log.msg("--------- Start Remote ---------")
        slot = operational.OperationalSlot.objects.filter(id=iSlotId)
        # If slot NOT operational yet...
        if not slot:
            log.err('Slot ' + str(iSlotId) + ' not operational yet')
            raise SlotErrorNotification(
                'Slot ' + str(iSlotId) + ' not operational yet')
        # ... if multiple slots have the same ID (never should happen)...
        elif len(slot) > 1:
            log.err('Multiple slots with the same id: ' + str(iSlotId))
            raise SlotErrorNotification('Incorrect slot number')
        # ... if the ID is correct
        else:
            # If it is too soon to connect to this slot...
            if slot[0].state != operational.STATE_RESERVED:
                log.err('Slot has not been reserved yet')
                raise SlotErrorNotification('Slot has not been reserved yet')
            gs_user = slot[
                0].groundstation_channel.groundstation_set.all()[0].user.username
            sc_user = slot[
                0].spacecraft_channel.spacecraft_set.all()[0].user.username
            # If this slot has not been assigned to this user...
            if gs_user != self.sUsername and sc_user != self.sUsername:
                log.err('This slot has not been assigned to this user')
                raise SlotErrorNotification(
                    'This user has not been asigned to this slot')
            #... if the GS user and the SC user belong to the same client...
            elif gs_user == self.sUsername and sc_user == self.sUsername:
                log.msg('Both MCC and GSS belong to the same client')
                return {'iResult': StartRemote.CLIENTS_COINCIDE}
            #... if the remote client is the SC user...
            elif gs_user == self.sUsername:
                self.gs_user = self.sUsername
                if not self.factory.active_protocols[str(sc_user)]:
                    log.msg('Remote user not connected yet')
                    return {'iResult': StartRemote.REMOTE_NOT_CONNECTED}
                else:
                    log.msg('Remote user is ' + sc_user)
                    self.factory.active_connections[gs_user] = sc_user
                    self.factory.active_connections[sc_user] = gs_user
                    self.factory.active_protocols[sc_user].callRemote(
                        NotifyConnection, sClientId=str(gs_user))
                #... if the remote client is the GS user...
            elif sc_user == self.sUsername:
                self.sc_user = self.sUsername
                if str(gs_user) not in self.factory.active_protocols:
                    log.msg('Remote user ' + gs_user + ' not connected yet')
                    return {'iResult': StartRemote.REMOTE_NOT_CONNECTED}
                else:
                    log.msg('Remote user is ' + gs_user)
                    self.factory.active_connections[gs_user] = sc_user
                    self.factory.active_connections[sc_user] = gs_user
                    self.factory.active_protocols[gs_user].callRemote(
                        NotifyConnection, sClientId=str(sc_user))

            return {'iResult': iSlotId}
    StartRemote.responder(iStartRemote)

    def vEndRemote(self):
        print "EndRemote"
        return {}
    EndRemote.responder(vEndRemote)

    def vSendMsg(self, sMsg):
        log.msg("--------- Send Message ---------")
        self.factory.active_protocols[
            self.sUsername].callRemote(NotifyMsg, sMsg=sMsg)

        return {}
    SendMsg.responder(vSendMsg)

    def vRemoteClientDisconnected(self):
        self.callRemote(NotifyError, sDescription='Remote client ' +
                        str(self.factory.active_connections[self.sUsername]) + ' was disconnected')


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
