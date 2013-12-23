import logging
logger = logging.getLogger(__name__)

from jsonrpc import JsonRpc, publicmethod
from django.core.urlresolvers import reverse
from django.http import HttpResponse

class jrcp_ConfigurationService(object):

    url = reverse("configuration-jrpc")

    @publicmethod
    def addGroundStation(self, identifier, callsign, elevation, \
                            latitude, longitude):
                            
        pass
    
    #def addAvailableSlot()
    #{}
    #def addChannel()
    #{}
    # TODO
    #def delGroundStation()
    #{}

