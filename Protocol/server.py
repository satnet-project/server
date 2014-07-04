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


class SATNetServer(jsonrpc.JSONRPC):
    """
    Class implementing the RPC N-server functions which will be invoked by a
    G- or M- clients.
    """

    def jsonrpc_iStartRemote(self, iClientId, iSlotId):
        """
        Invoked when a client wants to connect to an N-server.    
        :param iClientId:
            Remote client identification number
        :type iClientId:
            int
        :param iClientId:
            
        :type iClientId:
            int
        
        :returns:
            Code indicating whether the slot has ended or not, and whether the 
            other client required for the remote operation is still connected or not.
        :rtype:
            int    
        """
        return

    def jsonrpc_vEndRemote(self):
        """
        Invoked to send a message to a remote entity.        
        """
        return

    def jsonrpc_vSendMsg(self, iSlotId):
        """
        Invoked when a client wants to finalize the remote operation.    
        :param iClientId:
            Remote client identification number
        :type iClientId:
            int
        """
        return

if __name__ == '__main__':
    r = SATNetServer()
    reactor.listenTCP(7080, server.Site(r))
    reactor.run()