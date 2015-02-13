"""
   Copyright 2013, 2014 Ricardo Tubio-Pardavila

   Licensed under the Apache License, Version 2.0 (the "License");
   you may not use this file except in compliance with the License.
   You may obtain a copy of the License at

       http://www.apache.org/licenses/LICENSE-2.0

   Unless required by applicable law or agreed to in writing, software
   distributed under the License is distributed on an "AS IS" BASIS,
   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
   See the License for the specific language governing permissions and
   limitations under the License.
"""
__author__ = 'rtubiopa@calpoly.edu'

import base64
import logging
import json
import urllib.request, urllib.error, urllib.parse
from services.common import ax25
from website import settings as satnet_cfg

logger = logging.getLogger('common')


class ExocubeService(object):
    """Remote JSON service
    Basic class that handles the remote invokation of the ExoCube data
    reporting service.
    """

    EXOCUBE_URL = 'https://satcom.calpoly.edu/cgi-bin/polysat-pub/decoder.json'

    last_response = None

    @staticmethod
    def create_message(passive_message):
        """
        Creates a JSON-like structure using the information from the just
        received passive message.
        {
            "mission":"exocube",
            "live":0,
            "name":"anonymous",
            "callsign":"anonymous",
            "lat":35.3471,
            "long":-120.4553,
            "time":1,
            "rssi":0.0,
            "range":null,
            "az":null,
            "el":null,
            "packet":"C09C6C86A040400296966C908E861503CC450000F700004000011188"
        }
        :param passive_message: The just-received message
        :return: JSON-like structure
        """

        hex_string = base64.b64decode(passive_message.message).decode()

        return {
            'mission': 'ExoCube',
            'live': 0,
            'name': passive_message.groundstation.identifier,
            'callsign': passive_message.groundstation.callsign,
            'lat': passive_message.groundstation.latitude,
            'long': passive_message.groundstation.longitude,
            'time': passive_message.groundstation_timestamp,
            'rssi': 0.0,
            'range': None,
            'az': None,
            'el': None,
            'packet': hex_string
        }

    @staticmethod
    def send_exocube(passive_message):
        """
        Specific method for sending an AX.25 frame to the EXOCUBE server.
        :param passive_message: Data message to be sent (database model)
        """
        logger.info('>>> FORWARDING TO EXOCUBE (pass)')
        pass

        """
        try:
            ax25_p = ax25.AX25Packet.decode_base64(passive_message.message)
            logger.info('Received PACKET, decoded AX25 = ' + str(ax25_p))
        except Exception as ex:
            logger.warn('Received PACKET, not AX25, reason = ' + str(ex))

        exocube_data = ExocubeService.create_message(passive_message)
        #data = json.dumps(exocube_data)
        request = urllib.request.Request(
            ExocubeService.EXOCUBE_URL, exocube_data
        )
        request.add_header('content-type', 'application/json')
        request.add_header('content-length', str(len(exocube_data)))
        result = urllib.request.urlopen(request)
        response = result.read()

        if satnet_cfg.TESTING:
            ExocubeService.last_response = response
        logger.info('Response from exocube server: ' + str(response))
        """