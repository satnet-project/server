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

from txjsonrpc.web import jsonrpc
from twisted.web import server
from twisted.internet import reactor
import constants


class SATNetClient(jsonrpc.JSONRPC):
    """
    Class implementing the RPC G- or M- clients functions which will be invoked 
    by a G- or M- clients.
    """

    def jsonrpc_vNotifyError(self, sDescription):
        """
        Used to informed a client about an error in the network. 
        :param sDescription:
            
        :type sDescription:
            string
        """
        return

    def jsonrpc_vNotifyConnection(self, iClientId):
        """
        Notifies to a client the connecton of an aditional remote client.
        :param iClientId:
            Client identification number
        :type iClientId:
            int
        """
        return

    def jsonrpc_vNotifyMsg(self, bData, iLen):
        """
        Used to send a message to a remote client.    
        :param bData:
            Remote client identification number
        :type bData:
            
        :param iLen:
            Length of the data
        :type iLen:    
            int      
        """
        return

    def jsonrpc_vNotifySlotEnd(self, iSlotId):
        """
        Notifies to a client the end of the operations slot.    
        :param iSlotId:
            Slot identification number
        :type iSlotId:
            int
        """
        return


if __name__ == '__main__':
    r = SATNetClient()
    reactor.listenTCP(7080, server.Site(r))
    reactor.run()